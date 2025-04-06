from .verification import steamLoad
from .contentpatcher import ContentPatcher
from .manifest import Manifest
from .jsonreader import jsonStardewRead
import os, shutil, subprocess

class Helper:
    def __init__(self, manifest:Manifest):
        self.modFolderAssets=os.path.join(os.getcwd(), "assets")
        self.content = ContentPatcher(manifest=manifest)
        steamVerify=steamLoad()
        self.pathSteam=steamVerify.verify()
        self.jsonRead=jsonStardewRead()
    
    def sdk(self, assetFolder:str, assetObject:str):
        sdkPath=os.path.join(self.pathSteam, "Content (unpacked)", assetFolder, assetObject+".json")
        return self.jsonRead.read_json(sdkPath)


    def write(self):
        modPath=os.path.join(self.pathSteam, "Mods", self.content.Manifest.Name)
        if os.path.exists(modPath):
            shutil.rmtree(modPath)
        if not os.path.exists(modPath):
            os.makedirs(modPath)
            if(os.path.exists(self.modFolderAssets)):
                shutil.copytree(self.modFolderAssets,os.path.join(modPath, "assets"))

        
        
            
        self.jsonRead.write_json(os.path.join(modPath, "manifest.json"), self.content.Manifest.json())
        self.jsonRead.write_json(os.path.join(modPath, "content.json"), self.content.contentFile)
        for key, value in self.content.contentFiles.items():            
            self.jsonRead.write_json(os.path.join(modPath, "assets", f"{key}.json"), value)
        

        try:
            subprocess.run(os.path.join(self.pathSteam, "StardewModdingApi.exe"), check=True)
        except:
            print("Erro ao iniciar o jogo")