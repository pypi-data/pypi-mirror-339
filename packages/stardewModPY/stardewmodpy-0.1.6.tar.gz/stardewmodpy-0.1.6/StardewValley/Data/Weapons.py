from .model import modelsData
from typing import Any, Optional

class WeaponsData(modelsData):
    def __init__(
            self,
            key: str,
            Name: str,
            DisplayName: str,
            Description: str,
            MinDamage: int,
            MaxDamage: int,
            Knockback: float,
            Speed: int,
            Precision: int,
            Defense: int,
            Type: int,
            MineBaseLevel: int,
            MineMinLevel: int,
            AreaOfEffect: int,
            CritChance: float,
            CritMultiplier: float,
            CanBeLostOnDeath: bool,
            Texture: str,
            SpriteIndex: int,
            Projectiles: Optional[Any] = None,
            CustomFields: Optional[Any] = None
        ):
        super().__init__(key)

        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.MinDamage = MinDamage
        self.MaxDamage = MaxDamage
        self.Knockback = Knockback
        self.Speed = Speed
        self.Precision = Precision
        self.Defense = Defense
        self.Type = Type
        self.MineBaseLevel = MineBaseLevel
        self.MineMinLevel = MineMinLevel
        self.AreaOfEffect = AreaOfEffect
        self.CritChance = CritChance
        self.CritMultiplier = CritMultiplier
        self.CanBeLostOnDeath = CanBeLostOnDeath
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.Projectiles = Projectiles
        self.CustomFields = CustomFields

    def getJson(self) -> dict:
        return {
            "Name": self.Name,
            "DisplayName": self.DisplayName,
            "Description": self.Description,
            "MinDamage": self.MinDamage,
            "MaxDamage": self.MaxDamage,
            "Knockback": self.Knockback,
            "Speed": self.Speed,
            "Precision": self.Precision,
            "Defense": self.Defense,
            "Type": self.Type,
            "MineBaseLevel": self.MineBaseLevel,
            "MineMinLevel": self.MineMinLevel,
            "AreaOfEffect": self.AreaOfEffect,
            "CritChance": self.CritChance,
            "CritMultiplier": self.CritMultiplier,
            "CanBeLostOnDeath": self.CanBeLostOnDeath,
            "Texture": self.Texture,
            "SpriteIndex": self.SpriteIndex,
            "Projectiles": self.Projectiles,
            "CustomFields": self.CustomFields
        }
