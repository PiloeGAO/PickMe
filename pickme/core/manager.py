'''
    :package:   PickMe
    :file:      manager.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe manager.
'''
import os

from pickme.core.path import CONFIG_DIR
from pickme.core.rig import Rig

class Manager():
    def __init__(self, integration="standalone") -> None:

        if(integration == "maya"):
            from pickme.dccs.maya.integration import MayaIntegration
            self._integration = MayaIntegration()
        else:
            from pickme.core.integration import Integration
            self._integration = Integration()
        
        print(f"Current integration: {self._integration.name}")

        self._rigs = []

        self.load_configurations()

    @property
    def rigs(self):
        return self._rigs
    
    def load_configurations(self):
        """Load rig configurations from disk.
        """
        configurations_directories = [
            name for name in os.listdir(CONFIG_DIR)\
            if os.path.isfile(os.path.join(CONFIG_DIR, name, "config.json"))
        ]

        for dir in configurations_directories:
            config_filepath = os.path.join(CONFIG_DIR, dir, "config.json")
            config_icon = os.path.join(CONFIG_DIR, dir, "icon.png")

            if(self._integration.name != "Standalone"):
                # Only display rigs loaded in the scene.
                if(not self._integration.is_rig(dir)):
                    continue
                
            for object in self._integration.all_rigs(dir):
                rig = Rig(name=object, path=config_filepath, icon=config_icon)
                self._rigs.append(rig)
    
    def reload_configurations(self):
        """Clear the rigs in memory to reload the directory.
        """
        self._rigs = []
        self.load_configurations()