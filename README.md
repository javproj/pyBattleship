pyBattleship
============

Python Battleship game

Need to Update the main file so that you can play the computer.

AI is all set (battleshipAI.py). Main functions for the AI are:

createShipArray() -> Creates a random array of coordinates for ship placement

potentialHits(params) -> Given a gameGrid, shipHits, and hitData: Returns a list of potential coords where a ship could be located. Initially it just returns all coordinates that are hitsLeft distance away from the current hit coordinates. Calls on potentialTrim to do a smart Trim of the potential coords.

potentialTrim(params) -> Given a gameGrid, potential coords, and hitsLeft: Trim down potential coords to exclude those who have been hit/missed already, and those that are blocked by a hit/miss.

Currently Working to use a basic GUI like Tkinter to play the game instead of through terminal. 
