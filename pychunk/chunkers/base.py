from abc import ABC, abstractmethod

from typing import (List, 
                    Callable, 
                    Optional, 
                    Dict, 
                    Type)

from pychunk.nodes.base import BaseNode
from pychunk.utils.files_handler import TempFileHandler

import hashlib

import os
from fnmatch import fnmatch


class Chunker(ABC):
    
    __extensions_to_type = {'*.py'}
    temp_file_handler = TempFileHandler
    
    def __init__(self, files_path: str | List[str], 
                 hash_function: Optional[Callable] | None = None, 
                 pattern: str = "*.py"):

        if pattern not in self.__extensions_to_type:
            raise ValueError(f"Your pattern is not implemented yet. Available: {self.__extensions_to_type}")
        _files_path = files_path if isinstance(files_path, list) else [files_path]
        self._files_path = []
        for file_path in _files_path:
            self._files_path.extend(self._recursive_retrieval_of_files(file_path=file_path))
            
        self._hash_function = hash_function if hash_function else self._default_hash_function
        self._file_handler = self.temp_file_handler()
        print("Imported files: ", self._files_path)
          
    @abstractmethod
    def _create_nodes_of_file(self, file_path: str) -> Dict[str, Type['BaseNode']]:
        raise NotImplementedError("You need to implement _create_nodes_of_file method.")
    
    @abstractmethod
    def _create_nodes(self) -> Dict[str, Dict[str, Type['BaseNode']]]:
        raise NotImplementedError("You need to implement __create_nodes method.")
    
    @staticmethod
    def _default_hash_function(text: str) -> str:

        hasher = hashlib.new('sha256')
        text = text.replace("\n", "").replace(" ", "")
        if len(text) < 1:
            return ''
        hasher.update(text.encode('utf-8'))
        return hasher.hexdigest()
    
    @staticmethod
    def _recursive_retrieval_of_files(file_path: str, pattern: str="*.py") -> List[str]:
        
        if file_path.endswith(".py"):
            return [file_path]
        
        python_files = []
        for path, _, files in os.walk(file_path):
            if file_path.startswith("."):
                root_path = path.split("/")[-1]
                if root_path.startswith("."): continue
            
            for name in files:
                if ".venv/" in path: continue
                if fnmatch(name, pattern) and name != "__init__.py":
                    python_files.append(os.path.join(path, name))
                    
        python_files = [os.path.abspath(path) for path in python_files]
        return python_files
        
    def _find_venv(self) -> str:
        directories = []
        current_dir = os.path.dirname(os.path.abspath("."))

        while current_dir != '/':
            directories.append(current_dir)
            current_dir = os.path.dirname(current_dir)

        directories.append('/')  
        for dir in directories[:3]:
            for path, _, _ in os.walk(dir): 
                if ".venv" in path:
                    return path
        return None
        
        
            