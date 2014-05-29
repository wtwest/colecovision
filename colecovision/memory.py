"""Memory subsystem for the Colecovision"""


import abc
import array
import logging
import os
import struct


#-----------------------------------------------------------------------------
# Logging Configuration
#-----------------------------------------------------------------------------

_logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Interfaces
#-----------------------------------------------------------------------------


class MemoryRegionInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write(self, address, value):
        """Write a value to memory"""
        pass

    @abc.abstractmethod
    def read(self, address):
        """Read a value from memory"""
        pass

    @property
    def length(self):
        """Length of the memory region"""
        return self._length


class MemorySystemInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write(self, address, value):
        """Write a value to memory"""
        pass

    @abc.abstractmethod
    def read(self, address):
        """Read a value from memory"""
        pass

    @abc.abstractmethod
    def dump(self, start_address, end_address, file_name):
        """Dump the memory specified by the range to a file"""
        pass

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------


class ROM_MemoryRegion(MemoryRegionInterface):
    """Read-only memory region"""

    def __init__(self, file_name):
        """Initialization"""

        # open the file and save the file name
        self._rom_file = open(file_name, 'rb')
        self._rom_file_name = file_name

        # get the length (size) of the file
        stat_info = os.stat(self._rom_file_name)
        self._length = stat_info.st_size

    def __del__(self):
        """Closes the ROM file"""
        if self._rom_file:
            self._rom_file.close()

    def __repr__(self):
        """Returns a string to re-create the object"""
        return 'ROM_MemoryRegion({0})'.format(self._rom_file_name)

    def write(self, address, value):
        """Write a vaue to memory"""
        err_msg = 'Writing to ROM not supported, {0}'
        err_msg = err_msg.format(self._rom_file_name)
        raise NotImplementedError(err_msg)

    def read(self, address):
        """Read a value from memory"""

        if (address < 0) or (address >= self.length):
            raise IndexError('Address {0} is invalid'.format(address))

        # move to the correct offset within in the file
        self._rom_file.seek(address)

        # read a byte (returned as a string)
        read_value = self._rom_file.read(1)

        # convert the read value from a string to an integer
        result, = struct.unpack('B', read_value)

        return result

    @property
    def file_name(self):
        """File name of the ROM file"""
        return self._rom_file_name


class RAM_MemoryRegion(MemoryRegionInterface):
    """Read/Write memory region"""

    def __init__(self, size_bytes):
        """Initialization"""

        assert(size_bytes > 0)

        self._length = size_bytes

        # create an array to represent the memory
        self._memory = array.array('B')

        # fill in the memory with default values
        for i in range(size_bytes):
            self._memory.append(0xff)

    def __repr__(self):
        """Returns a string to re-create the object"""
        return 'RAM_MemoryRegion({0})'.format(self._length)

    def write(self, address, value):
        """Write a value to memory"""

        if (address < 0) or (address >= self.length):

            raise IndexError('Address {0} is invalid'.format(address))

        self._memory[address] = value

    def read(self, address):
        """Read a value from memory"""

        if (address < 0) or (address >= self.length):
            raise IndexError('Address {0} is invalid'.format(address))

        return self._memory[address]


class _MemoryRegionMapper(object):
    """Given a dictionary of memory regions and a memory address,
       presents the memory region that maps to the given address
       along with the memory-region specific address to use"""

    def __init__(self, mem_regions, mem_address):
        """Find the memory region that maps to the given address"""

        self._region = None
        self._region_address = 0

        if (mem_regions) and (mem_address >= 0):
        
            last_base_address_found = 0

            for base_address in mem_regions:
            
                if base_address <= mem_address:
                
                    if base_address > last_base_address_found:
                    
                        last_base_address_found = base_address

            if last_base_address_found in mem_regions:
            
                self._region = mem_regions[last_base_address_found]
                self._region_address = mem_address - last_base_address_found

    @property
    def address(self):
        """Memory Region address to use"""
        return self._region_address

    @property
    def region(self):
        """Memory Region to use"""
        return self._region

class MemorySystem(MemorySystemInterface):
    """Provides a single interface to several memory regions"""

    def __init__(self, data_bus_width=8):
        """Initializes the memory system"""

        self._bus_width = data_bus_width

        self._region = {}

    def __repr__(self):
        """Returns a string to re-create the object"""
        return 'MemorySystem(data_bus_width={0})'.format(self._bus_width)


    def write(self, address, value):
        """Write a value to memory"""

        assert(value <= ((2 ** self._bus_width) - 1))

        # Map given address to a specific memory region
        mem_map = _MemoryRegionMapper(self._region, address)

        if mem_map.region:
            
            mem_map.region.write(mem_map.address, value)

        else:

            ex_msg = "Writing to 0x{0} un-mapped address 0x{1}"

            raise RuntimeError(ex_msg.format(hex(value), hex(address)))


    def read(self, address):
        """Read a value from memory"""
        
        # Map given address to a specific memory region
        mem_map = _MemoryRegionMapper(self._region, address)

        if mem_map.region:

            value_read = mem_map.region.read(mem_map.address)

            return value_read

        else:

            ex_msg = "Reading from un-mapped address 0x{0}"

            raise RuntimeError(ex_msg.format(hex(address)))


    def map_region(self, mem_region, address):
        """Map a memory region into memory"""

        if self._region.has_key(address):
            
            _logger.warning("Mapping address that is already mapped")

        _logger.info("Mapping address 0x{0}".format(hex(address)))

        self._region[address] = mem_region

    def unmap_region(self, mem_region):
        """Remove a memory region's mapping in memory"""
        
        for k in self._region.keys():
            
            if self._region[k] == mem_region:
                
                _logger.info("Un-mapping address 0x{0}".format(hex(k)))

                self._region.pop(k)

                break

    def dump(self, start_address, end_address, file_name):
        """Dump the memory specified by the range to a file"""
        
        BYTES_PER_LINE = 4

        with open(file_name, "w") as f:

            for address in range(start_address, end_address, BYTES_PER_LINE):

                address_string = '{0:08X}'.format(address)

                f.write(address_string + ": ")

                for offset in range(BYTES_PER_LINE):
                  
                    value_string = "--"

                    try:

                        dump_value = self.read(address + offset)

                        value_string = '{0:02X}'.format(dump_value)

                    except:

                        pass

                    f.write(value_string)

                f.write("\n")
