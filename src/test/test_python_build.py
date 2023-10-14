import pytest

from rna_squirrel.config.python_build import PythonBuild
from typing import List

@pytest.fixture
def python_build():
    return PythonBuild()

def test_generate_header_strings(python_build:PythonBuild):
    file_header:List[str] = python_build.generate_config_header()
    assert file_header[1]  == "from typing import TypeVar, Type, List" 