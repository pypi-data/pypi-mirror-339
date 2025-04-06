from typing import Optional, List, Dict, Any
from .model import modelsData

class BuildingsData(modelsData):
    def __init__(self, key: str, Name: str, Description: str, Texture: str, 
                 NameForGeneralType: Optional[str] = None, 
                 Skins: List[str] = [], DrawShadow: bool = True, UpgradeSignTile: str = "-1, -1",
                 UpgradeSignHeight: float = 0.0, Size: Dict[str, int] = {'X': 3, 'Y': 2}, FadeWhenBehind: bool = True,
                 SourceRect: Dict[str, int] = {'X': 0, 'Y': 0, 'Width': 0, 'Height': 0}, 
                 SeasonOffset: Dict[str, int] = {'X': 0, 'Y': 0}, DrawOffset: str = "0, 0", 
                 SortTileOffset: float = 0.0, CollisionMap: Optional[str] = None, 
                 AdditionalPlacementTiles: Optional[str] = None, BuildingType: str = "StardewValley.Buildings.JunimoHut",
                 Builder: str = "Wizard", BuildCondition: Optional[str] = None, BuildDays: int = 0, 
                 BuildCost: int = 20000, BuildMaterials: List[Dict[str, str]] = None, 
                 BuildingToUpgrade: Optional[str] = None, MagicalConstruction: bool = True, 
                 BuildMenuDrawOffset: Dict[str, int] = {'X': 0, 'Y': 0}, HumanDoor: Dict[str, int] = {'X': -1, 'Y': -1}, 
                 AnimalDoor: Dict[str, int] = {'X': -1, 'Y': -1, 'Width': 0, 'Height': 0}, 
                 AnimalDoorOpenDuration: float = 0.0, AnimalDoorOpenSound: Optional[str] = None, 
                 AnimalDoorCloseDuration: float = 0.0, AnimalDoorCloseSound: Optional[str] = None, 
                 NonInstancedIndoorLocation: Optional[str] = None, IndoorMap: Optional[str] = None, 
                 IndoorMapType: Optional[str] = None, MaxOccupants: int = 20, 
                 ValidOccupantTypes: List[str] = [], AllowAnimalPregnancy: bool = False, 
                 IndoorItemMoves: Optional[str] = None, IndoorItems: Optional[str] = None, 
                 AddMailOnBuild: Optional[str] = None, Metadata: Dict = {}, ModData: Dict = {}, 
                 HayCapacity: int = 0, Chests: List[Dict[str, Any]] = None, DefaultAction: Optional[str] = None, 
                 AdditionalTilePropertyRadius: int = 0, AllowsFlooringUnderneath: bool = True, 
                 ActionTiles: List[str] = [], TileProperties: List[str] = [], ItemConversions: Optional[str] = None, 
                 DrawLayers: Optional[str] = None, CustomFields: Optional[str] = None):
        super().__init__(key)
        self.Name = Name
        self.NameForGeneralType = NameForGeneralType
        self.Description = Description
        self.Texture = Texture
        self.Skins = Skins
        self.DrawShadow = DrawShadow
        self.UpgradeSignTile = UpgradeSignTile
        self.UpgradeSignHeight = UpgradeSignHeight
        self.Size = Size
        self.FadeWhenBehind = FadeWhenBehind
        self.SourceRect = SourceRect
        self.SeasonOffset = SeasonOffset
        self.DrawOffset = DrawOffset
        self.SortTileOffset = SortTileOffset
        self.CollisionMap = CollisionMap
        self.AdditionalPlacementTiles = AdditionalPlacementTiles
        self.BuildingType = BuildingType
        self.Builder = Builder
        self.BuildCondition = BuildCondition
        self.BuildDays = BuildDays
        self.BuildCost = BuildCost
        self.BuildMaterials = BuildMaterials if BuildMaterials else []
        self.BuildingToUpgrade = BuildingToUpgrade
        self.MagicalConstruction = MagicalConstruction
        self.BuildMenuDrawOffset = BuildMenuDrawOffset
        self.HumanDoor = HumanDoor
        self.AnimalDoor = AnimalDoor
        self.AnimalDoorOpenDuration = AnimalDoorOpenDuration
        self.AnimalDoorOpenSound = AnimalDoorOpenSound
        self.AnimalDoorCloseDuration = AnimalDoorCloseDuration
        self.AnimalDoorCloseSound = AnimalDoorCloseSound
        self.NonInstancedIndoorLocation = NonInstancedIndoorLocation
        self.IndoorMap = IndoorMap
        self.IndoorMapType = IndoorMapType
        self.MaxOccupants = MaxOccupants
        self.ValidOccupantTypes = ValidOccupantTypes
        self.AllowAnimalPregnancy = AllowAnimalPregnancy
        self.IndoorItemMoves = IndoorItemMoves
        self.IndoorItems = IndoorItems
        self.AddMailOnBuild = AddMailOnBuild
        self.Metadata = Metadata
        self.ModData = ModData
        self.HayCapacity = HayCapacity
        self.Chests = Chests if Chests else []
        self.DefaultAction = DefaultAction
        self.AdditionalTilePropertyRadius = AdditionalTilePropertyRadius
        self.AllowsFlooringUnderneath = AllowsFlooringUnderneath
        self.ActionTiles = ActionTiles
        self.TileProperties = TileProperties
        self.ItemConversions = ItemConversions
        self.DrawLayers = DrawLayers
        self.CustomFields = CustomFields

    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "NameForGeneralType": self.NameForGeneralType,
            "Description": self.Description,
            "Texture": self.Texture,
            "Skins": self.Skins,
            "DrawShadow": self.DrawShadow,
            "UpgradeSignTile": self.UpgradeSignTile,
            "UpgradeSignHeight": self.UpgradeSignHeight,
            "Size": self.Size,
            "FadeWhenBehind": self.FadeWhenBehind,
            "SourceRect": self.SourceRect,
            "SeasonOffset": self.SeasonOffset,
            "DrawOffset": self.DrawOffset,
            "SortTileOffset": self.SortTileOffset,
            "CollisionMap": self.CollisionMap,
            "AdditionalPlacementTiles": self.AdditionalPlacementTiles,
            "BuildingType": self.BuildingType,
            "Builder": self.Builder,
            "BuildCondition": self.BuildCondition,
            "BuildDays": self.BuildDays,
            "BuildCost": self.BuildCost,
            "BuildMaterials": self.BuildMaterials,
            "BuildingToUpgrade": self.BuildingToUpgrade,
            "MagicalConstruction": self.MagicalConstruction,
            "BuildMenuDrawOffset": self.BuildMenuDrawOffset,
            "HumanDoor": self.HumanDoor,
            "AnimalDoor": self.AnimalDoor,
            "AnimalDoorOpenDuration": self.AnimalDoorOpenDuration,
            "AnimalDoorOpenSound": self.AnimalDoorOpenSound,
            "AnimalDoorCloseDuration": self.AnimalDoorCloseDuration,
            "AnimalDoorCloseSound": self.AnimalDoorCloseSound,
            "NonInstancedIndoorLocation": self.NonInstancedIndoorLocation,
            "IndoorMap": self.IndoorMap,
            "IndoorMapType": self.IndoorMapType,
            "MaxOccupants": self.MaxOccupants,
            "ValidOccupantTypes": self.ValidOccupantTypes,
            "AllowAnimalPregnancy": self.AllowAnimalPregnancy,
            "IndoorItemMoves": self.IndoorItemMoves,
            "IndoorItems": self.IndoorItems,
            "AddMailOnBuild": self.AddMailOnBuild,
            "Metadata": self.Metadata,
            "ModData": self.ModData,
            "HayCapacity": self.HayCapacity,
            "Chests": self.Chests,
            "DefaultAction": self.DefaultAction,
            "AdditionalTilePropertyRadius": self.AdditionalTilePropertyRadius,
            "AllowsFlooringUnderneath": self.AllowsFlooringUnderneath,
            "ActionTiles": self.ActionTiles,
            "TileProperties": self.TileProperties,
            "ItemConversions": self.ItemConversions,
            "DrawLayers": self.DrawLayers,
            "CustomFields": self.CustomFields
        }
