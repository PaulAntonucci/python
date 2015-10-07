#!/usr/bin/env python3


def pollynomial(x,y,z):
    some = 2*(x**2) + 3*x*y + 4*z
    some -= 1
    return some

from math import *

list = [ 2,'help',3.25,4,5,9]

noun = {}
noun[1] = "dog"
noun['ab'] = 'abbreviate'
noun['la'] = 'flab'


pi = 3.141592653589793

for k in range(0,5):
    print(' k= ' +str(k))
    x = 2*k
    y = 3.2*k
    z = 2*x - 2*y
    intermediate = pollynomial(x,y,z)
    print('polly who? ' + str(intermediate))
    print (list[k])

print(list)
print(' sin pi = ' + str(sin(pi)))
print(' sin pi/4 = ' + str(sin(pi/4)))
print('arc cos 0 = '  + str(2*acos(0)))
print ('arc sin 1 =' + str(2*asin(1)))

print (noun['ab'])
print (str(355.0/113))
       

string = 'Hello World'
for x in string:
    if x =='o':
        break
    print (x)


import time

start = time.clock()
print (start)
for x in range (0,1000):
    pass
stop = time.clock()
print ('stop - start, 1000 passes ' + str(stop - start))

start = time.clock()
print (start)
for x in range (0,1000000):
    pass
stop = time.clock()
print ('stop - start, e6 passes ' +str(stop - start))
start = time.clock()

while time.clock() < 10:
    if(time.clock() - start) > 1.0:
        start = time.clock()
        print (start)

print ('Done - time = ' + str(time.clock()))


    
    
