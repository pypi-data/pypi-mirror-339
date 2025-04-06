from .model import modelsData
from typing import Optional, Any


class FarmAnimalsData(modelsData):
    def __init__(
        self, 
        key: str,
        DisplayName: str,
        Texture: str,
        House: str,
        Gender: Optional[str] = "Female",
        PurchasePrice: Optional[int] = -1,
        ShopTexture: Optional[str] = None,
        ShopSourceRect: Optional[dict[str, int]] = {"X": 0, "Y": 0, "Width": 0, "Height": 0},
        RequiredBuilding: Optional[str] = None,
        UnlockCondition: Optional[str] = None,
        ShopDisplayName: Optional[str] = None,
        ShopDescription: Optional[str] = None,
        ShopMissingBuildingDescription: Optional[str] = None,
        AlternatePurchaseTypes: Optional[list[dict[str, Any]]] = None,
        EggItemIds: Optional[list[str]] = None,
        IncubationTime: Optional[int] = -1,
        IncubatorParentSheetOffset: Optional[int] = 1,
        BirthText: Optional[str] = None,
        DaysToMature: Optional[int] = 1,
        CanGetPregnant: Optional[bool] = False,
        ProduceItemIds: Optional[list[dict[str, Any]]] = [],
        DeluxeProduceItemIds: Optional[list[dict[str, Any]]] = [],
        DaysToProduce: Optional[int] = 1,
        ProduceOnMature: Optional[bool] = False,
        FriendshipForFasterProduce: Optional[int] = -1,
        DeluxeProduceMinimumFriendship: Optional[int] = 200,
        DeluxeProduceCareDivisor: Optional[float] = 1200.0,
        DeluxeProduceLuckMultiplier: Optional[float] = 0.0,
        HarvestType: Optional[str] = "DropOvernight",
        HarvestTool: Optional[str] = None,
        CanEatGoldenCrackers: Optional[bool] = True,
        Sound: Optional[str] = None,
        BabySound: Optional[str] = None,
        HarvestedTexture: Optional[str] = None,
        BabyTexture: Optional[str] = None,
        UseFlippedRightForLeft: Optional[bool] = False,
        SpriteWidth: Optional[int] = 16,
        SpriteHeight: Optional[int] = 16,
        EmoteOffset: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        SwimOffset: Optional[dict[str, int]] = {"X":0, "Y": 112},
        Skins: Optional[Any] = None,
        SleepFrame: Optional[int] = 12,
        UseDoubleUniqueAnimationFrames: Optional[bool] = False,
        ShadowWhenBaby: Optional[Any] = None,
        ShadowWhenBabySwims: Optional[Any] = None,
        ShadowWhenAdult: Optional[Any] = None,
        ShadowWhenAdultSwims: Optional[Any] = None,
        Shadow: Optional[Any] = None,
        ProfessionForFasterProduce: Optional[int] = None,
        ProfessionForHappinessBoost: Optional[int] = None,
        ProfessionForQualityBoost: Optional[int] = None,
        CanSwim: Optional[bool] = False,
        BabiesFollowAdults: Optional[bool] = False,
        GrassEatAmount: Optional[int] = 2,
        HappinessDrain: Optional[int] = None,
        SellPrice: Optional[int] = 0,
        CustomFields: Optional[Any] = None,
        ShowInSummitCredits: Optional[bool] = False,
        StatToIncrementOnProduce: Optional[list[dict[str, Any]]] = None,
        UpDownPetHitboxTileSize: Optional[str] = "1, 1",
        LeftRightPetHitboxTileSize: Optional[str] = "1, 1",
        BabyUpDownPetHitboxTileSize: Optional[str] = "1, 1",
        BabyLeftRightPetHitboxTileSize: Optional[str] = "1, 1"
    ):
        super().__init__(key)
        self.DisplayName = DisplayName
        self.Texture = Texture
        self.House = House
        self.Gender = Gender
        self.PurchasePrice = PurchasePrice
        self.ShopTexture = ShopTexture
        self.ShopSourceRect = ShopSourceRect
        self.RequiredBuilding = RequiredBuilding
        self.UnlockCondition = UnlockCondition
        self.ShopDisplayName = ShopDisplayName
        self.ShopDescription = ShopDescription
        self.ShopMissingBuildingDescription = ShopMissingBuildingDescription
        self.AlternatePurchaseTypes = AlternatePurchaseTypes
        self.EggItemIds = EggItemIds
        self.IncubationTime = IncubationTime
        self.IncubatorParentSheetOffset = IncubatorParentSheetOffset
        self.BirthText = BirthText
        self.DaysToMature = DaysToMature
        self.CanGetPregnant = CanGetPregnant
        self.ProduceItemIds = ProduceItemIds
        self.DeluxeProduceItemIds = DeluxeProduceItemIds
        self.DaysToProduce = DaysToProduce
        self.ProduceOnMature = ProduceOnMature
        self.FriendshipForFasterProduce = FriendshipForFasterProduce
        self.DeluxeProduceMinimumFriendship = DeluxeProduceMinimumFriendship
        self.DeluxeProduceCareDivisor = DeluxeProduceCareDivisor
        self.DeluxeProduceLuckMultiplier = DeluxeProduceLuckMultiplier
        self.HarvestType = HarvestType
        self.HarvestTool = HarvestTool
        self.CanEatGoldenCrackers = CanEatGoldenCrackers
        self.Sound = Sound
        self.BabySound = BabySound
        self.HarvestedTexture = HarvestedTexture
        self.BabyTexture = BabyTexture
        self.UseFlippedRightForLeft = UseFlippedRightForLeft
        self.SpriteWidth = SpriteWidth
        self.SpriteHeight = SpriteHeight
        self.EmoteOffset = EmoteOffset
        self.SwimOffset = SwimOffset
        self.Skins = Skins
        self.SleepFrame = SleepFrame
        self.UseDoubleUniqueAnimationFrames = UseDoubleUniqueAnimationFrames
        self.ShadowWhenBaby = ShadowWhenBaby
        self.ShadowWhenBabySwims = ShadowWhenBabySwims
        self.ShadowWhenAdult = ShadowWhenAdult
        self.ShadowWhenAdultSwims = ShadowWhenAdultSwims
        self.Shadow = Shadow
        self.ProfessionForFasterProduce = ProfessionForFasterProduce
        self.ProfessionForHappinessBoost = ProfessionForHappinessBoost
        self.ProfessionForQualityBoost = ProfessionForQualityBoost
        self.CanSwim = CanSwim
        self.BabiesFollowAdults = BabiesFollowAdults
        self.GrassEatAmount = GrassEatAmount
        self.HappinessDrain = HappinessDrain
        self.SellPrice = SellPrice
        self.CustomFields = CustomFields
        self.ShowInSummitCredits = ShowInSummitCredits
        self.StatToIncrementOnProduce = StatToIncrementOnProduce
        self.UpDownPetHitboxTileSize = UpDownPetHitboxTileSize
        self.LeftRightPetHitboxTileSize = LeftRightPetHitboxTileSize
        self.BabyUpDownPetHitboxTileSize = BabyUpDownPetHitboxTileSize
        self.BabyLeftRightPetHitboxTileSize = BabyLeftRightPetHitboxTileSize


    def getJson(self) -> dict:
        return {
            "DisplayName": self.DisplayName,
            "Texture": self.Texture,
            "House": self.House,
            "Gender": self.Gender,
            "PurchasePrice": self.PurchasePrice,
            "ShopTexture": self.ShopTexture,
            "ShopSourceRect": self.ShopSourceRect,
            "RequiredBuilding": self.RequiredBuilding,
            "UnlockCondition": self.UnlockCondition,
            "ShopDisplayName": self.ShopDisplayName,
            "ShopDescription": self.ShopDescription,
            "ShopMissingBuildingDescription": self.ShopMissingBuildingDescription,
            "AlternatePurchaseTypes": self.AlternatePurchaseTypes,
            "EggItemIds": self.EggItemIds,
            "IncubationTime": self.IncubationTime,
            "IncubatorParentSheetOffset": self.IncubatorParentSheetOffset,
            "BirthText": self.BirthText,
            "DaysToMature": self.DaysToMature,
            "CanGetPregnant": self.CanGetPregnant,
            "ProduceItemIds": self.ProduceItemIds,
            "DeluxeProduceItemIds": self.DeluxeProduceItemIds,
            "DaysToProduce": self.DaysToProduce,
            "ProduceOnMature": self.ProduceOnMature,
            "FriendshipForFasterProduce": self.FriendshipForFasterProduce,
            "DeluxeProduceMinimumFriendship": self.DeluxeProduceMinimumFriendship,
            "DeluxeProduceCareDivisor": self.DeluxeProduceCareDivisor,
            "DeluxeProduceLuckMultiplier": self.DeluxeProduceLuckMultiplier,
            "HarvestType": self.HarvestType,
            "HarvestTool": self.HarvestTool,
            "CanEatGoldenCrackers": self.CanEatGoldenCrackers,
            "Sound": self.Sound,
            "BabySound": self.BabySound,
            "HarvestedTexture": self.HarvestedTexture,
            "BabyTexture": self.BabyTexture,
            "UseFlippedRightForLeft": self.UseFlippedRightForLeft,
            "SpriteWidth": self.SpriteWidth,
            "SpriteHeight": self.SpriteHeight,
            "EmoteOffset": self.EmoteOffset,
            "SwimOffset": self.SwimOffset,
            "Skins": self.Skins,
            "SleepFrame": self.SleepFrame,
            "UseDoubleUniqueAnimationFrames": self.UseDoubleUniqueAnimationFrames,
            "ShadowWhenBaby": self.ShadowWhenBaby,
            "ShadowWhenBabySwims": self.ShadowWhenBabySwims,
            "ShadowWhenAdult": self.ShadowWhenAdult,
            "ShadowWhenAdultSwims": self.ShadowWhenAdultSwims,
            "Shadow": self.Shadow,
            "ProfessionForFasterProduce": self.ProfessionForFasterProduce,
            "ProfessionForHappinessBoost": self.ProfessionForHappinessBoost,
            "ProfessionForQualityBoost": self.ProfessionForQualityBoost,
            "CanSwim": self.CanSwim,
            "BabiesFollowAdults": self.BabiesFollowAdults,
            "GrassEatAmount": self.GrassEatAmount,
            "HappinessDrain": self.HappinessDrain,
            "SellPrice": self.SellPrice,
            "CustomFields": self.CustomFields,
            "ShowInSummitCredits": self.ShowInSummitCredits,
            "StatToIncrementOnProduce": self.StatToIncrementOnProduce,
            "UpDownPetHitboxTileSize": self.UpDownPetHitboxTileSize,
            "LeftRightPetHitboxTileSize": self.LeftRightPetHitboxTileSize,
            "BabyUpDownPetHitboxTileSize": self.BabyUpDownPetHitboxTileSize,
            "BabyLeftRightPetHitboxTileSize": self.BabyLeftRightPetHitboxTileSize
        }
