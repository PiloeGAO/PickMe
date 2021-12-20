'''
    :package:   PickMe
    :file:      userSetup.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Autodesk Maya user setup script.
'''

from maya import utils
from maya import cmds

from pickme.dccs.maya.shelf import create_shelf

# Delay execution on UI startup
utils.executeDeferred(create_shelf)