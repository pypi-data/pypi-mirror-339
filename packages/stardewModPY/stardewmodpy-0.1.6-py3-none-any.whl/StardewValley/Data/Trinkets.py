from .model import modelsData
from typing import Any, Optional

class TrinketsData(modelsData):
    def __init__(
            self,
            key: str,
            DisplayName: str,
            Description: str,
            Texture: str,
            SheetIndex: int,
            TrinketEffectClass: str,
            DropsNaturally: Optional[bool]=True,
            CanBeReforged: Optional[bool]=True,
            CustomFields: Optional[dict[str, str]] = None,
            ModData: Optional[dict[str, str]] = None
        ):
        super().__init__(key)

        self.DisplayName = DisplayName
        self.Description = Description
        self.Texture = Texture
        self.SheetIndex = SheetIndex
        self.TrinketEffectClass = TrinketEffectClass
        self.DropsNaturally = DropsNaturally
        self.CanBeReforged = CanBeReforged
        self.CustomFields = CustomFields
        self.ModData = ModData

    def getJson(self) -> dict:
        return {
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "Texture": self.Texture,
            "SheetIndex": self.SheetIndex,
            "TrinketEffectClass": self.TrinketEffectClass,
            "DropsNaturally": self.DropsNaturally,
            "CanBeReforged": self.CanBeReforged,
            "CustomFields": self.CustomFields,
            "ModData": self.ModData
        }
