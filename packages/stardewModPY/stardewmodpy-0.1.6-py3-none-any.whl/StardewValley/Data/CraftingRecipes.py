from .model import modelsData


class CraftingRecipesData(modelsData):
    def __init__(
        self,
        key: str,
        Ingredients: str,
        Types: str,
        Yield: str,
        Big_craftable: bool,
        Unlock_conditions: str,
        Display_name: str = ""
    ):
        super().__init__(key)
        self.Ingredients = Ingredients
        self.Types = Types
        self.Yield = Yield
        self.Big_craftable = "true" if Big_craftable else "false"
        self.Unlock_conditions = Unlock_conditions
        self.Display_name = Display_name


    def getJson(self) -> str:
        return f"{self.Ingredients}/{self.Types}/{self.Yield}/{self.Big_craftable}/{self.Unlock_conditions}/{self.Display_name}"
