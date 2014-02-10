"""Z80 instruction and support classes"""

import abc
import logging


#-----------------------------------------------------------------------------
# Module Data
#-----------------------------------------------------------------------------

# module logger
_logger = logging.getLogger(__name__)


#-----------------------------------------------------------------------------
# Interfaces
#-----------------------------------------------------------------------------

class InstructionInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self):
        """Execute the instruction"""
        pass

    @property
    def complete(self):
        """Flag used to indicate if execution is complete"""
        return (self._cycles == 0)

    @property
    def cycles(self):
        """Number of cycles remaining to finish execution"""
        return self._cycles

    @property
    def descriptor(self):
        """Description of the instruction...used to feed __str__"""
        return self._descriptor

    @descriptor.setter
    def descriptor(self, new_value):
        self._descriptor = new_value

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class AddressMode(object):
    """Instruction Addressing Modes"""

    REGISTER          = 0
    REGISTER_INDIRECT = 1
    INDEXED           = 2
    EXT_ADDRESS       = 3
    IMMEDIATE         = 4

class Load_8b(InstructionInterface):
    """8-bit Load Instruction"""

    def __init__(self, cycles, destination, source, cycles):
        """Initialization"""

        self._dest = destination
        self._src  = source
        self._cycles = cycles
        self._descriptor = None

    def execute(self):
        """Execute the load instruction"""

        self._cycles -= 1

        if self._cycles == 0:
            
            self._dest = self._src

        elif self._cycles < 0:

            self._cycles = 0

