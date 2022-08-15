def hashShifts(length):
    # Create shifts
    modZero = [1, 3, 5, 7, 8, 9, 2, 4, 6]
    modOne = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    modTwo = [2, 4, 6, 8, 1, 3, 5, 7, 9]
    modThree = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    modFour = [4, 8, 3, 7, 2, 6, 1, 5, 9]
    modFive = [5, 9, 4, 8, 3, 7, 2, 6, 1]
    modSix = [6, 2, 8, 4, 1, 7, 5, 9, 3]
    modSeven = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    modEight = [1, 3, 5, 9, 8, 6, 4, 2, 7]
    modNine = [9, 8, 7, 6, 5, 4, 3, 2, 1]

    if length % 10 == 0:
        return modZero
    elif length % 10 == 1:
        return modOne
    elif length % 10 == 2:
        return modTwo
    elif length % 10 == 3:
        return modThree
    elif length % 10 == 4:
        return modFour
    elif length % 10 == 5:
        return modFive
    elif length % 10 == 6:
        return modSix
    elif length % 10 == 7:
        return modSeven
    elif length % 10 == 8:
        return modEight
    elif length % 10 == 9:
        return modNine


def hashGenerator(key, rank):
    # Goal, create controlled randomness

    # Declaration
    hashNum = 0
    keyLength = len(key)

    # Choosing today's shifter. Will use these to scramble values
    modShift = hashShifts(len(key) + rank)
	
	#Scramble modshift
    for i in range(len(modShift)):
        modShift[i] = modShift[i] * len(key) + (modShift[0] * (-1**i))

    # ASCII Addition
    for i in range(len(key)):
        # Multiplies ASCII values by a number at modulated index of ASCII value
        hashNum += ord(key[i]) * modShift[(i % 9)]

    # Multiply and add by key length
    hashNum = hashNum * keyLength + ((ord(key[0]) + 1) * 2) + rank

    return hashNum


def hashOutput(numKey, hashlen):
    modShift = hashShifts(numKey)

    characters = ""
    newHex = "00"
    tickDown = numKey

    #Key Generation
    while len(characters) < hashlen:

        #Number countdown
        while tickDown > 254:
            tempTick = tickDown
            tempTick //= modShift[tickDown % 8 + 1]
            if tempTick == tickDown:  # Logic tree to prevent eternal loop
                tempTick -= 1  # Allows for new ModShift
                tickDown = tempTick
            else:
                tickDown = tempTick
            #print(tickDown, end=", ")

        if newHex == hex(tickDown)[2:]:
            newHex = hex(tickDown - (len(characters) % 15))[2:]
            tickDown -= (len(characters) % 15)
        else:
            newHex = hex(tickDown)[2:]
        characters += newHex  # Add new hexadecimal
        charLength = len(characters)
        tickDown = (tickDown**(charLength % 4)) * tickDown  # Raise variable for another round

    return characters

def cycleHashFunction(ph, rank, length):
	number = abs(hashGenerator(ph, rank))
	hexa = hashOutput(number, length)
	return hexa

def HashFunction(ph):
	rank = 0
	number = abs(hashGenerator(ph, rank))
	length = 64
	hexa = hashOutput(number, length)
	
	print ("\nHash Output:", hexa)

def singleRun():
    phrase = input("Please enter any phrase as your key: ")
    print ("Key:", phrase)
    HashFunction(phrase)

#Uncomment the line below to run file as a python program
#singleRun()                             
