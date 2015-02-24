'''
Created on Mar 15, 2012

@author: bxs003
'''
'''
Created on Mar 11, 2012

@author: bxs003
'''

import math

def hexAns(ans):
    binstr = bin(ans)
    binstr = binstr[2:len(binstr)]
    pad = (32-len(binstr))*'0'
    binstr = pad + binstr
    
    binstr = reverseStr(binstr)
    
    hi = binstr[0:16]
    lo = binstr[16:]
    
    hi_out = str(hex(int(hi,2)))
    lo_out = str(hex(int(lo,2)))
    out =  hi_out[2:] + ' ' + lo_out[2:]
    return out.upper()

def reverseStr(str):
    rev = ''
    lstr = len(str)
    for i in xrange(lstr):
        rev += str[lstr-1-i]
    
    return rev
       
def sig(name, id):
    return str(name + '(' + str(id) + ')')

def build_nums(mult_nums):
    mult_pairs = []
    for i in xrange(0, len(mult_nums), 8):
        num1 = int(mult_nums[i: i+4], 16)
        num2 = int(mult_nums[i+4: i+8], 16)
        mult_pairs.append((num1, num2))
        
    return mult_pairs

class ChipTest:
    def __init__(self):
        self._time = 1.0
        self._file = open('chip.force', 'w')
        
    def close(self):
        self._file.write('run ' + str(self._time))
        self._file.close()

    def initChip(self):
        self.writeComment('Force file for testing the 16x16 Multiplier Chip')
        self._file.write('\n')
        
        self._file.write('$unload_wdb("forces", @nosave, "", @noreplace, @noviewpoint);\n')
        self._file.write('delete traces RESET CE CS CLK IP[0:15] X[0:15] Y[0:15] Z[0:31] OP[0:15]\n')
        self._file.write('reset state -d\n')
        self._file.write('add traces RESET CE CS CLK IP[0:15] X[0:15] Y[0:15] Z[0:31] OP[0:15]\n')
        
        self.setBus('IP', 16, 0)
        self.force('RESET', 1)
        self.force('CE', 0)
        self.force('CS', 0)
        self.force('CLOCK', 0)
        
        self.cycleCLK(10)
        
        self._time += 10
        self.force('RESET', 0)
        self._time += 10

    def multiply(self, x, y):
        sep = '--------------------------------'
        self.writeComment(sep)
        self.writeComment('Answer in QUICKSIM HEX Format! ->  ' + hexAns(x*y))
        self.writeComment(sep)
        
        self.writeComment('Clock in X')
        self.setBus('IP', 16, x)
        self.force('CE', 0)
        self.cycleCLK(10)
        
        self.writeComment('Clock in Y')
        self.setBus('IP', 16, y)
        self.force('CE', 1)
        self.cycleCLK(10)
        
        self.writeComment('Load into Output Register, Show Low Word First')
        self.force('CS', 0)
        self.cycleCLK(10)
        
        self._time += 12
        self.writeComment('Show High Word')
        self.force('CS', 1)
        self._time += 12
        
    
    def cycleCLK(self, half_period):
        self._time += half_period
        self.force('CLOCK', 1)
        self._time += half_period
        self.force('CLOCK', 0)
        return self._time
    
    def writeComment(self, cmt):
        self._file.write('//' + cmt + '\n')
    
    def setBus(self, name, size, value):
        binstr = bin(value)
        binstr = binstr[2:len(binstr)]
        binstr = reverseStr(binstr)
    
        for i in xrange(size):
            if i < len(binstr):
                val = binstr[i]
            else:
                val = 0
            self.force(sig(name, i), val)
    
    def force(self, signal, bit):
        self._file.write('FORCE ' + signal + ' ' + str(bit) + ' ' + str(self._time) + '\n')

if __name__ == '__main__':
    mult_nums = '4e2a93bfb82c25f1ed008f4270cf56b53aad8e9501f8307d4397fa84f2cd50b2'
    
    if len(mult_nums) % 8 != 0:
        print 'mult_nums needs to be a multiple of 8 in length'
        print len(mult_nums)
        exit(-1)
        
    mult_pairs = build_nums(mult_nums)
    
    print 'Begin Force File Write'
    test = ChipTest()
    test.initChip()
    
    test.multiply(1, 1)
    
    for pair in mult_pairs:
        test.multiply(pair[0], pair[1])
        
    test.close()
    print 'End Force File Write'