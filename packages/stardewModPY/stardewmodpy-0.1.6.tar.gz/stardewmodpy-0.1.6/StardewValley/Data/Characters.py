from .model import modelsData
from typing import Optional, Any


class CharactersData(modelsData):
    def __init__(
        self, 
        key: str,
        DisplayName: str,
        BirthSeason: str,
        BirthDay: int,
        HomeRegion: str,
        Language: Optional[str] = "Default",
        Gender: Optional[str] = "Undefined",
        Age: Optional[str] = "Adult",
        Manner: Optional[str] = "Neutral",
        SocialAnxiety: Optional[str] = "Neutral",
        Optimism: Optional[str] = "Neutral",
        IsDarkSkinned: Optional[bool] = False,
        CanBeRomanced: Optional[bool] = False,
        LoveInterest: Optional[str] = "",
        Calendar: Optional[str] = "AlwaysShown",
        SocialTab: Optional[str] = "UnknownUntilMet",
        CanSocialize: Optional[str] = None,
        CanReceiveGifts: Optional[bool] = True,
        CanGreetNearbyCharacters: Optional[bool] = True,
        CanCommentOnPurchasedShopItems: Optional[Any] = None,
        CanVisitIsland: Optional[str] = None,
        IntroductionsQuest: Optional[bool] = None,
        ItemDeliveryQuests: Optional[str] = None,
        PerfectionScore: Optional[bool] = True,
        EndSlideShow: Optional[str] = "MainGroup",
        SpouseAdopts: Optional[Any] = None,
        SpouseWantsChildren: Optional[Any] = None,
        SpouseGiftJealousy: Optional[Any] = None,
        SpouseGiftJealousyFriendshipChange: Optional[int] = -30,
        SpouseRoom: Optional[dict[str, Any]] = None,
        SpousePatio: Optional[dict[str, Any]] = None,
        SpouseFloors: Optional[list] = [],
        SpouseWallpapers: list[str] = [],
        DumpsterDiveFriendshipEffect: Optional[int] = -25,
        DumpsterDiveEmote: Optional[int] = None,
        FriendsAndFamily: Optional[dict[str, str]] = {},
        FlowerDanceCanDance: Optional[Any] = None,
        WinterStarGifts: Optional[list[dict[str, Any]]] = [],
        WinterStarParticipant: Optional[str] = None,
        UnlockConditions: Optional[str] = None,
        SpawnIfMissing: Optional[bool] = True,
        Home: Optional[list[dict[str, Any]]] = None,
        TextureName: Optional[str] = None,
        Appearance: Optional[list[dict[str, Any]]] = [],
        MugShotSourceRect: Optional[Any] = None,
        Size: Optional[dict[str, int]] = {"X": 16, "Y": 32},
        Breather: Optional[bool] = True,
        BreathChestRect: Optional[Any] = None,
        BreathChestPosition: Optional[Any] = None,
        Shadow: Optional[Any] = None,
        EmoteOffset: Optional[dict[str, int]] = {"X": 0, "Y": 0},
        ShakePortraits: Optional[list[int]] = [],
        KissSpriteIndex: Optional[int] = 28,
        KissSpriteFacingRight: Optional[bool] = True,
        HiddenProfileEmoteSound: Optional[str] = None,
        HiddenProfileEmoteDuration: Optional[int] = -1,
        HiddenProfileEmoteStartFrame: Optional[int] = -1,
        HiddenProfileEmoteFrameCount: Optional[int] = 1,
        HiddenProfileEmoteFrameDuration: Optional[float] = 200.0,
        FormerCharacterNames: Optional[list[str]] = [],
        FestivalVanillaActorIndex: Optional[int] = -1,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.DisplayName = DisplayName
        self.BirthSeason = BirthSeason
        self.BirthDay = BirthDay
        self.HomeRegion = HomeRegion
        self.Language = Language
        self.Gender = Gender
        self.Age = Age
        self.Manner = Manner
        self.SocialAnxiety = SocialAnxiety
        self.Optimism = Optimism
        self.IsDarkSkinned = IsDarkSkinned
        self.CanBeRomanced = CanBeRomanced
        self.LoveInterest = LoveInterest
        self.Calendar = Calendar
        self.SocialTab = SocialTab
        self.CanSocialize = CanSocialize
        self.CanReceiveGifts = CanReceiveGifts
        self.CanGreetNearbyCharacters = CanGreetNearbyCharacters
        self.CanCommentOnPurchasedShopItems = CanCommentOnPurchasedShopItems
        self.CanVisitIsland = CanVisitIsland
        self.IntroductionsQuest = IntroductionsQuest
        self.ItemDeliveryQuests = ItemDeliveryQuests
        self.PerfectionScore = PerfectionScore
        self.EndSlideShow = EndSlideShow
        self.SpouseAdopts = SpouseAdopts
        self.SpouseWantsChildren = SpouseWantsChildren
        self.SpouseGiftJealousy = SpouseGiftJealousy
        self.SpouseGiftJealousyFriendshipChange = SpouseGiftJealousyFriendshipChange
        self.SpouseRoom = SpouseRoom
        self.SpousePatio = SpousePatio
        self.SpouseFloors = SpouseFloors
        self.SpouseWallpapers = SpouseWallpapers
        self.DumpsterDiveFriendshipEffect = DumpsterDiveFriendshipEffect
        self.DumpsterDiveEmote = DumpsterDiveEmote
        self.FriendsAndFamily = FriendsAndFamily
        self.FlowerDanceCanDance = FlowerDanceCanDance
        self.WinterStarGifts = WinterStarGifts
        self.WinterStarParticipant = WinterStarParticipant
        self.UnlockConditions = UnlockConditions
        self.SpawnIfMissing = SpawnIfMissing
        self.Home = Home
        self.TextureName = TextureName
        self.Appearance = Appearance
        self.MugShotSourceRect = MugShotSourceRect
        self.Size = Size
        self.Breather = Breather
        self.BreathChestRect = BreathChestRect
        self.BreathChestPosition = BreathChestPosition
        self.Shadow = Shadow
        self.EmoteOffset = EmoteOffset
        self.ShakePortraits = ShakePortraits
        self.KissSpriteIndex = KissSpriteIndex
        self.KissSpriteFacingRight = KissSpriteFacingRight
        self.HiddenProfileEmoteSound = HiddenProfileEmoteSound
        self.HiddenProfileEmoteDuration = HiddenProfileEmoteDuration
        self.HiddenProfileEmoteStartFrame = HiddenProfileEmoteStartFrame
        self.HiddenProfileEmoteFrameCount = HiddenProfileEmoteFrameCount
        self.HiddenProfileEmoteFrameDuration = HiddenProfileEmoteFrameDuration
        self.FormerCharacterNames = FormerCharacterNames
        self.FestivalVanillaActorIndex = FestivalVanillaActorIndex
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "DisplayName": self.DisplayName,
            "BirthSeason": self.BirthSeason,
            "BirthDay": self.BirthDay,
            "HomeRegion": self.HomeRegion,
            "Language": self.Language,
            "Gender": self.Gender,
            "Age": self.Age,
            "Manner": self.Manner,
            "SocialAnxiety": self.SocialAnxiety,
            "Optimism": self.Optimism,
            "IsDarkSkinned": self.IsDarkSkinned,
            "CanBeRomanced": self.CanBeRomanced,
            "LoveInterest": self.LoveInterest,
            "Calendar": self.Calendar,
            "SocialTab": self.SocialTab,
            "CanSocialize": self.CanSocialize,
            "CanReceiveGifts": self.CanReceiveGifts,
            "CanGreetNearbyCharacters": self.CanGreetNearbyCharacters,
            "CanCommentOnPurchasedShopItems": self.CanCommentOnPurchasedShopItems,
            "CanVisitIsland": self.CanVisitIsland,
            "IntroductionsQuest": self.IntroductionsQuest,
            "ItemDeliveryQuests": self.ItemDeliveryQuests,
            "PerfectionScore": self.PerfectionScore,
            "EndSlideShow": self.EndSlideShow,
            "SpouseAdopts": self.SpouseAdopts,
            "SpouseWantsChildren": self.SpouseWantsChildren,
            "SpouseGiftJealousy": self.SpouseGiftJealousy,
            "SpouseGiftJealousyFriendshipChange": self.SpouseGiftJealousyFriendshipChange,
            "SpouseRoom": self.SpouseRoom,
            "SpousePatio": self.SpousePatio,
            "SpouseFloors": self.SpouseFloors,
            "SpouseWallpapers": self.SpouseWallpapers,
            "DumpsterDiveFriendshipEffect": self.DumpsterDiveFriendshipEffect,
            "DumpsterDiveEmote": self.DumpsterDiveEmote,
            "FriendsAndFamily": self.FriendsAndFamily,
            "FlowerDanceCanDance": self.FlowerDanceCanDance,
            "WinterStarGifts": self.WinterStarGifts,
            "WinterStarParticipant": self.WinterStarParticipant,
            "UnlockConditions": self.UnlockConditions,
            "SpawnIfMissing": self.SpawnIfMissing,
            "Home": self.Home,
            "TextureName": self.TextureName,
            "Appearance": self.Appearance,
            "MugShotSourceRect": self.MugShotSourceRect,
            "Size": self.Size,
            "Breather": self.Breather,
            "BreathChestRect": self.BreathChestRect,
            "BreathChestPosition": self.BreathChestPosition,
            "Shadow": self.Shadow,
            "EmoteOffset": self.EmoteOffset,
            "ShakePortraits": self.ShakePortraits,
            "KissSpriteIndex": self.KissSpriteIndex,
            "KissSpriteFacingRight": self.KissSpriteFacingRight,
            "HiddenProfileEmoteSound": self.HiddenProfileEmoteSound,
            "HiddenProfileEmoteDuration": self.HiddenProfileEmoteDuration,
            "HiddenProfileEmoteStartFrame": self.HiddenProfileEmoteStartFrame,
            "HiddenProfileEmoteFrameCount": self.HiddenProfileEmoteFrameCount,
            "HiddenProfileEmoteFrameDuration": self.HiddenProfileEmoteFrameDuration,
            "FormerCharacterNames": self.FormerCharacterNames,
            "FestivalVanillaActorIndex": self.FestivalVanillaActorIndex,
            "CustomFields": self.CustomFields
        }
