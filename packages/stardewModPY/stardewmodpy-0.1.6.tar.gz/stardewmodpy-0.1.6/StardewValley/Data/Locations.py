from .model import modelsData
from typing import Optional, Any


class LocationsData(modelsData):
    def __init__(
        self,
        key:str,
        DisplayName: Optional[str] = None,
        DefaultArrivalTile: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        CreateOnLoad: Optional[dict[str, Any]] = None,
        CanPlantHere: Optional[bool] = None,
        CanHaveGreenRainSpawns: Optional[bool] = True,
        ExcludeFromNpcPathfinding: Optional[bool] = False,
        ArtifactSpots: Optional[list[dict[str, Any]]] = [],
        FishAreas: Optional[dict[str, dict[str, Any]]] = {},
        Fish: Optional[list[dict[str, Any]]] = [],
        Forage: Optional[list[dict[str, Any]]] = [],
        MinDailyWeeds: Optional[int] = 1,
        MaxDailyWeeds: Optional[int] = 5,
        FirstDayWeedMultiplier: Optional[int] = 15,
        MinDailyForageSpawn: Optional[int] = 1,
        MaxDailyForageSpawn: Optional[int] = 4,
        MaxSpawnedForageAtOnce: Optional[int] = 6,
        ChanceForClay: Optional[float] = 0.03,
        Music: Optional[list[dict[str, str]]] = [],
        MusicDefault: Optional[str] = None,
        MusicContext: Optional[str] = "Default",
        MusicIgnoredInRain: Optional[bool] = False,
        MusicIgnoredInSpring: Optional[bool] = False,
        MusicIgnoredInSummer: Optional[bool] = False,
        MusicIgnoredInFall: Optional[bool] = False,
        MusicIgnoredInWinter: Optional[bool] = False,
        MusicIgnoredInFallDebris: Optional[bool] = False,
        MusicIsTownTheme: Optional[bool] = False,
        CustomFields: Optional[Any] = None,
        FormerLocationNames: Optional[list[Any]] = []
        ):
        super().__init__(key)
        self.DisplayName = DisplayName
        self.DefaultArrivalTile = DefaultArrivalTile
        self.CreateOnLoad = CreateOnLoad
        self.CanPlantHere = CanPlantHere
        self.CanHaveGreenRainSpawns = CanHaveGreenRainSpawns
        self.ExcludeFromNpcPathfinding = ExcludeFromNpcPathfinding
        self.ArtifactSpots = ArtifactSpots
        self.FishAreas = FishAreas
        self.Fish = Fish
        self.Forage = Forage
        self.MinDailyWeeds = MinDailyWeeds
        self.MaxDailyWeeds = MaxDailyWeeds
        self.FirstDayWeedMultiplier = FirstDayWeedMultiplier
        self.MinDailyForageSpawn = MinDailyForageSpawn
        self.MaxDailyForageSpawn = MaxDailyForageSpawn
        self.MaxSpawnedForageAtOnce = MaxSpawnedForageAtOnce
        self.ChanceForClay = ChanceForClay
        self.Music = Music
        self.MusicDefault = MusicDefault
        self.MusicContext = MusicContext
        self.MusicIgnoredInRain = MusicIgnoredInRain
        self.MusicIgnoredInSpring = MusicIgnoredInSpring
        self.MusicIgnoredInSummer = MusicIgnoredInSummer
        self.MusicIgnoredInFall = MusicIgnoredInFall
        self.MusicIgnoredInWinter = MusicIgnoredInWinter
        self.MusicIgnoredInFallDebris = MusicIgnoredInFallDebris
        self.MusicIsTownTheme = MusicIsTownTheme
        self.CustomFields = CustomFields
        self.FormerLocationNames = FormerLocationNames


    def getJson(self) -> dict:
        return {
            "DisplayName": self.DisplayName,
            "DefaultArrivalTile": self.DefaultArrivalTile,
            "CreateOnLoad": self.CreateOnLoad,
            "CanPlantHere": self.CanPlantHere,
            "CanHaveGreenRainSpawns": self.CanHaveGreenRainSpawns,
            "ExcludeFromNpcPathfinding": self.ExcludeFromNpcPathfinding,
            "ArtifactSpots": self.ArtifactSpots,
            "FishAreas": self.FishAreas,
            "Fish": self.Fish,
            "Forage": self.Forage,
            "MinDailyWeeds": self.MinDailyWeeds,
            "MaxDailyWeeds": self.MaxDailyWeeds,
            "FirstDayWeedMultiplier": self.FirstDayWeedMultiplier,
            "MinDailyForageSpawn": self.MinDailyForageSpawn,
            "MaxDailyForageSpawn": self.MaxDailyForageSpawn,
            "MaxSpawnedForageAtOnce": self.MaxSpawnedForageAtOnce,
            "ChanceForClay": self.ChanceForClay,
            "Music": self.Music,
            "MusicDefault": self.MusicDefault,
            "MusicContext": self.MusicContext,
            "MusicIgnoredInRain": self.MusicIgnoredInRain,
            "MusicIgnoredInSpring": self.MusicIgnoredInSpring,
            "MusicIgnoredInSummer": self.MusicIgnoredInSummer,
            "MusicIgnoredInFall": self.MusicIgnoredInFall,
            "MusicIgnoredInWinter": self.MusicIgnoredInWinter,
            "MusicIgnoredInFallDebris": self.MusicIgnoredInFallDebris,
            "MusicIsTownTheme": self.MusicIsTownTheme,
            "CustomFields": self.CustomFields,
            "FormerLocationNames": self.FormerLocationNames
        }