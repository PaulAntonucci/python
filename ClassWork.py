class peakData:

    #what's the difference between the approaches below???
    
    # def __init__(self):
    #   self.frequency = 1.2345
    # amplitude = 4.567
    #   self.molecule = "none"
    # assigned = 0
    #   self.stuffs = []
    frequency = 1.234
    amplitude = .1234
    matchingMolecules = 0  # what does it look like?  up to how many characters??
        # how many molecules????
    width = 100 # e.g. pixels
    artifact = False
    contaminant = False
    matchingMoleculeNames = 'none yet','not yet'
    stuffs = []
    # ? a "type", artifact, contamination, molecule, more than one molecule . . .

    # or should this be a numpy array? 






class molecule:
    name = "hydrocarbon"
    # linelist = [frequency, amplitude, uncertainty, noise??

class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
print(d.tricks)

d.tricks = 'abcd','234'
#e.tricks = 'that','this'
print (d.tricks)
print (e.tricks)


    
a = peakData()
b = peakData()
c = peakData()
a.frequency = 2.6
b.frequency = 3.12

a.stuffs = 'hi there', 'how are you'
b.stuffs = 'I', 'do not', 'like it'

print(b.stuffs[2])

print (a.frequency)
print (b.frequency)
print (c.frequency)

a.frequency = 9.9
b.frequency = 10.9

print (a.frequency)
print (b.frequency)
print (c.frequency)

print (a.stuffs)
print (b.stuffs)
print (c.stuffs)

a.molecule = 'the old one'
print (a.molecule)
b.molecule = 'a new one'

if'c' in vars():
    print ("c the variable exists - it's here")
    if(hasattr(c,'molecule')):
       print('  c  has the molecule attribute')
else:
    print("c  not found")

if 'a' in locals():
    print ("checking on the variable   a  - it's here")
    if(hasattr(a,'molecule')):
       print(' a has the molecule attribute')
else:
    print("a not found")

print (a.molecule)
print (b.molecule)
print (c.molecule)

arrayOfPeakData = [peakData() for i in range (0,12)]


for i in range(0,10):
    arrayOfPeakData[i].frequency = 3+i
    arrayOfPeakData[i].molecule = 'mol '+str(i)
    arrayOfPeakData[i].stuffs = arrayOfPeakData[i].stuffs,  'me',  str(i)
    print ('internal printing' + arrayOfPeakData[i].molecule)
    

for i in range(0,11):
    print (str(i))
    print (arrayOfPeakData[i].molecule)
    print ("freq = " + str(arrayOfPeakData[i].frequency))
    print (arrayOfPeakData[i].stuffs)

arrayOfPeakData[1].frequency = 2.34

for i in range(0,10):
    print (str(i))
    print (arrayOfPeakData[i].molecule)
    print ("freq = " + str(arrayOfPeakData[i].frequency))
    print (arrayOfPeakData[i].stuffs)





