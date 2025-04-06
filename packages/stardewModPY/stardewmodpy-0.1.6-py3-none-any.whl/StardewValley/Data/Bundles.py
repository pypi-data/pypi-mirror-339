from .model import modelsData


class BundlesData(modelsData):
    def __init__(
        self, 
        key: str,
        bundle_name: str,
        reward: str,
        requirements: list[str],
        color: int,
        item_count: int,
        display_name: str
    ):
        super().__init__(key)
        self.bundle_name = bundle_name
        self.reward = reward
        self.requirements = requirements
        self.color = color
        self.item_count = item_count
        self.display_name = display_name


    def getJson(self) -> str:
        return f"{self.bundle_name}/{self.reward}/{self.requirements}/{self.color}/{self.item_count}//{self.display_name}"
