from .model import modelsData
from typing import Optional, Any


class GiftData(modelsData):
    def __init__(
        self,
        Id: str,
        ItemId: str,
        RandomItemId: Optional[list[str]] = None,
        Condition: Optional[str] = None,
        PerItemCondition: Optional[str] = None,
        MaxItems: Optional[Any] = None,
        IsRecipe: Optional[bool] = False,
        Quality: Optional[int] = -1,
        MinStack: Optional[int] = -1,
        MaxStack: Optional[int] = -1,
        ObjectInternalName: Optional[str] = None,
        ObjectDisplayName: Optional[str] = None,
        ToolUpgradeLevel: Optional[int] = -1,
        QualityModifiers: Optional[Any] = None,
        StackModifiers: Optional[Any] = None,
        QualityModifierMode: Optional[str] = "Stack",
        StackModifierMode: Optional[str] = "Stack",
        MinimumFriendshipThreshold: Optional[int] = 1000,
        Weight: Optional[float] = 1.0,
        ModData: Optional[dict[str, str]] = None
    ):
        super().__init__(None)
        self.Id = Id
        self.ItemId = ItemId
        self.RandomItemId = RandomItemId
        self.Condition = Condition
        self.PerItemCondition = PerItemCondition
        self.MaxItems = MaxItems
        self.IsRecipe = IsRecipe
        self.Quality = Quality
        self.MinStack = MinStack
        self.MaxStack = MaxStack
        self.ObjectInternalName = ObjectInternalName
        self.ObjectDisplayName = ObjectDisplayName
        self.ToolUpgradeLevel = ToolUpgradeLevel
        self.QualityModifiers = QualityModifiers
        self.StackModifiers = StackModifiers
        self.QualityModifierMode = QualityModifierMode
        self.StackModifierMode = StackModifierMode
        self.MinimumFriendshipThreshold = MinimumFriendshipThreshold
        self.Weight = Weight
        self.ModData = ModData


    def getJson(self) -> dict:
        return {
            "Id": self.Id,
            "ItemId": self.ItemId,
            "RandomItemId": self.RandomItemId,
            "Condition": self.Condition,
            "PerItemCondition": self.PerItemCondition,
            "MaxItems": self.MaxItems,
            "IsRecipe": self.IsRecipe,
            "Quality": self.Quality,
            "MinStack": self.MinStack,
            "MaxStack": self.MaxStack,
            "ObjectInternalName": self.ObjectInternalName,
            "ObjectDisplayName": self.ObjectDisplayName,
            "ToolUpgradeLevel": self.ToolUpgradeLevel,
            "QualityModifiers": self.QualityModifiers,
            "StackModifiers": self.StackModifiers,
            "QualityModifierMode": self.QualityModifierMode,
            "StackModifierMode": self.StackModifierMode,
            "MinimumFriendshipThreshold": self.MinimumFriendshipThreshold,
            "Weight": self.Weight,
            "ModData": self.ModData
        }


class BreedsData(modelsData):
    def __init__(
        self,
        Id: str,
        Texture: str,
        IconTexture: str,
        IconSourceRect: dict[str, int],
        CanBeChosenAtStart: Optional[bool] = True,
        CanBeAdoptedFromMarnie: Optional[bool] = True,
        AdoptionPrice: Optional[int] = 40000,
        BarkOverride: Optional[Any] = None,
        VoicePitch: Optional[float] = 1.0
    ):
        super().__init__(None)
        self.Id = Id
        self.Texture = Texture
        self.IconTexture = IconTexture
        self.IconSourceRect = IconSourceRect
        self.CanBeChosenAtStart = CanBeChosenAtStart
        self.CanBeAdoptedFromMarnie = CanBeAdoptedFromMarnie
        self.AdoptionPrice = AdoptionPrice
        self.BarkOverride = BarkOverride
        self.VoicePitch = VoicePitch


    def getJson(self) -> dict:
        return {
            "Id": self.Id,
            "Texture": self.Texture,
            "IconTexture": self.IconTexture,
            "IconSourceRect": self.IconSourceRect,
            "CanBeChosenAtStart": self.CanBeChosenAtStart,
            "CanBeAdoptedFromMarnie": self.CanBeAdoptedFromMarnie,
            "AdoptionPrice": self.AdoptionPrice,
            "BarkOverride": self.BarkOverride,
            "VoicePitch": self.VoicePitch
        }


class PetsData(modelsData):
    def __init__(
        self,
        key: str,
        DisplayName: str,
        BarkSound: str,
        ContentSound: str,
        Breeds: list[BreedsData],
        RepeatContentSoundAfter: Optional[int] = -1,
        EmoteOffset: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        EventOffset: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        AdoptionEventLocation: Optional[str] = "Farm",
        AdoptionEventId: Optional[str] = None,
        SummitPerfectionEvent: Optional[dict[str, Any]] = None,
        GiftChance: Optional[float] = 0.2,
        Gifts: Optional[list[GiftData]] = None,
        CustomFields: Optional[Any] = None

    ):
        super().__init__(key)
        self.DisplayName = DisplayName
        self.BarkSound = BarkSound
        self.ContentSound = ContentSound
        self.Breeds = Breeds
        self.RepeatContentSoundAfter = RepeatContentSoundAfter
        self.EmoteOffset = EmoteOffset
        self.EventOffset = EventOffset
        self.AdoptionEventLocation = AdoptionEventLocation
        self.AdoptionEventId = AdoptionEventId
        self.SummitPerfectionEvent = SummitPerfectionEvent
        self.GiftChance = GiftChance
        self.Gifts = Gifts
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "DisplayName": self.DisplayName,
            "BarkSound": self.BarkSound,
            "ContentSound": self.ContentSound,
            "Breeds": [b.getJson() for b in self.Breeds],
            "RepeatContentSoundAfter": self.RepeatContentSoundAfter,
            "EmoteOffset": self.EmoteOffset,
            "EventOffset": self.EventOffset,
            "AdoptionEventLocation": self.AdoptionEventLocation,
            "AdoptionEventId": self.AdoptionEventId,
            "SummitPerfectionEvent": self.SummitPerfectionEvent,
            "GiftChance": self.GiftChance,
            "Gifts": [g.getJson() for g in self.Gifts] if self.Gifts else None,
            "CustomFields": self.CustomFields
        }
