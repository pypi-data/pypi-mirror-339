from typing import Optional

class schedulesData:
    def __init__(
        self,
        key: str,
        time:Optional[int]= None,
        special_command: Optional[str]=None,
        location:Optional[str]=None,
        tileX: Optional[int]=None,
        tileY: Optional[int]=None,
        facingDirection: Optional[int]=None,
        animation: Optional[str]=None,
        dialogue:Optional[str]=None
    ):
        self.key=key
        self.value=""
        if special_command:
            self.value=special_command
        else:
            self.value=f"{time} {location} {tileX} {tileY} {facingDirection}"
            if animation:
                self.value+=f" {animation}"
            if dialogue:
                self.value+=f" {dialogue}"

        


    def getJson(self) -> str:
        return self.value