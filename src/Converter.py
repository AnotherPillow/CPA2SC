import json5, shutil, os, json
from PIL import Image

from .Logger import logger

class Converter:
    manifest: dict = {}
    incontent: dict = {}
    outcontent: dict = {
        "Format": "2.0",
        "Changes": []
    }

    def internaliseAsset(self, fp):
        return "{{InternalAssetKey: " + fp + "}}"
    
    
    def __init__(self):
        self.manifest = json5.load(open('input/manifest.json', encoding='utf8'))
        self.incontent = json5.load(open('input/content.json', encoding='utf8'))

        if os.path.exists('output'):
            shutil.rmtree('output')
        shutil.copytree('input', 'output')

    def convert(self):
        for change in self.incontent['Changes']:
            img = None
            if change['Action'] == 'Load':
                img = Image.load(change['FromFile'])
            if 'AnimationFrameTime' in change and 'AnimationFrameCount' in change:
                new = {
                    'LogName': f'Add animation for {change["Target"]}' if 'LogName' not in change else change['LogName'],
                    'Action': 'EditData',
                    'Target': 'spacechase0.SpaceCore/TextureOverrides',
                    'Entries': {
                        self.manifest['UniqueID'] + '_' + change['Target']: {
                            'TargetTexture': change['Target'],
                            'TargetRect': {
                                "X": 0,
                                "Y": 0,
                                "Width": img.size[0],
                                "Height": img.size[1],
                            } if img != None else change['ToArea'],
                            'SourceTexture': f"{self.internaliseAsset(change['FromFile'])}:0..{change['AnimationFrameCount'] - 1}@{change['AnimationFrameTime']}"
                                # "ToArea": { "X": 32, "Y": 48, "Width": 16, "Height": 16 }

                            
                        }
                    }
                }
                self.outcontent['Changes'].append(new)
            else:
                self.outcontent['Changes'].append(change)



        self.translateManifest()
        self.save()

    def translateManifest(self):
        self.manifest['Author'] += ' ~ CPA2SC'
        
    def save(self):
        logger.info(self.outcontent)
        
        with open('output/manifest.json', 'w') as f:
            json.dump(self.manifest, f, indent=4)
        
        with open('output/content.json', 'w') as f:
            json.dump(self.outcontent, f, indent=4)