"""Z80 microprocessor emulation"""

import logging

from colecovision.emulate.cpu.register import Register, CompositeRegister


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
        """Initialize the Z80 emulation"""

        self.pc    = Register(length=16, init_value=0)
        self.sp    = Register(length=16, init_value=0)
        self.ix    = Register(length=16, init_value=0)
        self.iy    = Register(length=16, init_value=0)
        self.i     = Register(length=8,  init_value=0)
        self.r     = Register(length=8,  init_value=0)
        self.a     = Register(length=8,  init_value=0)
        self.a_alt = Register(length=8,  init_value=0)
        self.f     = Register(length=8,  init_value=0)
        self.f_alt = Register(length=8,  init_value=0)
        self.b     = Register(length=8,  init_value=0)
        self.b_alt = Register(length=8,  init_value=0)
        self.c     = Register(length=8,  init_value=0)
        self.c_alt = Register(length=8,  init_value=0)
        self.d     = Register(length=8,  init_value=0)
        self.d_alt = Register(length=8,  init_value=0)
        self.e     = Register(length=8,  init_value=0)
        self.e_alt = Register(length=8,  init_value=0)
        self.h     = Register(length=8,  init_value=0)
        self.h_alt = Register(length=8,  init_value=0)
        self.l     = Register(length=8,  init_value=0)
        self.l_alt = Register(length=8,  init_value=0)

        # composite registers
        self.bc     = CompositeRegister(self.b, self.c)
        self.bc_alt = CompositeRegister(self.b_alt, self.c_alt)
        self.de     = CompositeRegister(self.d, self.e)
        self.de_alt = CompositeRegister(self.d_alt, self.e_alt)
        self.hl     = CompositeRegister(self.h, self.l)
        self.hl_alt = CompositeRegister(self.h_alt, self.l_alt)

        self.memory = memory_system

    def reset(self):
        """Resets the CPU"""
        pass

    def tick(self):
        """Clock Tick"""
        pass


