'''
Created on Oct 29, 2012

@author: bxs003
'''
'''
Created on Mar 15, 2012

@author: bxs003
'''
'''
Created on Mar 11, 2012

@author: bxs003
'''

import math

test_header = '''\
1 1,2 2,3 3,4 4,5 5,6 6,7 7,8 8,9 9,
10 10,11 11,12 12,13 13,14 14,15 15,16 16,17 17,18 18,19 19,
20 20,21 21,22 22,23 23,24 24,25 25,26 26,27 27,28 28,29 29,
30 30,31 31,32 32,33 33,34 34,35 35,36 36,37 37,38 38,39 39,
40 40,41 41,42 42,43 43,44 44,45 45,46 46,47 47,48 48,49 49,
50 50,51 51,52 52,53 53,54 54,55 55,56 56,57 57,58 58,59 59,
60 60,61 61,62 62,63 63,64 64,65 65,66 66,67 67,68 68,69 69,
70 70,71 71,72 72,73 73,74 74,75 75,76 76,77 77,78 78,79 79,
80 80,81 81,82 82,83 83,84 84,85 85,86 86,87 87,88 88,89 89,
90 90,91 91,92 92,93 93,94 94,95 95,96 96,97 97,98 98,99 99,
100 100,101 101,102 102,103 103,104 104,105 105,106 106,107 107,108 108,109 109,
110 110,111 111,112 112,113 113,114 114,115 115,116 116,117 117,118 118,119 119,
120 120,121 121,122 122,123 123,124 124,125 125,126 126,127 127,128 128;
OOOOIIIIIIIIIIIIIIIIIIIIIOOOOOOOOOOOOOOIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO;
*                                                                                                                11111111111111111111111111111*
* CHANNEL              11111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111222222222*
*  NUMBER     12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678*
'''

def build_pin_dict():
    pin_dict = {}
    
    for i in xrange(15):
        pin_dict['IP('+str(i)+')'] = i+6
        
    pin_dict['IP(15)'] = 22
        
    pin_dict['RESET'] = 5
    pin_dict['CE'] = 23
    pin_dict['CS'] = 25
    pin_dict['CLOCK'] = 24
    
    pin_dict['VDD'] = 21
    pin_dict['GND'] = 40
    
    # Output Pins
    pin_dict['NC_0'] = 26
    pin_dict['NC_1'] = 27
    
    for i in xrange(28, 40, 1):
        pin_dict['OP('+str((28-i)+15)+')'] = i
    
    pin_dict['OP(0)'] = 4
    pin_dict['OP(1)'] = 3
    pin_dict['OP(2)'] = 2
    pin_dict['OP(3)'] = 1
    
#    for key in pin_dict:
#        print key + ': ' + str(pin_dict[key])
    
    return pin_dict

def reverseStr(str):
    rev = ''
    lstr = len(str)
    for i in xrange(lstr):
        rev += str[lstr-1-i]
    
    return rev
       
def sig(name, id):
    return str(name + '(' + str(id) + ')')

def vector_comment(index, space=5):
    extra = space - len(str(index))
    cmt = '*Vector' + ' '*extra + str(index)
    return cmt + '* '

def build_nums(mult_nums):
    mult_pairs = []
    for i in xrange(0, len(mult_nums), 8):
        num1 = int(mult_nums[i: i+4], 16)
        num2 = int(mult_nums[i+4: i+8], 16)
        mult_pairs.append((num1, num2))
        
    return mult_pairs

