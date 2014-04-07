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
def nextHit(hitData, gameGrid):
    # Variable to be returned with coord value
    hitThis = ""
    
# Function to return potential hit locations which haven't already been touched
def potentialHits(grid, shipHits, hitData):
    # Array to return later
    pHits = []
    
    # Array to hold all hit locations of ships alive
    allHits = []
    
    # Variables to hold number counts
    highNum = 0
    lowNum = 0
    startNum = 0
    
    # Variables to hold letter decimal values
    startLetter = 65
    endLetter = 74
    letter = 65
    
    # Populate array
    for item in hitData:
        if hitData[item] != [] and shipHits[item] != 0:
            allHits.extend(hitData[item])
    
    for boat in shipHits:
        # Make sure the ship is not sunk already and hasn't been hit
        if shipHits[boat] != 0 and shipHits[boat] != int(boat[-2]):
            hitsLeft = shipHits[boat]
            coordsHit = hitData[boat]
            coordsHit.sort()
            
            if direction(coordsHit) is 0:   # Horizontal
                # Get high and low numbers values
                highNum = int(coordsHit[len(coordsHit) - 1][1:])
                lowNum = int(coordsHit[0][1:])
                
                # Get potential hits
                for a in range(1, lowNum):
                    if lowNum - hitsLeft <= a < lowNum:
                        pHits.append(coordsHit[0][:1] + str(a))
                for b in range(lowNum, highNum + 1):
                    if lowNum < b < highNum:
                        pHits.append(coordsHit[0][:1] + str(b))
                for c in range(highNum, 11):
                    if highNum  < c <= highNum + hitsLeft:
                        pHits.append(coordsHit[0][:1] + str(c))
                
            elif direction(coordsHit) is 1:   # Vertical
                # Get Start and end letter values
                startLetter = ord(coordsHit[0][:1])
                endLetter = ord(coordsHit[len(coordsHit) - 1][:1])
                
                # Get potential hits
                for a in range(65, startLetter):
                    if startLetter - hitsLeft <= a < startLetter:
                        pHits.append(chr(a) + coordsHit[0][1:])
                for b in range(startLetter, endLetter + 1):
                    if startLetter < b < endLetter:
                        pHits.append(chr(b) + coordsHit[0][1:])
                for c in range(endLetter, 75):
                    if endLetter < c <= endLetter + hitsLeft:
                        pHits.append(chr(c) + coordsHit[0][1:])
            
            else:   # Case - Single hit coord
                startNum = int(coordsHit[0][1:])
                letter = ord(coordsHit[0][:1])
                
                # Left coords
                for a in range(1, startNum):
                    if startNum - hitsLeft <= a < startNum:
                        pHits.append(coordsHit[0][:1] + str(a))
                # Right coords    
                for b in range(startNum, 11):
                    if startNum < b <= startNum + hitsLeft:
                        pHits.append(coordsHit[0][:1] + str(b))
                # Coords above
                for c in range(65, letter):
                    if letter - hitsLeft <= c < letter:
                        pHits.append(chr(c) + coordsHit[0][1:])
                # Coords below
                for d in range(letter, 75):
                    if letter < d <= letter + hitsLeft:
                        pHits.append(chr(d) + coordsHit[0][1:])
    
    # Trim results in case there is a miss or sunken shit at location
    return potentialTrim(pHits, grid)

# Function to only return potential coords that haven't been touched
def potentialTrim(grid, potentials):
    for coord in potentials:
        if grid[ord(coord[:1]) % 65][int(coord[1:])] != 'O':
            potentials.remove(coord)
    return potentials

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

# Returns False if the coordinates aren't in use
def coordsTaken(arr):
    for item in arr:
        if item in allCoords:
            return True
        else:
            return False
            
# Need a function shipDown (same as in pyBattleship class)
def shipDown(shipHits, boat):
    """ Returns True if the boat's hit value is at zero, meaning it is sunk"""
    if shipHits[boat] is 0:
        return True
    else:
        return False

# Function to figure out direction based on array of hits
def direction(hits):
    if hits[0][:1] is hits[1][:1]:
        return 0    # Horizontal
    elif hits[0][1:] is hits [1][1:]:
        return 1    # Vertical
    else:
        return 2    # Case - single array