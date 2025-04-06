from .model import modelsData
from typing import Optional, Any


class FruitTreesData(modelsData):
    def __init__(
        self,
        key: str,
        DisplayName: str,
        Seasons: list[str],
        Fruit: list[dict[str, Any]],
        Texture: str,
        TextureSpriteRow: int,
        PlantableLocationRules: Optional[list[Any]] = None,
        CustomFields: Optional[Any] = None
    ):  
        super().__init__(key)
        self.DisplayName = DisplayName
        self.Seasons = Seasons
        self.Fruit = Fruit
        self.Texture = Texture
        self.TextureSpriteRow = TextureSpriteRow
        self.PlantableLocationRules = PlantableLocationRules
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "DisplayName": self.DisplayName,
            "Seasons": self.Seasons,
            "Fruit": self.Fruit,
            "Texture": self.Texture,
            "TextureSpriteRow": self.TextureSpriteRow,
            "PlantableLocationRules": self.PlantableLocationRules,
            "CustomFields": self.CustomFields
        }
