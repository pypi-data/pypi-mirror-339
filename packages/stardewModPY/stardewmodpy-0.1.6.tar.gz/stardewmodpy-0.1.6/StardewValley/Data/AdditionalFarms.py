from typing import Optional, Dict, Any
from .model import modelsData
import json

class AdditionalFarmsData(modelsData):
    def __init__(self, key: int, Id: str, TooltipStringPath: str, MapName: str, IconTexture: str,
                 WorldMapTexture: str, SpawnMonstersByDefault: bool = False, ModData: Optional[Dict[str, Any]] = None,
                 CustomFields: Optional[str] = None):
        
        super().__init__(key)
        self.Id = Id
        self.TooltipStringPath = TooltipStringPath
        self.MapName = MapName
        self.IconTexture = IconTexture
        self.WorldMapTexture = WorldMapTexture
        self.SpawnMonstersByDefault = SpawnMonstersByDefault
        self.ModData = ModData if ModData is not None else {}
        self.CustomFields = CustomFields

    def getJson(self) -> str:
        return json.dumps({
            "Id": self.Id,
            "TooltipStringPath": self.TooltipStringPath,
            "MapName": self.MapName,
            "IconTexture": self.IconTexture,
            "WorldMapTexture": self.WorldMapTexture,
            "SpawnMonstersByDefault": self.SpawnMonstersByDefault,
            "ModData": self.ModData,
            "CustomFields": self.CustomFields
        }, ensure_ascii=False, indent=4)