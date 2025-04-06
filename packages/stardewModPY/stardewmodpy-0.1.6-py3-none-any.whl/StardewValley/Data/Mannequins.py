from .model import modelsData
from typing import Optional, Any


class MannequinsData(modelsData):
    def __init__(
        self,
        key: str,
        Id: str,
        DisplayName: str,
        Description: str,
        Texture: str,
        SheetIndex: int,
        FarmerTexture: str,
        DisplaysClothingAsMale: Optional[bool] = True,
        Cursed: Optional[bool] = False,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.Id = Id
        self.DisplayName = DisplayName
        self.Description = Description
        self.Texture = Texture
        self.SheetIndex = SheetIndex
        self.FarmerTexture = FarmerTexture
        self.DisplaysClothingAsMale = DisplaysClothingAsMale
        self.Cursed = Cursed
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "Id": self.Id,
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "Texture": self.Texture,
            "SheetIndex": self.SheetIndex,
            "FarmerTexture": self.FarmerTexture,
            "DisplaysClothingAsMale": self.DisplaysClothingAsMale,
            "Cursed": self.Cursed,
            "CustomFields": self.CustomFields
        }
