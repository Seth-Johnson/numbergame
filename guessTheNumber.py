#!/usr/bin/python3

# Simple guess the number game

import datetime
import time
import os
import random
import json


class game:
    maxGuesses = 0
    def __init__(self, difficulty):
        self.maxGuesses = difficulty[0][0]
        self.min = difficulty[0][1]
        self.max = difficulty[0][2]
        self.number = random.randint(self.min,self.max)
        self.guesses = 0
        self.date = None
        self.name = None
        if len(difficulty) > 1:
            self.level = int(difficulty[1])
        else:
            self.level = 0

def clearConsole():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass
    
def mainMenu():
    menuOptions = {"1": "Select a level", "2": "Custom game", "3": "Leaderboard", "E": "Exit"}
    print("GUESS THE NUMBER")
    for key, option in menuOptions.items():
        print("{}) {}".format(key, option))
    selection = input("Make selection: ")
    if selection.upper() == "E":
        exit()
    try:
        int(selection)
    except ValueError:
        clearConsole()
        print("Please choose either 1, 2 or 3.")
        time.sleep(3)
        return mainMenu()
    if int(selection) == 1:
        return levelSelect()
    elif int(selection) == 2:
        return customSelect()
    elif int(selection) == 3:
        clearConsole()
        printLeaderboard()
        return mainMenu()
    else:
        clearConsole()
        print("Please choose either 1, 2 or 3.")
        time.sleep(3)
        return mainMenu()

def customSelect():
    print("CUSTOM GAME SETUP")
    maxGuesses = input("Maximum number of allowed guesses (optional): ")
    try:
        if not maxGuesses:
            maxGuesses = 0
        else:
            int(maxGuesses)
    except ValueError:
        clearConsole()
        print("Max guesses must be a number.")
        time.sleep(3)
        return customSelect()
    min = input("Bottom range: ")
    try:
        int(min)
    except ValueError:
        clearConsole()
        print("Min range must be a number")
        time.sleep(3)
        return customSelect()
    max = input("Upper range: ")
    try:
        int(max)
    except ValueError:
        clearConsole()
        print("Max must be a number")
        time.sleep(3)
        return customSelect()
    return [[int(maxGuesses) if maxGuesses else maxGuesses,int(min),int(max)]]

        
def levelSelect():
    levels = [[0,1,10],[0,1,25],[0,1,100],[25,1,100],[10,1,100]]
    clearConsole()
    print("SELECT A LEVEL")
    for index, level in enumerate(levels):
        print("{}: A number between {} and {}. Guesses allowed: {}.".format((index+1),level[1],level[2],("Infinite" if not level[0] else level[0])))
    selection = input("Selection: ")
    try:
        int(selection)
    except ValueError:
        clearConsole()
        print("Selection must be a number.")
        time.sleep(3)
        return levelSelect()
    if int(selection) > len(levels) or int(selection) <= 0:
        clearConsole()
        print("Selection must be between 1 and {}".format(len(levels)))
        time.sleep(3)
        return levelSelect()
    return(levels[int(selection)-1],selection)

def guess(currentGame):
    currGuess = input("Guess: ")
    print(currGuess)
    try:
        int(currGuess)
    except ValueError:
        clearConsole()
        print("Guess must be a number.")
        time.sleep(3)
        return guess(currentGame)
    currentGame.guesses += 1
    currGuess = int(currGuess)
    if currGuess == currentGame.number:
        return True
    elif currGuess > currentGame.number:
        print("You're too high! ;)")
    else:
        print("You're too low.")
    if currentGame.maxGuesses:
        if currentGame.guesses == currentGame.maxGuesses:
            print("You're out of guesses, sorry!")
            return False
    return guess(currentGame)

def updateLeaderboard(currentGame):
    leaderboard = {'leaderboard': [] }
    if not os.path.exists('leaderboard.json'):
         with open('leaderboard.json', 'w') as leaderboardRaw:
             leaderboardRaw.write(json.dumps(leaderboard))
    with open('leaderboard.json','r') as leaderboardRaw:
        leaderboard  = json.load(leaderboardRaw)
        leaderboard['leaderboard'].append(currentGame.__dict__)
    with open('leaderboard.json','w') as leaderboardRaw:
        leaderboardRaw.write(json.dumps(leaderboard))


def printLeaderboard():
    try:
        file = open('leaderboard.json','r')
    except Exception:
        pass
    board = json.load(file)
    leaderboard = board['leaderboard']
    leaderboard.sort(key=lambda item: (-(item.get('level')), item.get("guesses")))
    print("LEADERBOARD (any key to exit)")
    print("Name\tLevel\tGuesses\tMax\tMin\tDate")
    for entry in leaderboard:
        #print(entry)
        print("{}\t{}\t{}\t{}\t{}\t{}".format(entry['name'],entry['level'],entry['guesses'],entry['max'],entry['min'],entry['date']))
    wait = input()
    clearConsole()
    return
def main():
    currGame = game(mainMenu())
    clearConsole()
    print("Guess a number between {} and {}".format(currGame.min,currGame.max))
    winCondition = guess(currGame)
    if winCondition:
        print("You win!")
        currGame.name = input("Leaderboard name: ")
        if currGame.name:
            currGame.date = datetime.datetime.now().strftime('%Y-%m-%d %X')
            updateLeaderboard(currGame)
    else:
        print("You lose :(")
    selection = input("Press 1 to play again, or any key to exit. ")
    try:
        int(selection)
    except ValueError:
        exit()
    if int(selection) == 1:
        clearConsole()
        return main()
    else:
        exit()

if __name__ == "__main__":
    main()
