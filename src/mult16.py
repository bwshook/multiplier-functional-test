'''
Created on Mar 11, 2012

@author: bxs003
'''

def writeComment(cmt):
    file.write('//' + cmt + '\n')

def hexAns(ans):
    binstr = bin(ans)
    binstr = binstr[2:len(binstr)]
    pad = (32-len(binstr))*'0'
    binstr = pad + binstr
    
    binstr = reverseStr(binstr)
    
    even_inv = ''
    for i in xrange(len(binstr)):
        if i % 2 == 0:
            if binstr[i] == '1':
                even_inv += '0'
            else:
                even_inv += '1'
        else:
            even_inv += binstr[i]
    
    return str(hex(int(even_inv, 2)))
    
def setXY(x, y, time):
    sep = '--------------------------------'
    writeComment(sep)
    writeComment('Answer in QUICKSIM HEX Format! ->  ' + hexAns(x*y))
    writeComment(sep)
    setBus('X', 16, x, time)
    file.write('\n')
    setBus('Y', 16, y, time)

def reverseStr(str):
    rev = ''
    lstr = len(str)
    for i in xrange(lstr):
        rev += str[lstr-1-i]
    
    return rev

def sig(name, id):
    return str(name + '(' + str(id) + ')')

def setBus(name, size, value, time):
    binstr = bin(value)
    binstr = binstr[2:len(binstr)]
    binstr = reverseStr(binstr)

    for i in xrange(size):
        if i < len(binstr):
            val = binstr[i]
        else:
            val = 0
        force(sig(name, i), val, time)

def force(signal, bit, time):
    file.write('FORCE ' + signal + ' ' + str(bit) + ' ' + str(time) + '\n')

file = open('mult16.force', 'w')
writeComment('Force file for testing the 16x16 Multiplier (Combinational logic portion)')

setBus('X', 16, 0, 0.0)
file.write('\n')
setBus('Y', 16, 0, 0.0)

setXY(1245, 3697, 20.0)
setXY(48621, 12745, 40.0)
setXY(65535, 65535, 60.0)
    
file.close()