"""Unit tests for the load instructions (8 and 16 bit)"""

import unittest
import colecovision.cpu.instruction
from colecovision.cpu.instruction import LoadError, Load_8b, AddressMode 
from colecovision.cpu.register import Register, CompositeRegister
from colecovision.memory import RAM_MemoryRegion

class TestLoadInstruction(unittest.TestCase):
    """Base class for load instruction test cases"""
    
    def setUp(self):
        """Setup CPU registers and memory for testing"""
        
        self.register = {}

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

        self.RAM_LENGTH = 1024
        
        self.ram = RAM_MemoryRegion(self.RAM_LENGTH)
        
        for i in range(self.RAM_LENGTH):
            self.ram.write(i, 0)
        

class TestRegisterToRegisterExecution(TestLoadInstruction):
    """Tests for register->register load instruction execution"""
    
    def setUp(self):
               
        TestLoadInstruction.setUp(self)
        
        self.MODE = (AddressMode.REGISTER, AddressMode.REGISTER)

        self.instruction = Load_8b(self.register, self.ram, self.MODE, self.register['A'], self.register['B'])
        
        self.source = self.register['A']
        self.destination = self.register['B']

        self.CYCLES = 4

    def test_verify_cycles(self):

        self.assertEqual(self.instruction.cycles, self.CYCLES)

    def test_verify_cycle_countdown(self):

        for i in range(self.CYCLES - 1):
            self.instruction.execute()
            self.assertNotEqual(self.instruction.complete, True)

        self.instruction.execute()
        self.assertEqual(self.instruction.complete, True)

    def test_execution(self):

        load_value = 0xab

        self.register['A'].value = load_value

        self.assertNotEqual(self.register['B'].value, load_value)

        for i in range(self.CYCLES - 1):
            self.instruction.execute()
            self.assertNotEqual(self.register['B'].value, load_value)

        self.instruction.execute()
        
        self.assertEqual(self.instruction.complete, True)
        
        self.assertEqual(self.register['B'].value, load_value)

class TestRegisterToRegisterDecode(TestLoadInstruction):
    """Tests for decoding register->register load instructions"""
    
    def setUp(self):
        
        TestLoadInstruction.setUp(self)
        
    def test_unknown_register(self):
        """Verify that an exception is raised if a load instruction
        is decoded and one of the registers (source, destination) is
        unknown.
        """
        
        load_instruction = colecovision.cpu.instruction.LOAD_8B_REGISTER_TO_REGISTER
        
        bad_register_id = 6
        
        load_instruction = load_instruction | (bad_register_id << 3)
        
        load_instruction = load_instruction | bad_register_id
        
        self.ram.write(0, load_instruction)
        
        self.assertEqual(self.ram.read(0), load_instruction)
        
        self.register['PC'].value = 0
        
        with self.assertRaises(colecovision.cpu.instruction.UnknownRegisterError):
            
            bytes_read, created_instruction = colecovision.cpu.instruction.create(self.register, self.ram)
        
        
        
        