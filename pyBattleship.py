"""
    Author: Jesse Vazquez, Jesse.Vazquez@trincoll.edu
    Last Modified: 04/14/2014
    
    This is a recreation of the Battleship board game where players place
    ships on a 10x10 grid, then proceed to try and sink the enemie's 5 ships
    
    battleshipAI.py will contain functions for the computer populating a grid 
    with pieces and determining which location to try and hit.
"""

import sys
import random  
import battleshipAI
from collections import OrderedDict

### Player Class ###
class Player():
    """ 
    This class will contain the player and game grids used to play the game.
    Contains functions used to create, modify, update, and print the grids during play.
    """
    
    def __init__(self, pieceLocations):
        """ 
        Takes the piece locations array as a parameter. Initializes the player instance by: creating locations and shipLocations dictionary, init's player piece grid and game grid, and updates dictionary with locations of each ship.
        """
        self.locations = pieceLocations
        # Need to keep track of ships and their locations
        self.shipLocations = OrderedDict([
            ("Aircraft Carrier (5)", []),
            ("Battleship (4)", []),
            ("Submarine (3)", []),
            ("Cruiser (3)", []),
            ("Patrol Boat (2)", [])
        ])
        
        # Need variable to keep track of how many times a player is hit
        self.hits = 0
        
        # Need variable to keep track of hit data for the last hit
        # Format: [boatName, ([hitLocations])]
        # e.g.: ["Aircraft Carrier (5)", (["E2", "E3"])]
        self.hitData = OrderedDict([
            ("Aircraft Carrier (5)", []),
            ("Battleship (4)", []),
            ("Submarine (3)", []),
            ("Cruiser (3)", []),
            ("Patrol Boat (2)", [])
        ])
        
        # Variable to hold string of last player's ship that was hit
        self.lastShipHit = ""
        
        # Need variable to keep track of how many hits a boat has
        self.shipHits = OrderedDict([
            ("Aircraft Carrier (5)", 5),
            ("Battleship (4)", 4),
            ("Submarine (3)", 3),
            ("Cruiser (3)", 3),
            ("Patrol Boat (2)", 2)
        ])
        
        # Initialize Player grid and game grid to all zeros
        self.myGrid = [ ["O" for i in range(10)] for j in range(10)]
        self.gameGrid =  [ ["O" for i in range(10)] for j in range(10)]
        
        # Initialize shipLocations
        self.setShipLocations(self.locations)
        
        # Now set up the grid with the gridSet method
        for num in range(0, len(self.locations), 2):
            self.gridSet(self.locations[num], self.locations[num + 1], self.myGrid)
    
    # Sets up initial grid with piece locations    
    def gridSet(self, start, end, grid):
        """ gridSet function takes the start, end coordinates, and the grid. It determines if the piece is to be placed horizontally or vertically, then updates the player grid"""
        # Horizontal piece layout
        if start[:1] is end[:1]:
            for num in range(int(start[1:]) - 1, int(end[1:])):
                grid[ord(start[:1]) % 65][num] = "S"
        
        # Vertical piece layout
        elif start[1:] is end[1:]:
            for num in range(ord(start[:1]) % 65, ord(end[:1]) % 65 + 1):
                grid[num][int(start[1:]) - 1] = "S"
        
        else:
            print "Looks like you have invalid coordinates, unable to set the grid"
        
    # Update player's game grid with Hit (H) or Miss (M)
    def gameGridUpdate(self, loc, hitMiss):
        """ gameGridUpdate function takes a coordinate value, and a string (hitMiss), then updates the gameGrid appropriately to be displayed by the player"""
        self.gameGrid[ord(loc[:1]) % 65][int(loc[1:]) - 1] = hitMiss
    
    # Player tries a location (e.g. "F5") on the grid of another player
    def move(self, opponent, loc):
        
        # If other player's grid @ location is occupied
        if opponent.myGrid[ord(loc[:1]) % 65][int(loc[1:]) - 1] is "S":
            print "HIT - %s - %s!!!!" % (loc, opponent.getShipName(loc))
            self.gameGridUpdate(loc, "H")
            self.lastShipHit = opponent.getShipName(loc)
            opponent.hits += 1
            
        # If other player's grid @ location is NOT occupied
        elif opponent.myGrid[ord(loc[:1]) % 65][int(loc[1:]) - 1] is "O":
            print "MISS on %s!!!!" % (loc)
            self.gameGridUpdate(loc, "M")
    
    # Update the shipLocations dictionary to store the grid locations of the ship
    def setShipLocations(self, coordinates):
        """ setShipLocations function takes in an array of start and end piece coordinates, creates an array of all coordinates of each ship, then assigns those coordinates to the shipLocations dictionary. This assumes that the param coordinates are in the format: 
        [acStart, acEnd, batStart, batEnd, subStart, subEnd, cruiseStart, cruiseEnd, patrolStart, patrolEnd]
        """
        start = ""
        end = ""
        # Hold keys for dictionary to use for assignment later, count variable will assist
        keys = self.shipLocations.keys()
        count = 0
        
        for num in range(0, len(coordinates), 2):
            start = coordinates[num]
            end = coordinates[num + 1]
            length = 0
            chrStart = 0
            positions = []
            
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
            
            # Assign positions to shipPositions array
            self.shipLocations[keys[count]] = positions
            count += 1
    
    # Get ship name from the shipLocations dictionary 
    def getShipName(self, loc):
        """ Returns the name of the ship that was hit"""
        for boat in self.shipLocations:
            if loc in self.shipLocations[boat]:
                # Subtract 1 hit from the boat
                self.shipHits[boat] -= 1
                
                # If the boat is down, return the boat name and that it's down
                # Otherwise return the boat value
                if self.shipDown(boat) is True:
                    #Change game grid to reflect sunken ship
                    self.sunkenShipUpdate(boat)
                    
                    return "%s is down!" % (boat)
                else:
                    return boat
    
    def shipDown(self, boat):
        """ Returns True if the boat's hit value is at zero, meaning it is sunk"""
        if self.shipHits[boat] is 0:
            return True
        else:
            return False
        
    # Need function to return True if the player has a boat which was hit on the board
    def hasHits(self):
        """ Returns True if player has a ship on the board which has been hit and is not sunk."""
        count = 0
        for item in self.hitData:
            if len(self.hitData[item]) != 0 and len(self.hitData[item]) != int(self.hitData[item][-2]):
                count += 1
        
        if count != 0:
            return True
        else:
            return False
    
    # Prints the Player grid with ships placed
    def printPlayerGrid(self):
        """ Prints the player grid with appropriate labels"""
        chrStart = 65
        labelNums = "    1    2    3    4    5    6    7    8    9   10 "
        print labelNums
        for line in self.myGrid:
            print chr(chrStart), line
            chrStart += 1
    
    # Prints Player's game grid with Hits and Misses
    def printGameGrid(self):
        """ Prints the player's game grid with appropriate labels"""
        chrStart = 65
        labelNums = "    1    2    3    4    5    6    7    8    9   10 "
        print labelNums
        for line in self.gameGrid:
            print chr(chrStart), line
            chrStart += 1
    
    # Updates the game grid to relfect a sunken ship with 'X'
    def sunkenShipUpdate(self, boat):
        coords = self.hitData[boat]
        for coord in coords:
            self.gameGrid[ord(coord[:1]) % 65][int(coord[1:])] = 'X'
    
    def printShipHits(self):
        """ Print the shipHits dictionary, used for testing"""
        return self.shipHits
    
    def printShipLocations(self):
        """ Print the shipLocations dictionary, used for testing"""
        return self.shipLocations

