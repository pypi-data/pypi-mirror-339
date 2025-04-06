from typing import Optional, List
from .model import modelsData

class BigCraftablesData(modelsData):
    def __init__(self,
        key: str,
        Name: str,
        DisplayName: str,
        Description: str,
        Price: int,
        Fragility: int,
        CanBePlacedOutdoors: bool = False,
        CanBePlacedIndoors: bool = False,
        IsLamp: bool = False, 
        Texture: bool = False,
        SpriteIndex: bool = False, 
        ContextTags: Optional[List[str]] = [],
        CustomFields: Optional[dict[str,str]] = None
    ):
        super().__init__(key)
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Price = Price
        self.Fragility = Fragility
        self.CanBePlacedOutdoors = CanBePlacedOutdoors
        self.CanBePlacedIndoors = CanBePlacedIndoors
        self.IsLamp = IsLamp
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.ContextTags = ContextTags if ContextTags is not None else []  # Evita mutabilidade de listas padrão
        self.CustomFields = CustomFields
    
    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "Price": self.Price,
            "Fragility": self.Fragility,
            "CanBePlacedOutdoors": self.CanBePlacedOutdoors,
            "CanBePlacedIndoors": self.CanBePlacedIndoors,
            "IsLamp": self.IsLamp,
            "Texture": self.Texture,
            "SpriteIndex": self.SpriteIndex,
            "ContextTags": self.ContextTags,
            "CustomFields": self.CustomFields
        }
