import pytest

from rna_squirrel.config.python_build import PythonBuild
from typing import List

@pytest.fixture
def python_build():
    return PythonBuild()

def test_generate_header_strings(python_build:PythonBuild):
    file_header:List[str] = python_build.generate_config_header()
    assert file_header[1]  == "from typing import TypeVar, Type, List"
    
def test_build_object_enum(python_build:PythonBuild):
    attributes:List[str] = ["PrimaryStructure","Ensemble"]
    class_name:str = "Nut"
    lines: List[str] = python_build.generate_object_enum(class_name=class_name,
                                                         atr_list=attributes)
    assert lines[1] == '\tPrimaryStructure = "PrimaryStructure_DB"'
    
def test_config_definition_generation(python_build:PythonBuild):
    lines:str = python_build.generate_config_baseclass()
    assert lines[0] == 'class NupackStrand(Nut):'