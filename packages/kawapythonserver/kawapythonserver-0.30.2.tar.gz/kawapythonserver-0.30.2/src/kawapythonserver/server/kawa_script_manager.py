import concurrent.futures
import json
import logging
import os
import pickle
import subprocess
import time
from concurrent.futures.thread import BrokenThreadPool

import pyarrow as pa
from kywy.client.kawa_client import KawaClient

from .clear_script_with_secrets import ClearScriptWithSecrets
from .interpreter_error import InterpreterError
from .kawa_directory_manager import KawaDirectoryManager
from .kawa_error_manager import KawaErrorManager
from .kawa_log_manager import KawaLogManager, get_kawa_logger
from .kawa_pex_builder import KawaPexBuilder
from .kawa_script_runner_inputs import ScriptRunnerInputs
from ..scripts.kawa_python_column_loader_callback import PythonColumnLoaderCallback
from ..scripts.kawa_python_datasource_loader_callback import PythonDatasourceLoaderCallback
from ..scripts.kawa_python_datasource_preview_loader_callback import PythonDatasourcePreviewCallback


def _get_executable(clear_script_with_secrets: ClearScriptWithSecrets):
    scope = {}
    exec(clear_script_with_secrets.clear_script, scope, scope)
    functions_in_scope_with_inputs = [v for v in scope.values() if hasattr(v, 'inputs')]
    if len(functions_in_scope_with_inputs) == 0:
        raise InterpreterError('The python script provided does not contain any function with inputs defined with '
                               'the @inputs decorator')
    if len(functions_in_scope_with_inputs) > 1:
        raise InterpreterError('The python script provided contain more than one function with defined inputs')
    final_function = functions_in_scope_with_inputs[0]
    inputs_provided_by_kawa = ['df', 'kawa']
    if hasattr(final_function, 'secrets'):
        secret_mapping = dict(final_function.secrets)
        inputs_provided_by_kawa.extend(secret_mapping.keys())
        if 'kawa' in secret_mapping:
            raise InterpreterError('kawa is a reserved name for the KawaClient and cannot be used in secrets')
        if 'df' in secret_mapping:
            raise InterpreterError('df is a reserved name for the DataFrame input and cannot be used in secrets')
    necessaries_inputs = final_function.__code__.co_varnames[:final_function.__code__.co_argcount]
    missing_arguments = set(necessaries_inputs).difference(inputs_provided_by_kawa)
    if len(missing_arguments) != 0:
        raise InterpreterError(f'Some arguments defined in the main function: {final_function.__name__} are not defined.'
                               f' The list : {missing_arguments}')
    return final_function


def log_subprocess_output(pipe, l):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        l.info('got line from subprocess: %r', line)


def _submit_sub_process(inputs: ScriptRunnerInputs):
    get_kawa_logger().info(f'Starting the sub process to run the script for jobId: {inputs.job_id}')
    start_time = time.time()
    error = ''
    try:
        my_env = os.environ.copy()
        my_env['PEX_EXTRA_SYS_PATH'] = os.pathsep.join([str(inputs.repo_path)])
        get_kawa_logger().info(f'PEX_EXTRA_SYS_PATH is {my_env["PEX_EXTRA_SYS_PATH"]}')
        sub = subprocess.run([
            inputs.pex_file_path, inputs.script_runner_path
        ],
            input=pickle.dumps(inputs),
            timeout=300,
            check=True,
            capture_output=True,
            env=my_env
        )
        execution_time = round(time.time() - start_time, 1)
        get_kawa_logger().info(f'''Logs from subprocess: 
###### SUB PROCESS LOGS START ######
{sub.stdout.decode("unicode_escape")}
###### SUB PROCESS LOGS FINISH ######''')
        get_kawa_logger().info(f'Sub process ended in {execution_time}s')

    except FileNotFoundError as exc:
        error = f'Process failed because the executable could not be found.{exc}'
    except subprocess.CalledProcessError as exc:
        get_kawa_logger().info(exc.stdout.decode("unicode_escape"))
        error = f'Error when execution script: \n {exc.stderr.decode("unicode_escape")}'
    except subprocess.TimeoutExpired as exc:
        get_kawa_logger().info(exc.stdout.decode("unicode_escape"))
        error = f'Process timed out.\n{exc}'
    except Exception as exc:
        get_kawa_logger().info('Some weird exception occurred')
        error = f'Process failed.\n{exc}'
    finally:
        if error:
            get_kawa_logger().error(error)
            raise Exception(error)


