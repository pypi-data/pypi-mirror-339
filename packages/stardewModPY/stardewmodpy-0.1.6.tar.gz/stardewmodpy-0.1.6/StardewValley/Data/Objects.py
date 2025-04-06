from typing import Optional, List
from .model import modelsData

class ObjectsBuffsData(modelsData):
    def __init__(self,
            Id:str,
            Duration: Optional[int]=0,
            BuffId: Optional[int]=None,
            IsDebuff: Optional[bool]=False,
            IconTexture: Optional[str]=None,
            IconSpriteIndex: Optional[int]=0,
            GlowColor: Optional[str]=None,
            CustomAttributes: Optional[dict[str, str]]=None,
            CustomFields: Optional[dict[str, str]]=None

        ):
        super().__init__(None)
        self.Id=Id
        self.BuffId=BuffId
        self.IconTexture=IconTexture
        self.IconSpriteIndex=IconSpriteIndex
        self.Duration=Duration
        self.IsDebuff=IsDebuff
        self.GlowColor=GlowColor
        self.CustomAttributes=CustomAttributes
        self.CustomFields=CustomFields
    
    def getJson(self) -> dict:
        return {
            "Id" : self.Id,
            "BuffId" : self.BuffId,
            "IconTexture" : self.IconTexture,
            "IconSpriteIndex" : self.IconSpriteIndex,
            "Duration" : self.Duration,
            "IsDebuff" : self.IsDebuff,
            "GlowColor" : self.GlowColor,
            "CustomAttributes" : self.CustomAttributes,
            "CustomFields" : self.CustomFields
        }


class ObjectsData(modelsData):
    def __init__(
            self,
            key: str,
            Name: str,
            DisplayName: str,
            Description: str,
            Type: str,
            Category: int,
            Price: Optional[int]=0, 
            Texture: Optional[str] = None,
            SpriteIndex: int = 0,
            ColorOverlayFromNextIndex: Optional[bool] = False, 
            Edibility: Optional[int] = -300,
            IsDrink: Optional[bool] = False,
            Buffs: Optional[List[ObjectsBuffsData]] = None, 
            GeodeDropsDefaultItems: bool = False,
            GeodeDrops: Optional[List[str]] = None, 
            ArtifactSpotChances: Optional[str] = None,
            CanBeGivenAsGift: bool = True, 
            CanBeTrashed: bool = True,
            ExcludeFromFishingCollection: bool = False, 
            ExcludeFromShippingCollection: bool = False,
            ExcludeFromRandomSale: bool = False, 
            ContextTags: Optional[List[str]] = None,
            CustomFields: Optional[str] = None
        ):
        
        super().__init__(key)
        # Atribuindo valores padrão para listas e outros mutáveis
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Type = Type
        self.Category = Category
        self.Price = Price
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.ColorOverlayFromNextIndex = ColorOverlayFromNextIndex
        self.Edibility = Edibility
        self.IsDrink = IsDrink
        self.Buffs = Buffs  # Se None, usa lista vazia
        self.GeodeDropsDefaultItems = GeodeDropsDefaultItems
        self.GeodeDrops = GeodeDrops if GeodeDrops is not None else []  # Se None, usa lista vazia
        self.ArtifactSpotChances = ArtifactSpotChances
        self.CanBeGivenAsGift = CanBeGivenAsGift
        self.CanBeTrashed = CanBeTrashed
        self.ExcludeFromFishingCollection = ExcludeFromFishingCollection
        self.ExcludeFromShippingCollection = ExcludeFromShippingCollection
        self.ExcludeFromRandomSale = ExcludeFromRandomSale
        self.ContextTags = ContextTags if ContextTags is not None else []  # Se None, usa lista vazia
        self.CustomFields = CustomFields

    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "Type": self.Type,
            "Category": self.Category,
            "Price": self.Price,
            "Texture": self.Texture,
            "SpriteIndex": self.SpriteIndex,
            "ColorOverlayFromNextIndex": self.ColorOverlayFromNextIndex,
            "Edibility": self.Edibility,
            "IsDrink": self.IsDrink,
            "Buffs": None if self.Buffs is None else [buff.getJson() for buff in self.Buffs],
            "GeodeDropsDefaultItems": self.GeodeDropsDefaultItems,
            "GeodeDrops": self.GeodeDrops,
            "ArtifactSpotChances": self.ArtifactSpotChances,
            "CanBeGivenAsGift": self.CanBeGivenAsGift,
            "CanBeTrashed": self.CanBeTrashed,
            "ExcludeFromFishingCollection": self.ExcludeFromFishingCollection,
            "ExcludeFromShippingCollection": self.ExcludeFromShippingCollection,
            "ExcludeFromRandomSale": self.ExcludeFromRandomSale,
            "ContextTags": self.ContextTags,
            "CustomFields": self.CustomFields
        }
    
    @classmethod
    def fromJson(cls, key: str, data: dict):
        buffs = data.get("Buffs")
        buffs_obj = [ObjectsBuffsData.fromJson(b) for b in buffs] if buffs else None
        
        return cls(
            key=key,
            Name=data.get("Name"),
            DisplayName=data.get("DisplayName"),
            Description=data.get("Description"),
            Type=data.get("Type"),
            Category=data.get("Category"),
            Price=data.get("Price", 0),
            Texture=data.get("Texture"),
            SpriteIndex=data.get("SpriteIndex", 0),
            ColorOverlayFromNextIndex=data.get("ColorOverlayFromNextIndex", False),
            Edibility=data.get("Edibility", -300),
            IsDrink=data.get("IsDrink", False),
            Buffs=buffs_obj,
            GeodeDropsDefaultItems=data.get("GeodeDropsDefaultItems", False),
            GeodeDrops=data.get("GeodeDrops", []),
            ArtifactSpotChances=data.get("ArtifactSpotChances"),
            CanBeGivenAsGift=data.get("CanBeGivenAsGift", True),
            CanBeTrashed=data.get("CanBeTrashed", True),
            ExcludeFromFishingCollection=data.get("ExcludeFromFishingCollection", False),
            ExcludeFromShippingCollection=data.get("ExcludeFromShippingCollection", False),
            ExcludeFromRandomSale=data.get("ExcludeFromRandomSale", False),
            ContextTags=data.get("ContextTags", []),
            CustomFields=data.get("CustomFields")
        )