# Piece locations
# An array storing the string locations of all pieces
# [acStart, acEnd, batStart, batEnd, subStart, subEnd, cruiseStart, cruiseEnd, patrolStart, patrolEnd]
p1Pieces = battleshipAI.createShipArray()
p2Pieces = battleshipAI.createShipArray()

## Game State ##
# Create player instances
p1 = Player(p1Pieces)
p2 = Player(p2Pieces)

# Variables to hold the last hit location
# [boatName, hitLocation, timesHit]
p1LastHit = []
p2LastHit = []

# Arrays to hold all coordinates that a player has tried
p1allTries = []
p2allTries = []

# Variable to determine who's turn it is
p1turn = True

while p1.hits < 18 and p2.hits < 18:
    print p1.hits, p2.hits
    # If Player 1 has max hits, player 2 wins
    if p1.hits is 17:
        print "Player 2 Wins!!"
        break
    
    # If Player 2 has max hits, player 1 wins
    elif p2.hits is 17:
        print "Player 1 Wins!!"
        break
    
    # Continue playing the game
    else:
        if p1turn:  # If it's player 1's turn
            p1.printGameGrid()
            
            hitLoc = raw_input("Player 1 - Enter hit location: ")
            
            while hitLoc in p1allTries:
                print "Already tried that coord, choose another"
                hitLoc = raw_input("Player 1 - Enter hit location: ")
            
            p1allTries.append(hitLoc)   # Add to tries array
            
            p1.move(p2, hitLoc)
            p1turn = False
        else:       # Player 2 turn (comp)
            print "Computer's Turn"
            
            if p1.hits < 1 and p1.hasHits() == False:   # Need a random coord
                hitLoc = battleshipAI.randCoord()
                
                while hitLoc in p1allTries: # No duplicates
                    hitLoc = battleshipAI.randCoord()
                
                p2allTries.append(hitLoc) #Add to p2 Tries array
            else:
                potentials = battleshipAI.potentialHits(p1.gameGrid, p1.shipHits, p1.hitData)
                hitLoc = potentials[random.randrange(0, len(potentials))]
                p2allTries.append(hitLoc)
                
            print "Computer tries %s" % (hitLoc)
            p2.move(p1, hitLoc)
            p1turn = True
