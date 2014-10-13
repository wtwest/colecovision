"""Z80 instruction and support classes"""

import abc
import logging
import colecovision.cpu.condition

#-----------------------------------------------------------------------------
# Module Data
#-----------------------------------------------------------------------------

# module logger
_logger = logging.getLogger(__name__)


#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

LOAD_8B_REGISTER_TO_REGISTER = 0x40


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
    
class UnknownRegisterError(InstructionError):
    """Unknow register ID error"""
    
    def __init__(self, bad_register_id):
        """Initialization"""
        
        self.bad_register_id = bad_register_id
        
    def __str__(self):
        """User-friendly string representation"""
        
        msg = "Unknown register ID {0}".format(self.bad_register_id)
        
        return msg
        
class AddressMode(object):
    """Instruction Addressing Modes"""

    REGISTER          = 0
    REGISTER_INDIRECT = 1
    INDEXED           = 2
    EXT_ADDRESS       = 3
    IMMEDIATE         = 4
    MEMORY_IMMEDIATE  = 5
    REGISTER_SPECIAL  = 6 # interrupt vector, memory refresh, etc.

class Load_8b(InstructionInterface):
    """8-bit Load Instruction"""


    # This dictionary uses the addressing modes for
    # the load destination and load source to determine
    # the cycle count for the instruction
    cycle_map = { (AddressMode.REGISTER, AddressMode.REGISTER)           : 4,
                  (AddressMode.REGISTER, AddressMode.IMMEDIATE)          : 7,
                  (AddressMode.REGISTER, AddressMode.REGISTER_INDIRECT)  : 7,
                  (AddressMode.REGISTER, AddressMode.INDEXED)            : 19,
                  (AddressMode.REGISTER_INDIRECT, AddressMode.REGISTER)  : 7,
                  (AddressMode.INDEXED, AddressMode.REGISTER)            : 19,
                  (AddressMode.REGISTER_INDIRECT, AddressMode.IMMEDIATE) : 10,
                  (AddressMode.INDEXED, AddressMode.IMMEDIATE)           : 19,
                  (AddressMode.REGISTER, AddressMode.MEMORY_IMMEDIATE)   : 13,
                  (AddressMode.MEMORY_IMMEDIATE, AddressMode.REGISTER)   : 13,
                  (AddressMode.REGISTER, AddressMode.REGISTER_SPECIAL)   : 9  }

    def __init__(self, register_set, ext_mem, 
                 addressing_mode, src, dst, **kwargs):
        """Initialization"""

        self._register        = register_set
        self._ext_mem         = ext_mem
        self._addressing_mode = addressing_mode
        self._src             = src
        self._dst             = dst
        self._cycles          = Load_8b.cycle_map[addressing_mode]

        if kwargs.has_key('src_idx'):
            self._src_idx = kwargs['src_idx']

        if kwargs.has_key('dst_idx'):
            self._dst_idx = kwargs['dst_idx']

        if kwargs.has_key('iff2'):
            self._iff2 = kwargs['iff2']

    def execute(self):
        """Execute the load instruction"""

        if self._cycles > 0:

            self._cycles -= 1

            if self._cycles == 0:

                if self._addressing_mode == (AddressMode.REGISTER, AddressMode.REGISTER):

                    self._dst.value = self._src.value

                elif self._addressing_mode == (AddressMode.REGISTER, AddressMode.IMMEDIATE):

                    self._dst.value = src

                elif self._addressing_mode == (AddressMode.REGISTER, AddressMode.REGISTER_INDIRECT):

                    self._dst.value = self._ext_mem.read(self._src.value)

                elif self._addressing_mode == (AddressMode.REGISTER, AddressMode.INDEXED):

                    self._dst.value = self._ext_mem.read(self._src.value + self._src_idx)

                elif self._addressing_mode == (AddressMode.REGISTER_INDIRECT, AddressMode.REGISTER):

                    self._ext_mem.write(self._dst.value, self._src.value)

                elif self._addressing_mode == (AddressMode.INDEXED, AddressMode.REGISTER):

                    self._ext_mem.write(self._dst.value + self._dst_idx, self._src.value)

                elif self._addressing_mode == (AddressMode.REGISTER_INDIRECT, AddressMode.IMMEDIATE):

                    self._ext_mem.write(self._dst.value, src)

                elif self._addressing_mode == (AddressMode.INDEXED, AddressMode.IMMEDIATE):

                    self._ext_mem.write(self._dst.value + self._dst_idx, self._src)

                elif self._addressing_mode == (AddressMode.REGISTER, AddressMode.MEMORY_IMMEDIATE):

                    self._dst.value = self._ext_mem.read(self._src)

                elif self._addressing_mode == (AddressMode.MEMORY_IMMEDIATE, AddressMode.REGISTER):

                    self._ext_mem.write(self._dst, self._src.value)

                elif self._addressing_mode == (AddressMode.REGISTER, AddressMode.REGISTER_SPECIAL):

                    self._dst.value = self._src.value

                    # update the sign flag
                    if (self._src.value & 0x10):
                        self._register['F'].value = self._register['F'].value | cpu.colecovision.condition.SIGN
                    else:
                        self._register['F'].value = self._register['F'].value & ~cpu.colecovision.condition.SIGN

                    
                    # update the zero flag
                    if not self._src.value:
                        self._register['F'].value = self._register['F'].value | cpu.colecovision.condition.ZERO
                    else:
                        self._register['F'].value = self._register['F'].value & ~cpu.colecovision.condition.ZERO

                    # reset half-carry
                    self._register['F'].value = self._register['F'].value & ~cpu.colecovision.condition.HALF_CARY

                    # add/substract is reset
                    self._register['F'].value = self._register['F'].value & ~cpu.colecovision.condition.SUBTRACT

                    # update the parity/overflow flag
                    if self._iff2:
                        self._register['F'].value = self._register['F'].value | cpu.colecovision.condition.PARITY_OVERFLOW
                    else:
                        self._register['F'].value = self._register['F'].value & ~cpu.colecovision.condition.PARITY_OVERFLOW

                else:
                    raise LoadError('Unknown addressing mode')

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------

