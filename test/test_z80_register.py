"""Unit tests for Z80 registers"""

import unittest
from colecovision.cpu.register import Register, CompositeRegister

class TestRegister(unittest.TestCase):

    def test_initialization_empty(self):
        reg = Register()
        self.assertEqual(reg.length, 8)
        self.assertEqual(reg.value, 0)

    def test_initialization_specific(self):
        reg_len = 16
        reg_val = 12
        reg = Register(length=reg_len, init_value=reg_val)
        self.assertEqual(reg.length, reg_len)
        self.assertEqual(reg.value, reg_val)


