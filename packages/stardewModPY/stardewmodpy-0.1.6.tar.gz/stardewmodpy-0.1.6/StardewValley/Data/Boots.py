from typing import Optional, List
from .model import modelsData
class BootsData(modelsData):
    def __init__(self, key:int):
        super().__init__(key)
    
    def getJson(self) -> str:
        return self.value