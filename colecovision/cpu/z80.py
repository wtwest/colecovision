"""Z80 microprocessor emulation"""

import logging

from colecovision.emulate.cpu.register import Register, CompositeRegister
from colecovision.emulate.cpu.instruction import Load_8b
from colecovision.emulate.cpu.instruction import AddressMode


#-----------------------------------------------------------------------------
# Module Data
#-----------------------------------------------------------------------------

# module logger
_logger = logging.getLogger(__name__)


#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------


class Z80(object):
    """Z80 emulation"""

    # CPU honors interrupt request at the end of current instruction
    # if interrupts enabled.  interrupting device I/O device must
    # insert 8 bit response vector

    # on HALT instruction, keep executing NOPs and wait for NMI or
    # MI

    # NMI, higher priority than INT, honors intterupt at the end of
    # current instruction (independent of interrupt enable), forces
    # CPU restart @ 0x0066. Pushes PC onto stack

    # need member for interrupt_status (mode 0, etc.) and interrupt enable

    # on reset, reset interrupt enable, clear PC, I and R, set interrupt status
    # to Mode 0...takes 3 cycles

    def __init__(self, memory_system):
        """Initialization"""


        # Create the CPU registers
        self.register        = {}
        self.register["PC"]  = Register(length=16, init_value=0)
        self.register["SP"]  = Register(length=16, init_value=0)
        self.register["IX"]  = Register(length=16, init_value=0)
        self.register["IY"]  = Register(length=16, init_value=0)
        self.register["I"]   = Register(length=8,  init_value=0)
        self.register["R"]   = Register(length=8,  init_value=0)
        self.register["A"]   = Register(length=8,  init_value=0)
        self.register["A'"]  = Register(length=8,  init_value=0)
        self.register["F"]   = Register(length=8,  init_value=0)
        self.register["F'"]  = Register(length=8,  init_value=0)
        self.register["B"]   = Register(length=8,  init_value=0)
        self.register["B'"]  = Register(length=8,  init_value=0)
        self.register["C"]   = Register(length=8,  init_value=0)
        self.register["C'"]  = Register(length=8,  init_value=0)
        self.register["D"]   = Register(length=8,  init_value=0)
        self.register["D'"]  = Register(length=8,  init_value=0)
        self.register["E"]   = Register(length=8,  init_value=0)
        self.register["E'"]  = Register(length=8,  init_value=0)
        self.register["H"]   = Register(length=8,  init_value=0)
        self.register["H'"]  = Register(length=8,  init_value=0)
        self.register["L"]   = Register(length=8,  init_value=0)
        self.register["L'"]  = Register(length=8,  init_value=0)
        self.register["BC"]  = CompositeRegister(self.register['B'], self.register['C'])
        self.register["BC'"] = CompositeRegister(self.register["B'"], self.register["C'"])
        self.register["DE"]  = CompositeRegister(self.register["D"], self.register["E"])
        self.register["DE'"] = CompositeRegister(self.register["D'"], self.register["E'"])
        self.register["HL"]  = CompositeRegister(self.register["H"], self.register["L"])
        self.register["HL'"] = CompositeRegister(self.register["H'"], self.register["L'"])

        # Get a reference to the memory system (RAM, ROM)
        self.memsys = memory_system


        # Mapping of opcodes to instructions

                               # op code   class     arguments                                                                 bytes to read
        self._instruction_map = {0x57ed : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.i,      AddressMode.REGISTER),          0),
                                 0x5fed : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.r,      AddressMode.REGISTER),          0),
                                 0x007f : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.a,      AddressMode.REGISTER),          0),
                                 0x0078 : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.b,      AddressMode.REGISTER),          0),
                                 0x0079 : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.c,      AddressMode.REGISTER),          0),
                                 0x007a : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.d,      AddressMode.REGISTER),          0),
                                 0X007b : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.e,      AddressMode.REGISTER),          0),
                                 0x007c : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.f,      AddressMode.REGISTER),          0),
                                 0x007d : (Load_8b, (4,  self.a, AddressMode.REGISTER,  self.l,      AddressMode.REGISTER),          0),
                                 0x007e : (Load_8b, (7,  self.a, AddressMode.REGISTER,  self.hl,     AddressMode.REGISTER_INDIRECT), 0),
                                 0x000a : (Load_8b, (7,  self.a, AddressMode.REGISTER,  self.bc,     AddressMode.REGISTER_INDIRECT), 0),
                                 0x001a : (Load_8b, (7,  self.a, AddressMode.REGISTER,  self.de,     AddressMode.REGISTER_INDIRECT), 0),
                                 0x7efd : (Load_8b, (19, self.a, AddressMode.REGISTER,  self.ix,     AddressMode.INDEXED),           1),
                                 0X7edd : (Load_8b, (19, self.a, AddressMode.REGISTER,  self.iy,     AddressMode.INDEXED),           1),
                                 0x3afd : (Load_8b, (13, self.a, AddressMode.REGISTER,  self.memsys, AddressMode.EXT_ADDRESS),       2),
                                 0x2efd : (Load_8b, (7,  self.a, AddressMode.REGISTER,  None,        AddressMode.IMMEDIATE),         1)}
                                 

    def reset(self):
        """Resets the CPU"""
        pass

    def tick(self):
        """Clock Tick"""
        pass


