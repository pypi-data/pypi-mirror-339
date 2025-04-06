from .model import modelsData
from typing import Optional, Any


class CropsData(modelsData):
    def __init__(
        self, 
        key: str,
        Seasons: list[str],
        DaysInPhase: list[int],
        HarvestItemId: str,
        Texture: str,
        RegrowDays: Optional[int] = -1,
        IsRaised: Optional[bool] = False,
        IsPaddyCrop: Optional[bool] = False,
        NeedsWatering: Optional[bool] = True,
        HarvestMethod: Optional[str] = "Grab",
        HarvestMinQuality: Optional[int] = 0,
        HarvestMaxQuality: Optional[int] = None,
        HarvestMaxIncreasePerFarmingLevel: Optional[float] = 0.0,
        ExtraHarvestChance: Optional[float] = 0.0,
        SpriteIndex: Optional[int] = 0,
        TintColors: Optional[list[str]] = [],
        CountForMonoculture: Optional[bool] = False,
        CountForPolyculture: Optional[bool] = False,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.Seasons = Seasons
        self.DaysInPhase = DaysInPhase
        self.HarvestItemId = HarvestItemId
        self.Texture = Texture
        self.RegrowDays = RegrowDays
        self.IsRaised = IsRaised
        self.IsPaddyCrop = IsPaddyCrop
        self.NeedsWatering = NeedsWatering
        self.HarvestMethod = HarvestMethod
        self.HarvestMinQuality = HarvestMinQuality
        self.HarvestMaxQuality = HarvestMaxQuality
        self.HarvestMaxIncreasePerFarmingLevel = HarvestMaxIncreasePerFarmingLevel
        self.ExtraHarvestChance = ExtraHarvestChance
        self.SpriteIndex = SpriteIndex
        self.TintColors = TintColors
        self.CountForMonoculture = CountForMonoculture
        self.CountForPolyculture = CountForPolyculture
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "Seasons": self.Seasons,
            "DaysInPhase": self.DaysInPhase,
            "HarvestItemId": self.HarvestItemId,
            "Texture": self.Texture,
            "RegrowDays": self.RegrowDays,
            "IsRaised": self.IsRaised,
            "IsPaddyCrop": self.IsPaddyCrop,
            "NeedsWatering": self.NeedsWatering,
            "HarvestMethod": self.HarvestMethod,
            "HarvestMinQuality": self.HarvestMinQuality,
            "HarvestMaxQuality": self.HarvestMaxQuality,
            "HarvestMaxIncreasePerFarmingLevel": self.HarvestMaxIncreasePerFarmingLevel,
            "ExtraHarvestChance": self.ExtraHarvestChance,
            "SpriteIndex": self.SpriteIndex,
            "TintColors": self.TintColors,
            "CountForMonoculture": self.CountForMonoculture,
            "CountForPolyculture": self.CountForPolyculture,
            "CustomFields": self.CustomFields
        }
