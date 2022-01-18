'''
    :package:   PickMe
    :file:      manager.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe manager.
'''
import os

from pickme.core.path import GLOBAL_CONFIG_DIR, LOCAL_CONFIG_DIR
from pickme.core.rig import Rig

from pickme.core.logger import get_logger
logger = get_logger(debug=os.environ.get("PICKME_DEBUG", False))

class Manager():
    def __init__(self, main_widget, integration="standalone") -> None:
        if(not os.path.isdir(LOCAL_CONFIG_DIR)):
            logger.info("Building local config directory.")
            os.mkdir(LOCAL_CONFIG_DIR)

        self._main_widget = main_widget

        if(integration.lower() == "maya"):
            from pickme.dccs.maya.integration import MayaIntegration
            self._integration = MayaIntegration(manager = self)
        else:
            from pickme.core.integration import Integration
            self._integration = Integration()
        
        logger.info(f"Current integration: {self._integration.name}")

        self._current_rig = 0
        self._rigs = []
        
        self.load_configurations()

    @property
    def ui(self):
        return self._main_widget

    @property
    def integration(self):
        return self._integration

    @property
    def rigs(self):
        return self._rigs
    
    @property
    def current_rig(self):
        return self._current_rig
    
    @current_rig.setter
    def current_rig(self, id):
        if(len(self._rigs) >= id):
            self._current_rig = len(self._rigs)-1
        
        self._current_rig = id
        self._rigs[self._current_rig].reload()

    @property
    def rig(self):
        if(len(self._rigs) == 0):
            return None
        
        return self._rigs[self._current_rig]
    
    def add_rig(self, new_rig):
        """Add a rig to manager

        Args:
            new_rig (class: Rig): New rig
        """
        self._rigs.append(new_rig)
    
    def load_configurations(self):
        """Load rig configurations from disk.
        """
        configurations_directories = [
            name for name in os.listdir(GLOBAL_CONFIG_DIR)\
            if os.path.isfile(os.path.join(GLOBAL_CONFIG_DIR, name, "config.json"))
        ]

        for dir in configurations_directories:
            if(self._integration.name != "Standalone"):
                # Only display rigs loaded in the scene.
                if(not self._integration.is_rig(dir)):
                    continue
                
            for object in self._integration.all_rigs(dir):
                rig = Rig(
                    manager=self,
                    id=len(self._rigs),
                    name=object,
                    path=os.path.join(GLOBAL_CONFIG_DIR, dir)
                )
                
                self._rigs.append(rig)
    
    def reload_configurations(self):
        """Clear the rigs in memory to reload the directory.
        """
        self._rigs = []
        self.load_configurations()