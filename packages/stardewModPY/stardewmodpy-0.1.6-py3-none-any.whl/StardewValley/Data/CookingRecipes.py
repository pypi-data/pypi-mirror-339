from .model import modelsData


class CookingRecipesData(modelsData):
    def __init__(
        self,
        key: str,
        Ingredients: str,
        Yield: str,
        Display_name: str = "",
        Unlock_conditions: str = "default"
    ):
        super().__init__(key)
        self.Ingredients = Ingredients
        self.Yield = Yield
        self.Unlock_conditions = Unlock_conditions
        self.Display_name = Display_name


    def getJson(self) -> str:
        return f"{self.Ingredients}/10 10/{self.Yield}/{self.Unlock_conditions}/{self.Display_name}"
