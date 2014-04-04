import random

# Array to hold all coordinates already used
allCoords = []

# Need function to create an array of ship locations
# Format:
# [acStart, acEnd, batStart, batEnd, subStart, subEnd, cruiseStart, cruiseEnd, patrolStart, patrolEnd]
def createShipArray():
    # Array to hold string coordinates of ships
    # Returned at the end
    shipArray = []
    
    # Array of integers holding the max length of the 5 different ships
    shipLengths = [5, 4, 3, 3, 2]
    
    # Variable to hold a tempCoordinate
    tempCoord = []
    
    for num in range(0, len(shipLengths)):
        # Determine which direction to place a piece - 
        # 0 = Horizontal, 1 = Vertical
        direction = random.randrange(0,2)
        
        tempCoord = directionCoords(direction, shipLengths[num])
        
        # If these coordinates are in use, try again
        while coordsTaken(getAllCoords(tempCoord[0], tempCoord[1])):
            tempCoord = directionCoords(direction, shipLengths[num])
        
        # Append to shipArray
        shipArray.append(tempCoord[0]) 
        shipArray.append(tempCoord[1])
        
        # Update the Coordinates in the main allCoords list
        updateCoords(tempCoord[0], tempCoord[1])
        
    # Now return the final array of 10 string values
    return shipArray

# Need function to decide on next hit location based on the last hit, 
# amount of hits, and boat hit
# Outputs a coordinate string
def nextHit(hitData, player):
    pass
    # If coord is at the edge of the grid
    # If there's a coord between two hits
    

# Function to get a start and end coord set based on direction and
# Length of the ship to be placed
def directionCoords(direc, length):
    # to be returned later
    startEnd = []
    
    # Holds the decimal value of a letter from 'A' to 'J'
    letterCode = 65
    
    #Maximum letter code for looping, chr(74) = 'J'
    # Set to 75 so I can use randrange(65, maxChar) and only get ints from 65-74
    maxChar = 75
    
    # Variables to hold the int for making coordinates
    numHold = 0
    
    # Holds array of letters already used
    horizontalLetters = []
    
    if direc is 0:    # Horizontal Placement
        # Pick random letter between 'A' and maxChar ('J')
        letterCode = random.randrange(65, maxChar)
        
        # Need a number starting position between 1 and (10 minus ship length)
        numHold = random.randrange(1, 10 - length)
        
        # Append coordinate value for start position
        startEnd.append(chr(letterCode) + str(numHold))
        
        # Now the end coord
        startEnd.append(chr(letterCode) + str(numHold + length - 1))
        
        return startEnd
    
    else:   # Vertical Placement
        # Random letter between A and J(74)-length
        letterCode = random.randrange(65, maxChar - length)
        
        # Pick a random number
        numHold = random.randrange(1, 10)
        
        # Append to return array
        startEnd.append(chr(letterCode) + str(numHold))
        startEnd.append(chr(letterCode + length - 1) + str(numHold))
        
        return startEnd
        

# Need a function to return a random hit location
def randCoord():
    # Random value between 65 and 74 (need to put 75)
    letterCode = random.randrange(65, 75)
    
    # Random number between 1 and 10
    num = random.randrange(1, 11)
    
    return chr(letterCode) + str(num)
    
# Function to get full coordinates based on start and end values, then store them in the 
# allCoords array
def updateCoords(start, end):
    positions = []
    chrStart = 0
    length = 0
    
    # Same row
    if start[:1] is end[:1]:
        length = int(end[1:]) - int(start[1:]) + 1
        for number in range(int(start[1:]), int(end[1:]) + 1):
            positions += [str(start[:1] + str(number))]
    
    # Same Column
    elif start[1:] is end[1:]:
        length = (ord(end[:1]) % 65) - (ord(start[:1]) % 65) + 1
        chrStart = ord(start[:1])
        for number in range(chrStart, chrStart + length):
            positions += [str(chr(number) + start[1:])]
    
    allCoords.append(positions)

# Function to return list coordinates between start and end values
def getAllCoords(start, end):
    positions = []
    chrStart = 0
    length = 0
    
    # Same row
    if start[:1] is end[:1]:
        length = int(end[1:]) - int(start[1:]) + 1
        for number in range(int(start[1:]), int(end[1:]) + 1):
            positions += [str(start[:1] + str(number))]
    
    # Same Column
    elif start[1:] is end[1:]:
        length = (ord(end[:1]) % 65) - (ord(start[:1]) % 65) + 1
        chrStart = ord(start[:1])
        for number in range(chrStart, chrStart + length):
            positions += [str(chr(number) + start[1:])]
    
    return positions

# Function to check coordinates are already in use
# Returns False if the coordinates aren't in use
def coordsTaken(arr):
    for item in arr:
        if item in allCoords:
            return True
        else:
            return False