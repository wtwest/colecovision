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

class InstructionError(Exception):
    """Generic instruction error"""
    pass


class LoadError(InstructionError):
    """Load instruction error"""
    
    def __init__(self, msg):
        """Initialization"""
        
        self.msg = msg

    def __str__(self):
        """User-friendly string representation"""
        
        return self.mgs
        
class AddressMode(object):
    """Instruction Addressing Modes"""

    REGISTER          = 0
    REGISTER_INDIRECT = 1
    INDEXED           = 2
    EXT_ADDRESS       = 3
    IMMEDIATE         = 4

class Load_8b(InstructionInterface):
    """8-bit Load Instruction"""

    def __init__(self, cycles, 
                 destination, destination_mode,
                 source, source_mode,
                 *additional_data):
        """Initialization"""

        self._cycles = cycles
        self._dest = destination
        self._dest_mode = destination_mode
        self._src  = source
        self._src_mode = source_mode
        self._extra_args = additional_data

    def execute(self):
        """Execute the load instruction"""

        self._cycles -= 1

        if self._cycles == 0:
            
            source_val = None 

            # Get the source value
            
            if self._src_mode == AddressMode.REGISTER:

                source_val = self._src.value
            
            elif self._src_mode = AddressMode.REGISTER_INDIRECT:
                
                # TODO Need access to memory system
                pass

            elif self._src_mode = AddressMode.INDEXED:
                
                # TODO Need access to memory system
                pass

            elif self._src_mode = AddressMode.EXT_ADDRESS:
                
                source_value = self._src.read(self._extra_args)

            elif self._src_mode = AddressMode.IMMEDIATE:
                
                source_value = self._extra_args

            else:
                err_msg = "Source addressing mode {0} not supported".format(self._src_mode)
                raise LoadError(err_msg)
                
            # Load the souce value to the destination
            
            if self._dest_mode == AddressMode.REGISTER:
            
                self._dest.value = source_val
                
            elif self._dest_mode == AddressMode.REGISTER_INDIRECT:
            
                

        elif self._cycles < 0:

            self._cycles = 0

