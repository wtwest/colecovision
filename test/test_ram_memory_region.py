"""Unit tests for RAM memory regions"""

import unittest
import random
from colecovision.memory import RAM_MemoryRegion


class TestMemoryRegion(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verify_length_1(self):
        """verify the length of the region is correct"""

        LENGTH = 1024

        mem = RAM_MemoryRegion(LENGTH)

        self.assertEqual(mem.length, LENGTH)

    def test_verify_length_2(self):
        """verify an exception is raised creating a region with 0 bytes"""

        LENGTH = 0

        with self.assertRaises(AssertionError):
            mem = RAM_MemoryRegion(LENGTH)  # lint:ok

    def test_verify_contents(self):
        """verify the contents of the memory region"""

        LENGTH = 1024

        ram_contents = [random.randint(0, 255) for x in range(LENGTH)]

        mem = RAM_MemoryRegion(LENGTH)

        for i in range(LENGTH):
            mem.write(i, ram_contents[i])

        for i in range(LENGTH):
            self.assertEqual(ram_contents[i], mem.read(i))

    def test_verify_read_error(self):
        """verify error is raised if we try to read from an invalid address"""

        LENGTH = 1024

        ram_contents = [random.randint(0, 255) for x in range(LENGTH)]

        mem = RAM_MemoryRegion(LENGTH)

        for i in range(LENGTH):
            mem.write(i, ram_contents[i])

        with self.assertRaises(IndexError):
            mem.read(-1)

        with self.assertRaises(IndexError):
            mem.read(LENGTH)

    def test_verify_write_error(self):
        """verify error is raised if we try to write to an invalid address"""

        LENGTH = 2048

        ram_contents = [random.randint(0, 255) for x in range(LENGTH)]

        mem = RAM_MemoryRegion(LENGTH)

        for i in range(LENGTH):
            mem.write(i, ram_contents[i])

        with self.assertRaises(IndexError):
            mem.write(-1, 0xff)

        with self.assertRaises(IndexError):
            mem.write(LENGTH, 0xff)

    def test_write_invalid_data(self):
        """verify we can only write 8 bits of data"""

        LENGTH = 2048

        mem = RAM_MemoryRegion(LENGTH)

        with self.assertRaises(OverflowError):
            mem.write(0, 1234)

        with self.assertRaises(OverflowError):
            mem.write(0, -1)

        with self.assertRaises(OverflowError):
            mem.write(0, 256)
