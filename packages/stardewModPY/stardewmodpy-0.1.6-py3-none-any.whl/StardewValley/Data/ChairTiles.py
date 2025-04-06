from .model import modelsData


class ChairTiles(modelsData):
    def __init__(
        self, 
        key: str,
        sheet_filename: str,
        tileX: int,
        tileY: int,
        width_in_tiles: int,
        height_in_tiles: int,
        direction: str,
        type: str,
        drawTileX: int,
        drawTileY: int,
        isSeasonal: bool
    ):
        super().__init__(key)
        self.sheet_filename = sheet_filename
        self.tileX = tileX
        self.tileY = tileY
        self.width_in_tiles = width_in_tiles
        self.height_in_tiles = height_in_tiles
        self.direction = direction
        self.type = type
        self.drawTileX = drawTileX
        self.drawTileY = drawTileY
        self.isSeasonal = isSeasonal


    def getJson(self) -> str:
        return f"{self.sheet_filename}/{self.tileX}/{self.tileY}/{self.width_in_tiles}/{self.height_in_tiles}/{self.direction}/{self.type}/{self.drawTileX}/{self.drawTileY}/{self.isSeasonal}"
