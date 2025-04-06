from .manifest import Manifest
from typing import Optional


class ContentData:
    def __init__(self):
        self.Action = self.__class__.__name__
        self.json={
            "Action":self.Action
        }

class Include(ContentData):
    def __init__(self, FromFile:str):
        super().__init__()
        self.json["FromFile"]=FromFile

class Load(ContentData):
    def __init__(self, LogName:str, Target:str, FromFile:str):
        super().__init__()
        self.json["LogName"]=LogName
        self.json["Target"]=Target
        self.json["FromFile"]=FromFile

class EditData(ContentData):
    def __init__(self, LogName:str, Target:str, TargetField:Optional[list[str]]=None, Fields:Optional[dict]=None, Entries:Optional[dict]=None):
        super().__init__()
        self.json["LogName"]=LogName
        self.json["Target"]=Target
        if TargetField:
            self.json["TargetField"]=TargetField
        if Fields:
            self.json["Fields"]=Fields
        if Entries:
            self.json["Entries"]=Entries

class EditImage(ContentData):
    def __init__(self, LogName:str, FromFile:str, FromArea:dict, ToArea:dict):
        super().__init__()
        self.json["LogName"]=LogName
        self.json["FromFile"]=FromFile
        self.json["FromArea"]=FromArea
        self.json["ToArea"]=ToArea

class ContentPatcher:
    def __init__(self, manifest:Manifest):
        self.Manifest=manifest
        self.Manifest.ContentPackFor={
            "UniqueID": "Pathoschild.ContentPatcher"
        }

        self.contentFile={
            "Format": "2.5.0",
            "Changes": []
        }

        self.contentFiles={}
    
    def registryContentData(self, contentData:Load|EditData|EditImage, contentFile:str="content", newFile:bool=True):
        if contentFile=="content":
            self.contentFile["Changes"].append(contentData.json)
        else:
            if newFile:
                self.contentFiles[contentFile]={
                    "Changes":[

                    ]
                }
            self.contentFiles[contentFile]["Changes"].append(contentData.json)
    
    
    


class contentNewFile:
    def __init__(self):
        self.content={
            "Changes": []
        }

