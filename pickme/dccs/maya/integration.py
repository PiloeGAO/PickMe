'''
    :package:   PickMe
    :file:      integration.py
    :author:    ldepoix
    :version:   0.0.1
    :brief:     PickMe Maya integration class.
'''
from pickme.core.integration import Integration

class MayaIntegration(Integration):
    def __init__(self) -> None:
        super(MayaIntegration, self).__init__()

        self._name = "Maya"