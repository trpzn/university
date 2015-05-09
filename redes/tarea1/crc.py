#CODED BY: Tomas Ramirez Dorner
#FOR: Redes

import random
import sys
import math

#if test = 1 Testing function activates
test = 1;

def TESTING():
    if(not test):
        return
    ##put here code to test
    cadena = '111010'
    print(cadena)
    polinomio = '101'
    print(polinomio)
    resultado = enviar_crc(cadena,polinomio)
    print('-------------------------------------')
    print(recibir_crc(resultado,polinomio))


#function calculate crc code of a given 'trama' with given 'polinomio'
#Inputs in binary
def enviar_crc(frame,polynom):
    frame = stringToList(frame,0)
    polynom = stringToList(polynom,0)
    polyGrad = len(polynom)-1
    addCeros(frame,polyGrad)
    remainder = divideReminder(frame,polynom)
    outputFrame = xor(frame,remainder,'right')
    outputFrame = stringToList(outputFrame,1)
    
    return outputFrame

def recibir_crc(frame,polynom):
    frame = stringToList(frame,0)
    polynom = stringToList(polynom,0)
    remainder = divideReminder(frame,polynom)

    if(len(remainder)==0):
        return 0
    else:
        return 1
    
    
def divideReminder(dividend,divisor):
    divisor = divisor.copy()
    dividend = dividend.copy()
    dividable = True
    currentDividend = dividend[:len(divisor)]
    restDividend = dividend[len(divisor):]
    while(dividable):
        #current dividend isn't dividable by divisor
        if(not isDividable(currentDividend,divisor)):
            #there isn't more numbers in restDividend to down
            if(len(restDividend)<=0):
                #not more dividables, end of divition
                dividable = False
            #there is more numbers in restDividend to down
            else:
                temp = restDividend.pop(0)
                currentDividend.append(temp)
                dividable = True
        else:
        #currentDividend is dividable by divisor
            currentDividend = xor(currentDividend,divisor,'left')
            dividable = True
    return currentDividend
            
    
def xor(dataA,dataB,sideOfXor):
    dataA = dataA.copy()
    dataB = dataB.copy()
    #left xor
    output = []
    if(sideOfXor == 'left'):
        #if dataB it's shorter add 0
        while(len(dataA)>len(dataB)):
            dataB.append(0)
        for x in range(len(dataA)):
            xorCalc = dataA[x]^dataB[x]
            output.append(xorCalc)
        #delete 0's in beginning
        for x in output.copy():
            if(x==0):
                output.remove(0)
            else:
                break
        return output
    if(sideOfXor == 'right'):
        output = dataA.copy()
        if(len(dataB)>0):
            dataATrim = output[-len(dataB):]
            for x in range(len(dataATrim)):
                output[-len(dataATrim)+x] = dataATrim[x]^dataB[x]
        return output
    #else
    return 0
        

    
def addCeros(inputList,cerosToAdd):
    while(cerosToAdd>0):
        inputList.append(0)
        cerosToAdd-=1
    

def isDividable(dividend,divisor):
    if(len(dividend)<len(divisor)):
        return False
    return True

def stringToList(string,direction):
    output = []
    #if direction = 1 string to list of ints
    if(not direction):
        for char in string:
            output.append(int(char))
    #if direction = 0 list of ints to string
    else:
            output = ''.join(str(e) for e in string) 
    return output
    


####################################################################
#testing

TESTING()

        
    
    
