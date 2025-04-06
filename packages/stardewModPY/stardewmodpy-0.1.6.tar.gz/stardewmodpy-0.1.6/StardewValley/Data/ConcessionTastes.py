from .model import modelsData


class ConcessionTastesData(modelsData):
    def __init__(
        self, 
        key: str,
        Name: str,
        LovedTags: list[str],
        LikedTags: list[str],
        DislikedTags: list[str]
    ):
        super().__init__(key)
        self.Name = Name
        self.LovedTags = LovedTags
        self.LikedTags = LikedTags
        self.DislikedTags = DislikedTags


    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "LovedTags": self.LovedTags,
            "LikedTags": self.LikedTags,
            "DislikedTags": self.DislikedTags
        }
