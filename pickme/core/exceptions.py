"""
    :package:   PickMe
    :file:      exceptions.py
    :brief:     Exceptions classes.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.5
"""

class Error(Exception):
    """Base class for exception in Hestia."""
    pass

class CoreError(Error):
    def __init__(self, message):
        """Exception raised for errors in the pickme.core module.
        Args:
            message (str): Error message.
        """
        self.message = message

class SVGError(Error):
    def __init__(self, message):
        """Exception raised for errors in the svg class.
        Args:
            message (str): Error message.
        """
        self.message = message