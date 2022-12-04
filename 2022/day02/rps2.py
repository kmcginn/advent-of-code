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

class Outcome(Enum):
    # values also double as the points awarded for the outcome
    LOSE = 0
    DRAW = 3
    WIN = 6

def calculate_game_score(opponent: Hand, you: Outcome):
    score: int = you.value

    if opponent == Hand.ROCK:
        if you == Outcome.DRAW:
            # DRAW - ROCK
            score += Hand.ROCK.value
        elif you == Outcome.WIN:
            # WIN - PAPER
            score += Hand.PAPER.value
        else: # SCISSORS
            # LOSE - SCISSORS
            score += Hand.SCISSORS.value
    elif opponent == Hand.PAPER:
        if you == Outcome.LOSE:
            # LOSE - ROCK
            score += Hand.ROCK.value
        elif you == Outcome.DRAW:
            # DRAW - PAPER
            score += Hand.PAPER.value
        else: # SCISSORS
            # WIN - SCISSORS
            score += Hand.SCISSORS.value
    else: # SCISSORS
        if you == Outcome.WIN:
            # WIN - ROCK
            score += Hand.ROCK.value
        elif you == Outcome.LOSE:
            # LOSE - PAPER
            score += Hand.PAPER.value
        else: # SCISSORS
            # DRAW - SCISSORS
            score += Hand.SCISSORS.value
    return score

def get_hand(input: str):
    if input == "A":
        return Hand.ROCK
    elif input == "B":
        return Hand.PAPER
    else:
        return Hand.SCISSORS

def get_outcome(input: str):
    if input == "X":
        return Outcome.LOSE
    elif input == "Y":
        return Outcome.DRAW
    else: # Z
        return Outcome.WIN

def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    total_score = 0
    with open(file_path) as input_file:
        for round in input_file:
            opponent_char, you_char = round.split()
            opponent = get_hand(opponent_char)
            you = get_outcome(you_char)
            total_score += calculate_game_score(opponent, you)
    print(total_score)



if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
