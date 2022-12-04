#! python3
"""
Puzzle link: https://adventofcode.com/2022/day/2

"""

import os

from enum import Enum

class Hand(Enum):
    # values also double as the points awarded for using it in the game
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

def calculate_game_score(opponent: Hand, you: Hand):
    score: int = you.value

    if opponent == Hand.ROCK:
        if you == Hand.ROCK:
            # DRAW
            score += 3
        elif you == Hand.PAPER:
            # WIN
            score += 6
        else: # SCISSORS
            # LOSE
            pass
    elif opponent == Hand.PAPER:
        if you == Hand.ROCK:
            # LOSE
            pass
        elif you == Hand.PAPER:
            # DRAW
            score += 3
        else: # SCISSORS
            # WIN
            score += 6
    else: # SCISSORS
        if you == Hand.ROCK:
            # WIN
            score += 6
        elif you == Hand.PAPER:
            # LOSE
            pass
        else: # SCISSORS
            # DRAW
            score += 3
    return score

def get_hand(input: str):
    if input == "A" or input == "X":
        return Hand.ROCK
    elif input == "B" or input == "Y":
        return Hand.PAPER
    else:
        return Hand.SCISSORS

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    total_score = 0
    with open(file_path) as input_file:
        for round in input_file:
            opponent_char, you_char = round.split()
            opponent = get_hand(opponent_char)
            you = get_hand(you_char)
            total_score += calculate_game_score(opponent, you)
    print(total_score)



if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