class ChipTest:
    def __init__(self, path, hex_path, pin_dict):
        self._vector = 0
        self._file = open(path, 'w')
        self._hexfile = open(hex_path, 'w')
        self.pin_dict = pin_dict
        
        self.pin_states = []
        self.pin_state_str = ''
        for i in xrange(129):
            self.pin_state_str = '0'
            self.pin_states.append(0)
            
        self.x = 0
        self.y = 0
            
        self.mark_valid = False
        
    def close(self):
        self._file.close()
        self._hexfile.close()

    def initChip(self):
        self.markInvalid()
        self.writeComment('Force file for testing the 16x16 Multiplier Chip')
        self._file.write(test_header)
        
        #self.writeComment('Init Chip')
        self.force('VDD', 1)
        self.force('GND', 0)
        self.setBus('IP', 16, 0)
        self.force('RESET', 1)
        self.force('CE', 0)
        self.force('CS', 0)
        self.force('CLOCK', 0)
        self.commit_signals()
        
        self.cycleCLK()
        
        self.force('RESET', 0)
        
        self.markValid()
        self.commit_signals()
        self.markInvalid()
        
    def markValid(self):
        self.mark_valid = True
        
    def markInvalid(self):
        self.mark_valid = False

    def multiply(self, x, y):
        self.x = x
        self.y = y
        #self.writeComment('Answer in QUICKSIM HEX Format! ->  ' + hexAns(x*y))
        
        #self.writeComment('Clock in X')
        self.setBus('IP', 16, x)
        self.force('CE', 0)
        self.commit_signals()
        self.cycleCLK()
        
        #self.writeComment('Clock in Y')
        self.setBus('IP', 16, y)
        self.force('CE', 1)
        self.commit_signals()
        self.cycleCLK()
        
        #self.writeComment('Load into Output Register, Show Low Word First')
        self.force('CS', 0)
        self.cycleCLK(True)
        
        #self.writeComment('Show High Word')
        self.force('CS', 1)
        self.commit_signals()
        self.markInvalid()
    
    def cycleCLK(self, half_clk_valid = False):
        self.force('CLOCK', 1)
        self.commit_signals()
        
        if half_clk_valid:
            self.markValid()
            
        self.force('CLOCK', 0)
        self.commit_signals()
        
    def commit_signals(self):
        self._set_output_pins()
        
        self._make_pin_state_str()
        self._write_hexline()
        
        self._set_output_pins_low()
        self._make_pin_state_str()
        self._file.write(vector_comment(self._vector) + self.pin_states_str[1:] + '\n')
        
        self._vector += 1
        
    def _make_pin_state_str(self):
        self.pin_states_str = 'x'
        for i in xrange(1,129):
            self.pin_states_str += str(self.pin_states[i])
        
    def _set_output_pins(self):
        ans = self.x*self.y
        binstr = bin(ans)[2:]
        binstr = (32-len(binstr))*'0'+binstr
        binstr = binstr[::-1] # reverse the string
        
        low = binstr[0:16]
        high = binstr[16:]
        
        output = low
        if self.pin_states[self.pin_dict['CS']] == 1:
            output = high
            
        for i in xrange(16):
            self.pin_states[self.pin_dict['OP('+str(i)+')']] = output[i]
            
        # These are always high outputs
        self.pin_states[self.pin_dict['NC_0']] = 1
        self.pin_states[self.pin_dict['NC_1']] = 1
        
    def _set_output_pins_low(self):
        for i in xrange(16):
            self.pin_states[self.pin_dict['OP('+str(i)+')']] = 0
        
        self.pin_states[self.pin_dict['NC_0']] = 0
        self.pin_states[self.pin_dict['NC_1']] = 0
        
    def _write_hexline(self):
        hexstr = hex(int(self.pin_states_str[1:41], 2))
        if hexstr.find('L') == -1:
            hexstr = hexstr[2:len(hexstr)]
        else:
            hexstr = hexstr[2:len(hexstr)-1]
        
        hexstr = (10-len(hexstr))*'0'+hexstr
        hexstr = hexstr.upper()
        
        valid = ''
        if self.mark_valid:
            valid = ' ***Valid Output***'
        
        self._hexfile.write(str(self._vector) + ': x'+hexstr+str(valid)+'\n')
    
    def writeComment(self, cmt):
        self._file.write('*' + cmt + '*\n')
    
    def setBus(self, name, size, value):
        binstr = bin(value)
        binstr = binstr[2:len(binstr)]
        binstr = reverseStr(binstr)
    
        for i in xrange(size):
            if i < len(binstr):
                val = int(binstr[i])
            else:
                val = 0
            self.force(sig(name, i), val)
    
    def force(self, name, value):
        pin_id = self.pin_dict[name]
        self.pin_states[pin_id] = value
    
def write_test_file(vector_path, output_path):
    # List of random 16 bit numbers to multiply (all the numbers are just concatenated together)
    # The list is broken into pairs by the build_nums function
    mult_nums = '4e2a93bfb82c25f1ed008f4270cf56b53aad8e9501f8307d4397fa84f2cd50b2'
    
    if len(mult_nums) % 8 != 0:
        print 'mult_nums needs to be a multiple of 8 in length'
        print len(mult_nums)
        exit(-1)
        
    mult_pairs = build_nums(mult_nums)
    
    pin_dict = build_pin_dict()
    test = ChipTest(vector_path, output_path, pin_dict)
    test.initChip()
    test.multiply(1, 1)
    
    for pair in mult_pairs:
        test.multiply(pair[0], pair[1])
        
    test.close()

if __name__ == '__main__':
    write_test_file('mult16.tst', 'hex_outs.txt')