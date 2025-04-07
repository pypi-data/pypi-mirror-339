import json
import pickle
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any


class FileHandler(metaclass=ABCMeta):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.check_suffix()
        if not file_path.exists():
            self.save(data=None)

    @abstractmethod
    def load(self) -> Any:
        pass

    @abstractmethod
    def save(self, data) -> None:
        pass

    @abstractmethod
    def expected_suffix(self) -> str:
        """return the expected suffix as string"""
        pass

    def check_suffix(self):
        if self.file_path.suffix != self.expected_suffix():
            raise ValueError(
                f"File must have a {self.expected_suffix()} suffix")

    @property
    def last_modification(self):
        """Timestamp of last modification"""
        return self.file_path.stat().st_mtime


class JsonFileHandler(FileHandler):
    def load(self) -> Any:
        with open(self.file_path, "r") as file:
            return json.load(file)

    def save(self, data) -> None:
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def expected_suffix(self) -> str:
        return ".json"


class PickleFileHandler(FileHandler):
    def load(self) -> Any:
        with open(self.file_path, "rb") as file:
            return pickle.load(file)

    def save(self, data) -> None:
        with open(self.file_path, "wb") as file:
            pickle.dump(data, file)

    def expected_suffix(self) -> str:
        return ".pickle"
