"""Z80 register functionality"""

class Register(object):
    """Z80 register"""

    def __init__(self, length=8, init_value=0):
        """Initialize the register length and value"""
        
        self._length = length
        
        self._value = ((2 ** self._length) - 1) & init_value 

    def __str__(self):
        """User friendly string representation of the object"""
        return hex(self._value)

    def __repr__(self):
        """Creates a string that can be used to re-create the object"""
        return 'Register(length={0}, init_value={1})'.format(self._length, self._value)

    @property
    def length(self):
        """Length of the register, in bits"""
        return self._length

    @property
    def value(self):
        """Value contained within the register"""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = ((2 ** self._length) - 1) & new_value

    
class CompositeRegister(object):
    """Register that is a composite of two individual registers"""

    def __init__(self, high, low):
        """Specify the two registers used to make a composite"""

        assert(low.length == high.length)

        self._low = low
        self._high = high

    @property
    def length(self):
        """Length of the register in bits"""
        return (self._low.length + self._high.length)
    
    @property
    def value(self):
        """Value contained within the register"""
        temp = self._high.value << self._high.length
        temp |= self._low.value
        return temp

    @value.setter
    def value(self, new_value):
        temp = ((2 ** self.length) - 1) & new_value
        self._high.value = temp >> self._high.length
        self._low.value = temp & ((2 ** self._low.length) - 1)
        
