import pytest
from pathlib import Path

from rna_squirrel.config.yaml_operations import YAMLOperations
CONFIG_PATH = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\test_class.yaml")
def test_open_yaml():
    yaml: YAMLOperations = YAMLOperations()
    data = yaml.open_yml_config(file_path=WINDOWS_PATH)
    assert data == ''