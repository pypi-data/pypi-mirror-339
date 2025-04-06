import json
import pickle
import pytest

from tests import TEST_DATA


@pytest.fixture
def temp_json_file(tmp_path_factory):
    file_path = tmp_path_factory.mktemp('data') / "test.json"
    data = {"key1": 0}
    with open(file_path, "w") as f:
        json.dump(data, f)
    yield file_path


@pytest.fixture
def temp_pickle_file(tmp_path_factory):
    file_path = tmp_path_factory.mktemp('data') / "test.pickle"
    data = {"key1": 0}
    with open(file_path, "wb") as f:
        pickle.dump(data, f)
    yield file_path


@pytest.fixture
def fp_ldc_energy(tmp_path_factory):
    with open(TEST_DATA / "test_energy_meter.json") as f:  # this file will remain as is
        content = json.load(f)
    filepath = tmp_path_factory.mktemp('data') / "test_energy_tmp.json"  # this file will be modified
    with open(filepath, 'w') as f:
        json.dump(content, f)
    yield filepath
