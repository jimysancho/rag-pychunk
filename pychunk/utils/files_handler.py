import tempfile
import shutil

from typing import Type

class TempFileHandler:
    
    def __init__(self):
        self._tmp_folder = self._create_tmp_folder()
    
    @property
    def tmp_folder(self):
        return self._tmp_folder
    
    def create(self) -> Type['TempFileHandler']:
        self._tmp_folder = self._create_tmp_folder()
        return self
                
    def _create_tmp_folder(self) -> str:
        return tempfile.mkdtemp()
    
    def delete_tmp_folder(self) -> None:
        shutil.rmtree(self._tmp_folder)
