def workingClear(ilist):
  del ilist[:]
def brokenClear(ilist):
  ilist = [] # Lets ilist point to a new list, losing the reference to the argument list
list1=[1, 2]; workingClear(list1); print (list1)
list1=[1, 2]; brokenClear(list1); print (list1)
print (list1[1] + list1[0])

maximumNumberOfFileLines = 30
LinesToWriteToFile=["hello there!" for i in range (maximumNumberOfFileLines)]

CrossLadderMatrix =[[0,2,3,4,5,6],[1,2,3,4,5,6,],[2,2,3,4,5,6,],[3,2,3,4,5,6,],[4,2,3,4,5,6,],[5,2,3,4,5,6,],[6,2,3,4,5,6,],[7,2,3,4,5,6]]
for index in range (0,len(LinesToWriteToFile)):
    lineToWrite = LinesToWriteToFile[index]
    print (lineToWrite)

    #print (lineToWrite[index])
 



for lindex in range (0,len(lineToWrite)):
    #for index in range (0,6):
        print (str(lineToWrite[lindex]))
        #print (str(CrossLadderMatrix[index,lindex]))
        
                  
