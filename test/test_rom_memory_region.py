"""Unit tests for ROM memory regions"""

import os
import random
import struct
import unittest
from colecovision.memory import ROM_MemoryRegion


class TestMemoryRegion(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_rom_file(self, name, length):

        # create a list of random numbers to be used
        # as contents for the ROM file
        file_contents = [random.randint(0, 255) for x in range(length)]

        # create/open the ROM file
        with open(name, 'wb') as f:

            # write the list of random numbers to the ROM file
            for val in file_contents:
                write_val = struct.pack('B', val)
                f.write(write_val)

        # return the list of random numbers we used for the
        # contents of the ROM file
        return file_contents

    def delete_rom_file(self, name):
        os.remove(name)

    def test_verify_length_1(self):
        """verify the length of the memory region is correct"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 10

        self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        # verify the length
        self.assertEqual(ROM_LENGTH, mem.length)

        self.delete_rom_file(ROM_FILE)

    def test_verify_length_2(self):
        """verify the length of the memory region is correct"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 0

        self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        # verify the length
        self.assertEqual(ROM_LENGTH, mem.length)

        self.delete_rom_file(ROM_FILE)

    def test_verify_contents_1(self):
        """verify the contents of 1K the memory region"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 1024

        rom_content = self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        # verify the length
        self.assertEqual(ROM_LENGTH, mem.length)

        # verify the contents
        for i in range(len(rom_content)):
            self.assertEqual(rom_content[i], mem.read(i))

        self.delete_rom_file(ROM_FILE)

    def test_verify_contents_2(self):
        """verify the contents of 8K the memory region"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 8192

        rom_content = self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        # verify the length
        self.assertEqual(ROM_LENGTH, mem.length)

        # verify the contents
        for i in range(len(rom_content)):
            self.assertEqual(rom_content[i], mem.read(i))

        self.delete_rom_file(ROM_FILE)

    def test_verify_contents_3(self):
        """verify the contents of 0K the memory region"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 0

        rom_content = self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        # verify the length
        self.assertEqual(ROM_LENGTH, mem.length)

        # verify the contents
        for i in range(len(rom_content)):
            self.assertEqual(rom_content[i], mem.read(i))

        self.delete_rom_file(ROM_FILE)

    def test_no_write_support(self):
        """verify that writes to ROM fail"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 8192

        self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        # verify writes fail

        with self.assertRaises(NotImplementedError):
            mem.write(0, random.randint(0, 255))

        with self.assertRaises(NotImplementedError):
            mem.write(4096, random.randint(0, 255))

        with self.assertRaises(NotImplementedError):
            mem.write(8191, random.randint(0, 255))

        self.delete_rom_file(ROM_FILE)

    def test_read_out_of_range(self):
        """verify reads fail if an address out of range is specified"""

        # ROM file info (name, length)
        ROM_FILE = 'romtest.rom'
        ROM_LENGTH = 8192

        self.create_rom_file(ROM_FILE, ROM_LENGTH)

        mem = ROM_MemoryRegion(ROM_FILE)

        with self.assertRaises(IndexError):
            mem.read(ROM_LENGTH)

        with self.assertRaises(IndexError):
            mem.read(-1)

        self.delete_rom_file(ROM_FILE)
