import concurrent.futures
import threading
import typing
from time import sleep

from .job_info import JobInfo
from .kawa_directory_manager import KawaDirectoryManager
from .kawa_error_manager import KawaErrorManager
from .kawa_log_manager import get_kawa_logger


class KawaJobsManager:

    def __init__(self,
                 kawa_directory_manager: KawaDirectoryManager,
                 kawa_error_manager: KawaErrorManager):
        self.directory_manager: KawaDirectoryManager = kawa_directory_manager
        self.error_manager: KawaErrorManager = kawa_error_manager
        self.jobs: typing.Dict[str, JobInfo] = {}
        # starts cleaner thread
        self.MAX_OLD_JOB = 24 * 3600  # 24 hours old
        self.CHECK_OLD_JOB_INTERVAL = 1 * 3600  # 1 hour
        threading.Timer(self.CHECK_OLD_JOB_INTERVAL, self.clear_old_jobs).start()

    def add_job(self,
                job_id: str,
                future: concurrent.futures.Future):
        self.jobs[job_id] = JobInfo(job_id, future)

    def get_job_log(self, job_id: str):
        try:
            job_info = self.jobs.get(job_id)
            # in case of ETL preview, we do not dump any logs and job_info will be None
            if not job_info:
                return ''
            result = self.job_poll_result(job_info)
            job_log_path = self.directory_manager.log_path(job_id)
            try:
                with open(job_log_path, 'r') as file:
                    result['log'] = file.read()
                    file.close()
            except FileNotFoundError:
                get_kawa_logger().error(f'FileNotFoundError when getting logs from jobid: {job_id}, ')
                result['log'] = ''
            return result
        except Exception as err:
            get_kawa_logger().error(f'Issue when getting logs from jobid: {job_id} with error : {err}')
            self.error_manager.rethrow(err)

    def poll_jobs(self, poll_jobs):
        try:
            result = {}
            for job_id in poll_jobs:
                job_info = self.jobs.get(job_id)
                if job_info:
                    result[job_id] = self.job_poll_result(job_info)
                else:
                    # Not found, maybe the Python server was restarted
                    result[job_id] = self.job_poll_result_not_found()
            return result
        except Exception as err:
            self.error_manager.rethrow(err)

    def job_poll_result(self, job_info: JobInfo):
        is_done = job_info.future.done()
        # intermediate events: how to know which ones are new since last polling?
        if is_done:
            if job_info.future.cancelled():
                return {'status': 'CANCELLED'}
            elif job_info.future.exception():
                return {
                    'status': 'FAILURE',
                    'error': self.error_manager.error_to_str(job_info.future.exception())
                }
            else:
                return {'status': 'SUCCESS'}  # TODO: result? (which form?)
        else:
            if job_info.future.running():
                return {'status': 'RUNNING'}
            else:
                return {'status': 'PENDING'}

    @staticmethod
    def job_poll_result_not_found():
        # May occur if the Python server was restarted, and so the job queue was lost
        return {'status': 'NOT_FOUND'}

    def delete_job(self,
                   job_id: str,
                   delay_seconds: int = 0
                   ):
        self.clear_old_jobs_from_map()
        sleep(delay_seconds)
        self.directory_manager.remove_job_working_files(job_id)
        self.directory_manager.remove_job_log(job_id)
        self.directory_manager.remove_repo_files(job_id)
        if job_id in self.jobs:
            del self.jobs[job_id]

    def clear_old_jobs(self):
        self.clear_old_jobs_from_map()
        self.directory_manager.remove_files_older_than(self.MAX_OLD_JOB)

    def clear_old_jobs_from_map(self):
        keep = {}
        for job_id, job_info in self.jobs.items():
            if not job_info.is_older(self.MAX_OLD_JOB):
                keep[job_id] = job_info
        self.jobs = keep
