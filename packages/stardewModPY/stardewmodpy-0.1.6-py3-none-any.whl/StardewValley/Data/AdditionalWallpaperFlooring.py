from .model import modelsData
import json

class AdditionalWallpaperFlooringData(modelsData):
    def __init__(self, key: str, Id: str, Texture: str, IsFlooring: bool, Count: int):
        super().__init__(key)
        self.Id = Id
        self.Texture = Texture
        self.IsFlooring = IsFlooring
        self.Count = Count

    def getJson(self) -> dict:
        return {
            'Id': self.Id,
            'Texture': self.Texture,
            'IsFlooring': self.IsFlooring,
            'Count': self.Count
        }
