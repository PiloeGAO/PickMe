'''
    :package:   PickMe
    :file:      path.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     Path functions.
'''
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ICONS_DIR = os.path.join(ROOT_DIR, "icons")

CONFIG_DIR = os.environ.get("pickme_configs", os.path.join(ROOT_DIR, "configs"))