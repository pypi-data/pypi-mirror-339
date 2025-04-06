from .model import modelsData
from typing import Optional, Any


class FishPondsData(modelsData):
    def __init__(
        self,
        key: str,
        Id: str,
        RequiredTags: list[str],
        ProducedItems: list[dict[str, Any]],
        PopulationGates: dict[str, list[str]],
        MaxPopulation: Optional[int] = -1,
        Precedence: Optional[int] = 0,
        SpawnTime: Optional[int] = -1,
        WaterColor: Optional[list[dict[str, Any]]] = None
    ):
        super().__init__(key)
        self.Id = Id
        self.RequiredTags = RequiredTags
        self.ProducedItems = ProducedItems
        self.PopulationGates = PopulationGates
        self.MaxPopulation = MaxPopulation
        self.Precedence = Precedence
        self.SpawnTime = SpawnTime
        self.WaterColor = WaterColor


    def getJson(self) -> dict:
        return {
            "Id": self.Id,
            "RequiredTags": self.RequiredTags,
            "ProducedItems": self.ProducedItems,
            "PopulationGates": self.PopulationGates,
            "MaxPopulation": self.MaxPopulation,
            "Precedence": self.Precedence,
            "SpawnTime": self.SpawnTime,
            "WaterColor": self.WaterColor
        }
