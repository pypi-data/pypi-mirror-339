from .model import modelsData
from typing import Any, Optional, List

class TriggerActionsData(modelsData):
    def __init__(
            self,
            key: str,
            Id: str,
            Trigger: str,
            Condition: str=None,
            SkipPermanentlyCondition: Optional[Any] = None,
            HostOnly: bool = False,
            Action: str = None,
            Actions: Optional[List[str]] = None,
            CustomFields: Optional[Any] = None,
            MarkActionApplied: bool = True
        ):
        super().__init__(key)

        self.Id = Id
        self.Trigger = Trigger
        self.Condition = Condition
        self.SkipPermanentlyCondition = SkipPermanentlyCondition
        self.HostOnly = HostOnly
        self.Action = Action
        self.Actions = Actions if Actions is not None else []
        self.CustomFields = CustomFields
        self.MarkActionApplied = MarkActionApplied

    def getJson(self) -> dict:
        return {
            "Id": self.Id,
            "Trigger": self.Trigger,
            "Condition": self.Condition,
            "SkipPermanentlyCondition": self.SkipPermanentlyCondition,
            "HostOnly": self.HostOnly,
            "Action": self.Action,
            "Actions": self.Actions,
            "CustomFields": self.CustomFields,
            "MarkActionApplied": self.MarkActionApplied
        }
