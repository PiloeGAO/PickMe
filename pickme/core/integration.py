'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Default integration class.
'''

class Integration(object):
    def __init__(self):
        self._name = "Standalone"
    
    @property
    def name(self):
        return self._name