#import numpy
import random
import sys
import math

#if test = 1 testing function activates
test = 1

def TESTING():
    if(not test):
        return
    #put here testing code
    print("enviar_hamming('1101')")            
    enviar_hamming('1101')
    print('----------------------')
    print("recibir_hamming('1010101')")
    recibir_hamming('1010101')
    print('----------------------')
    print("recibir_hamming('1010001')")
    recibir_hamming('1010100')
    print('----------------------')
    

###################################################################
##INICIO enviar_humming
###################################################################

#Calculate humming code for given binary int stream
def enviar_hamming(binaryStream):
    
    binaryStream = constructBinList(binaryStream)
    powCount = 0
    pos = 0
    for data in binaryStream:
        if(data == 2):
            binaryStream[pos] = xorParity(binaryStream,powCount)
            powCount+=1
        pos+=1
        
    intReturn = 0
    intPow = 0
    binaryStream.reverse()
    
    for data in binaryStream:
        intReturn += data *(10**intPow)
        intPow+=1
    print(intReturn)
    return intReturn
        

#Build the Primary list with 2 representing pows of 2 and datastream
def constructBinList(binaryStream):
    binOutList = []
    for digit in str(binaryStream):
        binOutList.append(int(digit))
        
    binaryStream = binOutList
    binOutList = []
    
    twoPow = 0 #current pow of 2 used
    currDpos = 0 #current position in dataStream
    dAmount = 0 #amount of data used

    #while there are items in binary stream
    while (currDpos<len(binaryStream)):
        binOutList.append(2)
        while ((dAmount+1)<int(math.pow(2,twoPow)) and currDpos<len(binaryStream)):
            binOutList.append(binaryStream[currDpos])
            currDpos+=1
            dAmount+=1
        twoPow+=1
        dAmount=0
    return binOutList

def xorParity(binaryList,twoPow):
    #find initial position
    initial = int(math.pow(2,twoPow))-1
    jumpread = int(math.pow(2,twoPow))

    trimList = binaryList[initial:]
    
    returnList = trimParityRec(trimList,jumpread)
    
    returnList = returnList[1:]

    acumulatedXor = returnList[0]
    for data in returnList[1:]:
        acumulatedXor = bool(data) ^ bool(acumulatedXor)

    if(acumulatedXor):return 1
    else: return 0

    
  

def trimParityRec(binaryList,jumpread):
    if(len(binaryList) == 0): return []
    binaryListA = binaryList[:jumpread]
    binaryListB = binaryList[jumpread*2:]
    returnList = []
    for data in binaryListA:
                   returnList.append(data)
    return returnList + trimParityRec(binaryListB,jumpread)

###################################################################
##end enviar_humming
###################################################################

###################################################################
##inicio recibir_humming
###################################################################

def recibir_hamming(bitStream):
    bitStreamFixed = constructBinList2(bitStream)
    bitStream.split()
    clearBitStream = []
    failureList = []
    powCount = 0
    pos = 0
    failure = 0
    for data in bitStream:
        if((pos+1)==(2**powCount)):
            if(int(data) != int(xorParity(bitStreamFixed,powCount))):
                failure+=1
                failureList.append(powCount)
            powCount+=1
        else:
            clearBitStream.append(data)
        pos+=1

    
    print(failureList)

    intReturn = 0
    intPow = 0
    clearBitStream.reverse()
    
    for data in clearBitStream:
        intReturn += int(data) *(10**intPow)
        intPow+=1
    
    print(intReturn)

def constructBinList2(binaryStream):
    binOutList = []
    for digit in str(binaryStream):
        binOutList.append(int(digit))
        
    binaryStream = binOutList
    binOutList = []
    
    twoPow = 0 #current pow of 2 used
    currDpos = 0 #current position in dataStream
    dAmount = 0 #amount of data used

    #while there are items in binary stream
    while (currDpos<len(binaryStream)):
        binaryStream[currDpos] = 2
        currDpos+=1
        while ((dAmount+1)<int(math.pow(2,twoPow)) and currDpos<len(binaryStream)):
            currDpos+=1
            dAmount+=1
        twoPow+=1
        dAmount=0
    return binaryStream

###################################################################
##end recibir_humming
###################################################################
    
###################################################################
##TEST ZONE
###################################################################

TESTING()
