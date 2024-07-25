"""
File for handeling manipulation of memory
"""

import psutil
# from psutil._pswindows import svmem
# from psutil._pslinux import svmem
from dataclasses import dataclass


@dataclass
class MemoryResources():
    total_memory:int
    free_memory:int
    


def get_memory_resources():
    current_resources = psutil.virtual_memory()
    