from .model import modelsData
from typing import Optional, Any


class MachinesData(modelsData):
    def __init__(
        self, 
        key:str,
        OutputRules: Optional[list[dict[str, Any]]] = None,
        AdditionalConsumedItems: Optional[list[dict[str, Any]]] = None,
        AllowFairyDust: Optional[bool] = True,
        ReadyTimeModifiers: Optional[list[dict[str, Any]]] = None,
        ReadyTimeModifierMode: Optional[str] = "Stack"
    ):
        super().__init__(key)
        self.OutputRules = OutputRules if OutputRules is not None else []
        self.AdditionalConsumedItems = AdditionalConsumedItems if AdditionalConsumedItems is not None else []
        self.AllowFairyDust = AllowFairyDust
        self.ReadyTimeModifiers = ReadyTimeModifiers if ReadyTimeModifiers is not None else []
        self.ReadyTimeModifierMode = ReadyTimeModifierMode


    def getJson(self) -> dict:
        return {
            "OutputRules": self.OutputRules,
            "AdditionalConsumedItems": self.AdditionalConsumedItems,
            "AllowFairyDust": self.AllowFairyDust,
            "ReadyTimeModifiers": self.ReadyTimeModifiers,
            "ReadyTimeModifierMode": self.ReadyTimeModifierMode
        }
