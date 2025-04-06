from .model import modelsData

class AnimationDescriptionsData(modelsData):
    def __init__(self, key: str, value: str):
        super().__init__(key)
        self.value = value

    def getJson(self) -> str:
        return self.value
