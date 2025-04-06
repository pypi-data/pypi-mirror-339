from .model import modelsData
from typing import Optional, Any


class IncomingPhoneCallsData(modelsData):
    def __init__(
        self, 
        key: str,
        Dialogue: str,
        FromNpc: Optional[str] = None,
        FromPortrait: Optional[str] = None,
        FromDisplayName: Optional[str] = None,
        MaxCalls: Optional[int] = 1,
        TriggerCondition: Optional[str] = None,
        RingCondition: Optional[str] = None,
        IgnoreBaseChance: Optional[bool] = False,
        SimpleDialogueSplitBy: Optional[str] = None,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.Dialogue = Dialogue
        self.FromNpc = FromNpc
        self.FromPortrait = FromPortrait
        self.FromDisplayName = FromDisplayName
        self.MaxCalls = MaxCalls
        self.TriggerCondition = TriggerCondition
        self.RingCondition = RingCondition
        self.IgnoreBaseChance = IgnoreBaseChance
        self.SimpleDialogueSplitBy = SimpleDialogueSplitBy
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "Dialogue": self.Dialogue,
            "FromNpc": self.FromNpc,
            "FromPortrait": self.FromPortrait,
            "FromDisplayName": self.FromDisplayName,
            "MaxCalls": self.MaxCalls,
            "TriggerCondition": self.TriggerCondition,
            "RingCondition": self.RingCondition,
            "IgnoreBaseChance": self.IgnoreBaseChance,
            "SimpleDialogueSplitBy": self.SimpleDialogueSplitBy,
            "CustomFields": self.CustomFields
        }
