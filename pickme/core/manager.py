'''
    :package:   PickMe
    :file:      manager.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe manager.
'''
import os
import sys

from pickme import __version__
from pickme.core.path import GLOBAL_CONFIG_DIR, LOCAL_CONFIG_DIR
from pickme.core.rig import Rig
from pickme.core.update_system import UpdateVersion, get_update_versions

from pickme.core.logger import get_logger
logger = get_logger(debug=bool(os.environ.get("PICKME_DEBUG", "False")))

class Manager():
    def __init__(self, main_widget, integration="standalone") -> None:
        logger.info("Manager start.")
        if(not os.path.isdir(LOCAL_CONFIG_DIR)):
            logger.info("Building local config directory.")
            os.mkdir(LOCAL_CONFIG_DIR)

        self._main_widget = main_widget

        if(integration.lower() == "maya"):
            from pickme.dccs.maya.integration import MayaIntegration
            self._integration = MayaIntegration(manager = self)

            self._integration.hook_exceptions()
        else:
            from pickme.core.integration import Integration
            self._integration = Integration()

            self.hook_exceptions()
        
        self.check_for_updates()
        logger.info(f"Current integration: {self._integration.name}")

        self._current_rig = 0
        self._rigs = []
        
        self.load_configurations()
        logger.info("Manager loaded successfully.")

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
    
    # Manager tuils functions.
    def hook_exceptions(self):
        """Define a custom exception handling for the application.
        """
        old_hook = sys.excepthook

        def new_hook(type, value, traceback):
            self.error_exec_function(type, value, traceback)
            old_hook(type, value, traceback)
        
        sys.excepthook = new_hook
    
    def error_exec_function(self, type, value, traceback):
        """Function to run on error, to display the error message to user.

        Args:
            type (class): Exception class
            value (str): Value of the exception
            traceback (class: traceback): position of the error
        """
        logger.error(f"{type.__name__} : {value}")

        self.ui.show_error(type, value, traceback)
    
    def check_for_updates(self):
        """Check for updates, and display a modal if new version is available.
        """
        logger.info(f"Current version {__version__}")

        if(bool(os.environ.get("PICKME_VERSION_CHECK", "True")) == False):
            logger.warning("Update check de-activated, skipping version check.")
            return

        online_versions = get_update_versions("https://api.github.com/repos/PiloeGAO/PickMe/releases")
        if(len(online_versions) == 0): return
        
        current_version = UpdateVersion(name="Current Version", description="", number=__version__)

        if(online_versions[-1].version_id > current_version.version_id):
            logger.info(f"New update is available : {online_versions[-1].version}")

            self._main_widget.open_update_dialog(online_versions[-1])
    
    # Core PickMe functions.
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

######################
# Manager Management #
######################
CURRENT_MANAGER = None

def set_current_manager(manager):
    """Set the current manager.
    Args:
        manager (class:`Manager`): Manager instance.
    """
    global CURRENT_MANAGER
    CURRENT_MANAGER = manager

def current_manager():
    """Get current manager.
    Returns:
        class:`Manager`: Manager instance.
    """
    global CURRENT_MANAGER
    return CURRENT_MANAGER

def start_manager(*args, **kwargs):
    """Start a manager.

    Returns:
        class:`Manager`: Manager initialized.
    """
    if(current_manager()):
        logger.info("Manager already started, using it.")
        return current_manager()
    
    integration = kwargs["integration"] if "integration" in kwargs else "standalone"

    manager = Manager(kwargs.get("main_widget"), integration)
    set_current_manager(manager)

    return manager