class KawaScriptManager:

    def __init__(self,
                 kawa_url,
                 kawa_directory_manager: KawaDirectoryManager,
                 kawa_log_manager: KawaLogManager,
                 kawa_error_manager: KawaErrorManager,
                 pex_executable_path: str,
                 script_runner_path: str):
        self.kawa_url: str = kawa_url
        self._thread_executor: concurrent.futures.ThreadPoolExecutor = concurrent.futures.ThreadPoolExecutor()
        self.directory_manager: KawaDirectoryManager = kawa_directory_manager
        self.kawa_log_manager: KawaLogManager = kawa_log_manager
        self.error_manager: KawaErrorManager = kawa_error_manager
        self.logger: logging.Logger = get_kawa_logger()
        self.pex_executable_path = pex_executable_path
        self.script_runner_path = script_runner_path

    def get_script_metadata(self, clear_script_with_secrets: ClearScriptWithSecrets):
        try:
            script_meta = self._get_function_metadata(clear_script_with_secrets)
            json_meta = json.dumps(script_meta)
            self.logger.debug('Script metadata: %s', json_meta)
            return json_meta
        except Exception as err:
            self.error_manager.rethrow(err)

    def submit_to_thread_executor(self, fn, /, *args, **kwargs) -> concurrent.futures.Future:
        try:
            return self._thread_executor.submit(fn, *args, **kwargs)
        except BrokenThreadPool as broken_exception:
            self.logger.warning(f'Current executor is broken with exception: {broken_exception}')
            self.logger.warning('Shutting it down with cancel futures')
            self._thread_executor.shutdown(cancel_futures=True)
            self.logger.info('Starting a new executor')
            self._thread_executor = concurrent.futures.ThreadPoolExecutor()
            return self._thread_executor.submit(fn, *args, **kwargs)

    def submit_script_for_execution(self,
                                    job_id: str,
                                    principal: str,
                                    clear_script_with_secrets: ClearScriptWithSecrets,
                                    action_payload,
                                    arrow_table: pa.Table,
                                    module: str) -> concurrent.futures.Future:
        start = time.time()
        kawa_client = self._create_kawa_client(action_payload)
        exec_time = round(time.time() - start, 1)
        get_kawa_logger().info(f'kawa_client created in {exec_time}s for jobId: {job_id}')
        callback = self._create_callback(action_payload, kawa_client, clear_script_with_secrets)
        job_log_file = self.directory_manager.log_path(job_id)
        pex_builder = KawaPexBuilder(self.pex_executable_path,
                                     f'{self.directory_manager.repo_path(job_id)}/requirements.txt',
                                     self.directory_manager.pex_path())
        pex_file_path = pex_builder.build_pex_if_necessary(job_id)

        script_parameters_values = action_payload.get('scriptParametersValues', [])
        script_parameters_dict = {p['scriptParameterName']: p['value']
                                  for p in script_parameters_values
                                  if p.get('value') is not None}

        script_runner_inputs = ScriptRunnerInputs(
            self.script_runner_path,
            pex_file_path,
            job_id,
            module,
            job_log_file,
            clear_script_with_secrets.kawa_secrets,
            self.directory_manager.repo_path(job_id),
            kawa_client,
            callback,
            arrow_table,
            clear_script_with_secrets.meta_data,
            script_parameters_dict
        )
        return self.submit_to_thread_executor(_submit_sub_process, script_runner_inputs)

    @staticmethod
    def _get_function_metadata(clear_script_with_secrets: ClearScriptWithSecrets):
        func = _get_executable(clear_script_with_secrets)
        return {
            'parameters': func.inputs,
            'outputs': func.outputs if hasattr(func, 'outputs') else []
        }

    def _create_callback(self, action_payload,
                         kawa_client: KawaClient,
                         clear_script_with_secrets: ClearScriptWithSecrets):
        job_id = str(action_payload['job']).split('|')[1]
        if action_payload.get('pythonPrivateJoinId'):
            python_private_join_id = action_payload.get('pythonPrivateJoinId')
            dashboard_id = action_payload.get('dashboardId')
            application_id = action_payload.get('applicationId')
            return PythonColumnLoaderCallback(python_private_join_id,
                                              job_id,
                                              kawa_client,
                                              dashboard_id,
                                              application_id)
        if action_payload.get('dataSourceId'):
            datasource_id = action_payload.get('dataSourceId')
            reset_before_insert = action_payload.get('isFullRefresh')
            optimize_after_insert = action_payload.get('optimizeTableAfterInsert')
            return PythonDatasourceLoaderCallback(datasource_id=datasource_id,
                                                  reset_before_insert=reset_before_insert,
                                                  optimize_after_insert=optimize_after_insert,
                                                  job_id=job_id,
                                                  kawa_client=kawa_client)
        if action_payload.get('isPreview'):
            return PythonDatasourcePreviewCallback(job_id,
                                                   clear_script_with_secrets.meta_data,
                                                   self.directory_manager)

        return None

    def _create_kawa_client(self, action_payload) -> KawaClient:
        workspace_id = action_payload.get('workspaceId')
        api_key = action_payload.get('apiKey')
        if not api_key:
            return KawaClient(kawa_api_url=self.kawa_url)  # if key is not there we don;t need the client
        kawa_client = KawaClient(kawa_api_url=self.kawa_url)
        kawa_client.set_api_key(api_key=api_key)
        kawa_client.set_active_workspace_id(workspace_id=workspace_id)
        return kawa_client
