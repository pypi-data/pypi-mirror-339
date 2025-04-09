import shutil

import pyarrow as pa
import io
import time

from .kawa_error_manager import KawaErrorManager
from .kawa_log_manager import get_kawa_logger

_dataset_path_suffix = '_dataset'
_script_path_suffix = '_script'
_etl_preview_path_suffix = '_etl_preview'
_log_path_suffix = '_log'
_repo_path_suffix = '_repo'


class KawaDirectoryManager:

    def __init__(self,
                 working_directory,
                 kawa_error_manager: KawaErrorManager):
        self.error_manager: KawaErrorManager = kawa_error_manager
        self._working_directory = working_directory
        self._working_directory.mkdir(exist_ok=True)

    def dataset_path(self, job_id: str):
        return self._working_directory / (job_id + _dataset_path_suffix)

    def script_path(self, job_id: str):
        without_pipe = job_id.replace('|', '')
        return self._working_directory / (without_pipe + _script_path_suffix)

    def etl_preview_path(self, job_id: str):
        without_pipe = job_id.replace('|', '')
        return self._working_directory / (without_pipe + _etl_preview_path_suffix)

    def repo_path(self, job_id: str):
        without_pipe = job_id.replace('|', '')
        return self._working_directory / (without_pipe + _repo_path_suffix)

    def log_path(self, job_id: str):
        return self._working_directory / (job_id + _log_path_suffix)

    def pex_path(self):
        return self._working_directory / 'pex'

    def write_table(self, job_id: str, data_table: pa.Table):
        try:
            pa.parquet.write_table(data_table, self.dataset_path(job_id))
        except Exception as err:
            self.error_manager.rethrow(err)

    def read_table(self, job_id: str) -> pa.Table:
        try:
            return pa.parquet.read_table(self.dataset_path(job_id))
        except Exception as err:
            self.error_manager.rethrow(err)

    def write_encrypted_script(self, job_id: str, encrypted_script: str):
        try:
            with io.open(self.script_path(job_id), 'w', encoding='utf8') as f:
                f.write(encrypted_script)
        except Exception as err:
            self.error_manager.rethrow(err)

    def read_encrypted_script(self, job_id: str) -> str:
        try:
            with io.open(self.script_path(job_id), 'r', encoding='utf8') as f:
                encrypted_script = f.read()
            return encrypted_script
        except Exception as err:
            self.error_manager.rethrow(err)

    def write_json_etl_preview(self, job_id: str, json: str):
        try:
            with io.open(self.etl_preview_path(job_id), 'w', encoding='utf8') as f:
                f.write(json)
        except Exception as err:
            self.error_manager.rethrow(err)

    def read_json_etl_preview(self, job_id: str) -> str:
        try:
            with io.open(self.etl_preview_path(job_id), 'r', encoding='utf8') as f:
                etl_preview = f.read()
            return etl_preview
        except Exception as err:
            self.error_manager.rethrow(err)

    def remove_job_working_files(self, job_id):
        get_kawa_logger().debug('Remove working files for job: %s', job_id)
        self._remove_file_if_exists(self.dataset_path(job_id))
        self._remove_file_if_exists(self.script_path(job_id))

    def remove_repo_files(self, job_id):
        get_kawa_logger().debug('Remove repo files for job: %s', job_id)
        self._remove_folder_and_files_if_exists(self.repo_path(job_id))

    def remove_job_log(self, job_id):
        get_kawa_logger().debug('Remove log file for job: %s', job_id)
        self._remove_file_if_exists(self.log_path(job_id))

    def remove_files_older_than(self, max_age: int):
        self._remove_files_older_than(max_age, '*' + _dataset_path_suffix)
        self._remove_files_older_than(max_age, '*' + _script_path_suffix)

    def _remove_files_older_than(self, max_age: int, pattern: str):
        for item in self._working_directory.glob(pattern):
            if item.is_file():
                mtime = item.stat().st_mtime
                if time.time() - mtime > max_age:
                    self._remove_file_if_exists(item)

    def _remove_file_if_exists(self, file):
        try:
            get_kawa_logger().debug('remove file: %s' + file.name)
            file.unlink()
        except Exception:
            pass

    def _remove_folder_and_files_if_exists(self, file):
        try:
            get_kawa_logger().debug('remove path: %s' + file.name)
            shutil.rmtree(file)
        except Exception:
            pass

    def is_dataset_file(self, file):
        return file.name().endswith('_dataset')
