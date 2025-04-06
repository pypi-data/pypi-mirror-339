import pickle
import pytest
import json

from src.berroutils.plugins.file_handler import JsonFileHandler, PickleFileHandler


def test_save_json(temp_json_file):
    handler = JsonFileHandler(temp_json_file)
    data = {"key": "value"}
    handler.save(data)

    with open(temp_json_file, "r") as file:
        content = json.load(file)

    assert content == data


def test_load_json(temp_json_file):
    handler = JsonFileHandler(temp_json_file)
    content = handler.load()

    assert content == {"key1": 0}


def test_nonexisting_fp(tmp_path):
    """Test initiation of class with nonexiting path (handler)
    Test initiation of class with empty file (handler_2)"""
    new_path = tmp_path / "new_test.json"
    handler = JsonFileHandler(new_path)

    with open(new_path, "r") as f:
        data = json.load(f)
    assert not data

    handler_2 = JsonFileHandler(new_path)
    content = handler_2.load()
    assert not content


def test_check_suffix(temp_json_file):
    with pytest.raises(ValueError):
        JsonFileHandler(temp_json_file.with_suffix(".txt"))


def test_save_pickle(temp_pickle_file):
    handler = PickleFileHandler(temp_pickle_file)
    data = {"key": "value"}
    handler.save(data)

    with open(temp_pickle_file, "rb") as file:
        content = pickle.load(file)

    assert content == data


def test_load_pickle(temp_pickle_file):
    handler = PickleFileHandler(temp_pickle_file)
    content = handler.load()

    assert content == {"key1": 0}
