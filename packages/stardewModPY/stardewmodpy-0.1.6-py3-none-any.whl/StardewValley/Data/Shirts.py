from .model import modelsData
from typing import Optional, Any


class ShirtsData(modelsData):
    def __init__(
        self,
        key: str,
        Texture: str,
        Name: Optional[str] = "Shirt",
        DisplayName: Optional[str] = "Shirt",
        Description: Optional[str] = "A wearable shirt",
        Price: Optional[int] = 50,
        SpriteIndex: int = 0,
        DefaultColor: Optional[str] = None,
        CanBeDyed: Optional[bool] = False,
        IsPrismatic: Optional[bool] = False,
        HasSleeves: Optional[bool] = False,
        CanChooseDuringCharacterCustomization: Optional[bool] = False,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.Texture = Texture
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Price = Price
        self.SpriteIndex = SpriteIndex
        self.DefaultColor = DefaultColor
        self.CanBeDyed = CanBeDyed
        self.IsPrismatic = IsPrismatic
        self.HasSleeves = HasSleeves
        self.CanChooseDuringCharacterCustomization = CanChooseDuringCharacterCustomization
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "Texture": self.Texture,
            "Name": self.Name,
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "Price": self.Price,
            "SpriteIndex": self.SpriteIndex,
            "DefaultColor": self.DefaultColor,
            "CanBeDyed": self.CanBeDyed,
            "IsPrismatic": self.IsPrismatic,
            "HasSleeves": self.HasSleeves,
            "CanChooseDuringCharacterCustomization": self.CanChooseDuringCharacterCustomization,
            "CustomFields": self.CustomFields
        }
