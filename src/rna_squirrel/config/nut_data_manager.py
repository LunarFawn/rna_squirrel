"""
File for managing how data is saved and accessed
"""

from ruamel.yaml import YAML


class YamlDataOperations():
    """
    Class for handeling using yaml files
    for rough quick file access
    """
    
    def __init__(self) -> None:
        self._yaml:YAML = YAML()
        
    @property
    def yaml(self)->YAML:
        return self._yaml
    
    def save_data(self):
        pass