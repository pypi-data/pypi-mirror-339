from .model import modelsData


class RandomBundleData(modelsData):
    def __init__(
        self,
        Name: str,
        Index: int,
        Sprite: str,
        Color: str,
        Items: str,
        Pick: int,
        Reward: str,
        RequiredItems: int = -1
    ):
        super().__init__(None)
        self.Name = Name
        self.Index = Index
        self.Sprite = Sprite
        self.Color = Color
        self.Items = Items
        self.Pick = Pick
        self.Reward = Reward
        self.RequiredItems = RequiredItems


    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "Index": self.Index,
            "Sprite": self.Sprite,
            "Color": self.Color,
            "Items": self.Items,
            "Pick": self.Pick,
            "Reward": self.Reward,
            "RequiredItems": self.RequiredItems
        }


class BundleSetsData(modelsData):
    def __init__(
        self,
        Id: str,
        Bundles: list[RandomBundleData]
    ):
        super().__init__(None)
        self.Id = Id
        self.Bundles = Bundles


    def getJson(self) -> dict:
        return {
            "Id": self.Id,
            "Bundles": [b.getJson() for b in self.Bundles]
        }


class RandomBundlesData(modelsData):
    def __init__(
        self,
        AreaName: str,
        Keys: str,
        BundleSets: list[BundleSetsData],
        Bundles: list[RandomBundleData]
    ):
        super().__init__(None)
        self.AreaName = AreaName
        self.Keys = Keys
        self.BundleSets = BundleSets
        self.Bundles = Bundles


    def getJson(self) -> dict:
        return {
            "AreaName": self.AreaName,
            "Keys": self.Keys,
            "BundleSets": [bundle_set.getJson() for bundle_set in self.BundleSets],
            "Bundles": [bundle.getJson() for bundle in self.Bundles]
        }
