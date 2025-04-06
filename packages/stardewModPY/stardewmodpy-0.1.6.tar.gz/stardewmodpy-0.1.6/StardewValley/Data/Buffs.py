from typing import Optional, List
from .model import modelsData

class BuffsData(modelsData):
    def __init__(self, key:str, DisplayName:str, Duration:int, IconTexture:str,
    IconSpriteIndex:Optional[int]=0, Description:Optional[str]=None,
    IsDebuff:Optional[bool]=None, GlowColor:Optional[str]=None, 
    MaxDuration:Optional[int]=-1, Effects:Optional[dict]=None, ActionsOnApply:Optional[list[str]]=None,
    CustomFields:Optional[str]=None):
        super().__init__(key)
        self.DisplayName=DisplayName
        self.Duration=Duration
        self.IconTexture=IconTexture
        self.IconSpriteIndex=IconSpriteIndex
        self.Description=Description
        self.IsDebuff=IsDebuff
        self.GlowColor=GlowColor
        self.MaxDuration=MaxDuration
        self.Effects=Effects
        self.ActionsOnApply=ActionsOnApply
        self.CustomField=CustomFields
    
    def getJson(self) -> dict:
        return {
            "Key": self.key,
            "DisplayName": self.DisplayName,
            "Duration": self.Duration,
            "IconTexture": self.IconTexture,
            "IconSpriteIndex": self.IconSpriteIndex,
            "Description": self.Description,
            "IsDebuff": self.IsDebuff,
            "GlowColor": self.GlowColor,
            "MaxDuration": self.MaxDuration,
            "Effects": self.Effects if self.Effects is not None else {},
            "ActionsOnApply": self.ActionsOnApply if self.ActionsOnApply is not None else [],
            "CustomFields": self.CustomField
        }