def _get_load_instruction_register(register_id):
    """Returns the register associated with the register ID for a
    load instuction.
    """
    
    # load instruction register IDs
    REGISTER_ID_A = 7
    REGISTER_ID_B = 0
    REGISTER_ID_C = 1
    REGISTER_ID_D = 2
    REGISTER_ID_E = 3
    REGISTER_ID_H = 4
    REGISTER_ID_L = 5

    instruction_register = None
    
    if register_id == REGISTER_ID_A:
        instruction_register = 'A'
    elif register_id == REGISTER_ID_B:
        instruction_register = 'B'
    elif register_id == REGISTER_ID_C:
        instruction_register = 'C'
    elif register_id == REGISTER_ID_D:
        instruction_register = 'D'
    elif register_id == REGISTER_ID_E:
        instruction_register = 'E'
    elif register_id == REGISTER_ID_H:
        instruction_register = 'H'
    elif register_id == REGISTER_ID_L:
        instruction_register = 'L'
    else:
        raise UnknownRegisterError(register_id)
    
    return instruction_register

def create(register, memory):
    
    """Decodes memory at the given PC address and creates an instruction.
    
    Returns a tuple that contains the number of bytes read and the
    instruction.
    """
    
    # no instruction
    created_instruction = None
    
    # no bytes read
    instruction_bytes_read = 0

    # create possible one, two, three, and four byte instructions
    one_byte_instruction   = memory.read(register['PC'].value)
    two_byte_instruction   = (memory.read(register['PC'].value + 1) << 8) | one_byte_instruction
    three_byte_instruction = (memory.read(register['PC'].value + 2) << 16) | two_byte_instruction
    four_byte_instruction  = (memory.read(register['PC'].value + 3) << 16) | three_byte_instruction
                                                   
    
    if (one_byte_instruction & LOAD_8B_REGISTER_TO_REGISTER):
        
        src_reg = _get_load_instruction_register(one_byte_instruction & 0x07)
        dst_reg = _get_load_instruction_register((one_byte_instruction >> 3) & 0x07)
        
        created_instruction = Load_8b(register, None, (AddressMode.REGISTER, AddressMode.REGISTER),
                                      register[src_reg], register[dst_reg])
        
        instruction_bytes_read = 1
        
    
    return (instruction_bytes_read, created_instruction)

