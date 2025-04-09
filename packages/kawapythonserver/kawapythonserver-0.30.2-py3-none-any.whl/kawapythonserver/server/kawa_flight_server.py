import concurrent.futures
import glob
import json
import logging
import os
import time
import traceback
from dataclasses import dataclass

import pyarrow as pa
import pyarrow.flight
import pyarrow.parquet

from .clear_script_with_secrets import ClearScriptWithSecrets
from .interpreter_error import InterpreterError
from .kawa_directory_manager import KawaDirectoryManager
from .kawa_error_manager import KawaErrorManager
from .kawa_jobs_manager import KawaJobsManager
from .kawa_log_manager import KawaLogManager, get_kawa_logger
from .kawa_script_manager import KawaScriptManager
from ..scripts.kawa_tool_kit import build_kawa_toolkit_from_yaml_file


class KawaFlightServer(pa.flight.FlightServerBase):

    def __init__(self,
                 dict_logging_config,
                 job_logging_level,
                 job_logging_formatter,
                 pex_executable_path: str,
                 script_runner_path: str,
                 location=None,
                 working_directory=None,
                 tls_certificates=None,
                 aes_key=None,
                 kawa_url=None,
                 **kwargs):
        super(KawaFlightServer, self).__init__(location=location, tls_certificates=tls_certificates, **kwargs)
        self._location = location
        self._aes_key = aes_key
        self.kawa_url = kawa_url
        self.executor: concurrent.futures.ProcessPoolExecutor = concurrent.futures.ProcessPoolExecutor()

        self.error_manager: KawaErrorManager = KawaErrorManager()
        self.directory_manager: KawaDirectoryManager = KawaDirectoryManager(working_directory, self.error_manager)
        self.jobs_manager: KawaJobsManager = KawaJobsManager(self.directory_manager, self.error_manager)
        self.log_manager: KawaLogManager = KawaLogManager(
            dict_logging_config,
            job_logging_level,
            logging.Formatter(job_logging_formatter)
        )
        self.script_manager: KawaScriptManager = KawaScriptManager(kawa_url,
                                                                   self.directory_manager,
                                                                   self.log_manager,
                                                                   self.error_manager,
                                                                   pex_executable_path,
                                                                   script_runner_path)

        get_kawa_logger().info('KAWA Python automation server started at location: %s', self._location)

    def _make_flight_info(self, job_id):
        schema = pa.parquet.read_schema(self.directory_manager.dataset_path(job_id))
        metadata = pa.parquet.read_metadata(self.directory_manager.dataset_path(job_id))
        descriptor = pa.flight.FlightDescriptor.for_path(
            job_id.encode('utf-8')
        )
        endpoints = [pa.flight.FlightEndpoint(job_id, [self._location])]
        return pyarrow.flight.FlightInfo(schema,
                                         descriptor,
                                         endpoints,
                                         metadata.num_rows,
                                         metadata.serialized_size)

    def list_flights(self, context, criteria):
        raise InterpreterError('Not supported')

    def get_flight_info(self, context, descriptor):
        return self._make_flight_info(descriptor.path[0].decode('utf-8'))

    def do_put(self, context, descriptor, reader, writer):
        job_id = descriptor.path[0].decode('utf-8')
        data_table = reader.read_all()
        get_kawa_logger().info('Upload dataset for job: %s', job_id)
        self.directory_manager.write_table(job_id, data_table)

    def do_get(self, context, ticket):
        job_id = ticket.ticket.decode('utf-8')
        get_kawa_logger().info('Download dataset for job: %s', job_id)
        return pa.flight.RecordBatchStream(self.directory_manager.read_table(job_id))

    def list_actions(self, context):
        return [
            ('run_script', 'Queue an automation script for execution.'),
            ('restart_script', 'Restart an already uploaded script.'),
            ('script_metadata', 'Get automation script metadata (parameters, outputs).'),
            ('poll_jobs', 'Poll status of specific queued jobs.'),
            ('health', 'Check server health.'),
            ('etl_preview', 'Load a preview of the output of the script')
        ]

    def do_action(self, context, action):
        try:
            get_kawa_logger().debug('action.type: %s', action.type)
            if action.type == 'run_script':
                self.action_run_script(action)
            elif action.type == 'script_metadata':
                json_result = self.action_script_metadata(action)
                return self.json_to_array_of_one_flight_result(json_result)
            elif action.type == 'poll_jobs':
                json_result = self.action_poll_jobs(action)
                return self.json_to_array_of_one_flight_result(json_result)
            elif action.type == 'get_job_log':
                json_result = self.action_get_job_log(action)
                return self.json_to_array_of_one_flight_result(json_result)
            elif action.type == 'delete_job':
                self.action_delete_job(action)
            elif action.type == 'health':
                # Improve it later
                return self.json_to_array_of_one_flight_result('{"status":"OK"}')
            elif action.type == 'etl_preview':
                return self.json_to_array_of_one_flight_result(self.action_etl_preview(action))
            else:
                raise NotImplementedError
        except Exception as err:
            traceback.print_exception(err)
            self.error_manager.rethrow(err)

    def action_run_script(self, action):
        try:
            self.run_script(action)
        except Exception as err:
            self.error_manager.rethrow(err)

    def action_etl_preview(self, action):
        try:
            fut, job_id = self.run_script(action)
            fut.result()  # will wait until future is done
            etl_preview_json = self.directory_manager.read_json_etl_preview(job_id.split('|')[1])
            return EtlPreviewResult(etl_preview_json, '').to_json()
        except Exception as err:
            get_kawa_logger().error(f'Error when getting etl preview: {err}')
            res = EtlPreviewResult('', str(err)).to_json()
            return res

    def run_script(self, action):
        json_action_payload = self.parse_action_payload(action)
        job_id = json_action_payload['job']
        get_kawa_logger().info(f'**** New script execution requested for jobId {job_id}')
        principal = json_action_payload['principal']
        encrypted_script_with_secrets = json_action_payload['script']
        return (self.do_submit_script_for_execution(job_id,
                                                    principal,
                                                    encrypted_script_with_secrets,
                                                    json_action_payload), job_id)

    def action_script_metadata(self, action):
        json_action_payload = self.parse_action_payload(action)
        encrypted_script_with_secrets = json_action_payload['script']
        clear_script_with_secrets = ClearScriptWithSecrets.decrypt(encrypted_script_with_secrets, self._aes_key)
        return self.script_manager.get_script_metadata(
            clear_script_with_secrets=clear_script_with_secrets
        )

    def action_poll_jobs(self, action):
        json_action_payload = self.parse_action_payload(action)
        poll_jobs = json_action_payload['jobs']
        return json.dumps(self.jobs_manager.poll_jobs(poll_jobs))

    def action_get_job_log(self, action):
        try:
            json_action_payload = self.parse_action_payload(action)
            job_id = json_action_payload['job']
            res = self.jobs_manager.get_job_log(job_id)
            get_kawa_logger().debug(f'Result from job loading: {res}')
            return json.dumps(res)
        except Exception as e:
            get_kawa_logger().error(f'Issue when loading logs for {job_id} with error: {e}')

    def action_delete_job(self, action):
        json_action_payload = self.parse_action_payload(action)
        job_id = json_action_payload['job']
        delay = json_action_payload.get('delay', 0)
        if isinstance(delay, int):
            time.sleep(delay)
        self.jobs_manager.delete_job(job_id)

    def do_submit_script_for_execution(self,
                                       job_id: str,
                                       principal: str,
                                       encrypted_script_with_secrets: str,
                                       json_action_payload) -> concurrent.futures.Future:
        clear_script_with_secrets = ClearScriptWithSecrets.decrypt(encrypted_script_with_secrets, self._aes_key)
        self.load_package_from_source_control(clear_script_with_secrets, job_id)
        module = self.extract_module_from_package_and_task(clear_script_with_secrets,
                                                           job_id)
        get_kawa_logger().debug(f'MODULE TO USE: {module} for jobId: {job_id}')
        is_automation_job = not (
                'pythonPrivateJoinId' in json_action_payload or
                'dataSourceId' in json_action_payload or
                'isPreview' in json_action_payload)
        arrow_table = self.directory_manager.read_table(job_id) if is_automation_job else None
        future = self.script_manager.submit_script_for_execution(
            job_id=job_id,
            principal=principal,
            clear_script_with_secrets=clear_script_with_secrets,
            action_payload=json_action_payload,
            arrow_table=arrow_table,
            module=module
        )
        future.add_done_callback(lambda f: self.on_run_script_complete(f, job_id))
        self.jobs_manager.add_job(job_id, future)
        return future

    def extract_module_from_package_and_task(self,
                                             clear_script_wit_secrets: ClearScriptWithSecrets,
                                             job_id: str) -> str:
        if clear_script_wit_secrets.is_from_kawa_source_control():
            return 'kawa_managed_tool'
        toolkit_name, tool_name = clear_script_wit_secrets.toolkit, clear_script_wit_secrets.tool
        repo_path = self.directory_manager.repo_path(job_id)
        files = glob.glob(f'{repo_path}/**/kawa-toolkit.yaml', recursive=True)
        kawa_toolkits = [build_kawa_toolkit_from_yaml_file(repo_path, file) for file in files]
        for kawa_toolkit in kawa_toolkits:
            if kawa_toolkit.name != toolkit_name:
                continue
            for tool in kawa_toolkit.tools:
                if tool.name != tool_name:
                    continue
                return tool.module

        raise Exception(f'No module found in the repo for toolkit: {toolkit_name} and tool: {tool_name}')

    def load_package_from_source_control(self, clear_script_with_secrets: ClearScriptWithSecrets,
                                         job_id: str):
        start_time = time.time()
        repo_path = self.directory_manager.repo_path(job_id)
        get_kawa_logger().info(f'Start loading repo from source control in {repo_path} for jobId: {job_id}')
        if clear_script_with_secrets.is_from_kawa_source_control():
            # in case of tool coming from kawa source control, we just load the content from ClearScriptWithSecrets
            # and copy it to the repo path
            os.mkdir(repo_path)
            with open(f'{repo_path}/kawa_managed_tool.py', 'w') as file:
                file.write(clear_script_with_secrets.content)
            with open(f'{repo_path}/requirements.txt', 'w') as file:
                file.write(clear_script_with_secrets.requirements)
        else:
            command = 'git clone -b {branch} --single-branch https://oauth2:{token}@{repo_rul} {repo_path}'.format(
                branch=clear_script_with_secrets.branch,
                token=clear_script_with_secrets.repo_key,
                repo_rul=clear_script_with_secrets.repo_url.replace('https://', ''),
                repo_path=repo_path
            )
            os.system(command)
        t = round(time.time() - start_time, 1)
        get_kawa_logger().info(f'End loading repo in {t}s from source control for jobId: {job_id}')

    def on_run_script_complete(self, future, job_id):
        get_kawa_logger().debug('Script execution complete, for job: %s', job_id)
        self.directory_manager.remove_job_working_files(job_id)
        self.directory_manager.remove_repo_files(job_id)

    @staticmethod
    def json_to_array_of_one_flight_result(json_result: str):
        flight_result = pyarrow.flight.Result(pyarrow.py_buffer(json_result.encode('utf-8')))
        return [flight_result]

    @staticmethod
    def parse_action_payload(action: pyarrow.flight.Action):
        return json.loads(action.body.to_pybytes().decode('utf-8'))


@dataclass
class EtlPreviewResult:

    result: str
    error: str

    def to_json(self):
        return json.dumps(self.__dict__)
