'''
    :package:   PickMe
    :file:      shelf.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Maya shelf (source: arnoldShelf.py [mtoa plugin]).
'''
import os

from maya import cmds
import maya

from pickme.core.path import ICONS_DIR

def remove_shelf():
    """Clear the current PickMe shelf from the interface.
    """
    if(cmds.shelfLayout('PickMe', exists=True)):
        cmds.deleteUI('PickMe')

def create_shelf():
    """Create a new Maya Shelf with a button to open the PickMe interface.
    """
    remove_shelf()
    shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
    maya.mel.eval('global string $PickMeShelf;')
    maya_version = int(cmds.about(version=True))
    if(maya_version < 2017):
        maya.mel.eval('$PickMeShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel PickMe`;')   
    else:
        maya.mel.eval('$PickMeShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel -version \"2022\" PickMe`;')

    shelfStyle = ('shelf' if maya_version >= 2016 else 'simple')

    cmds.shelfButton(
        label='Open PickMe',
        command='from pickme.dccs.maya.shelf_commands import open_ui; open_ui()',
        sourceType='python', annotation='',
        image=os.path.join(ICONS_DIR, "pointer.png"),
        style='iconOnly'
    )

    cmds.separator(width=12,height=35, style=shelfStyle, hr=False)

    cmds.shelfButton(
        label='Open help',
        command='from pickme.dccs.maya.shelf_commands import open_doc; open_doc()',
        sourceType='python', annotation='',
        image=os.path.join(ICONS_DIR, "information.png"),
        style='iconOnly'
    )