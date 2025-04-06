from .model import modelsData
from typing import Any, Optional


class MuseumRewardsData(modelsData):
    def __init__(
        self,
        key: str,
        TargetContextTags: list[dict[str, Any]],
        RewardActions: list[str] = None,
        RewardItemId: Optional[str] = None,
        RewardItemCount: Optional[int] = 1,
        RewardItemIsSpecial: Optional[bool] = False,
        RewardItemIsRecipe: Optional[bool] = False,
        FlagOnCompletion: Optional[bool] = False,
        CustomFields: Optional[Any] = None
    ):
        super().__init__(key)
        self.TargetContextTags = TargetContextTags
        self.RewardActions = RewardActions
        self.RewardItemId = RewardItemId
        self.RewardItemCount = RewardItemCount
        self.RewardItemIsSpecial = RewardItemIsSpecial
        self.RewardItemIsRecipe = RewardItemIsRecipe
        self.FlagOnCompletion = FlagOnCompletion
        self.CustomFields = CustomFields


    def getJson(self) -> dict:
        return {
            "TargetContextTags": self.TargetContextTags,
            "RewardActions": self.RewardActions,
            "RewardItemId": self.RewardItemId,
            "RewardItemCount": self.RewardItemCount,
            "RewardItemIsSpecial": self.RewardItemIsSpecial,
            "RewardItemIsRecipe": self.RewardItemIsRecipe,
            "FlagOnCompletion": self.FlagOnCompletion,
            "CustomFields": self.CustomFields
        }
