#! python3
"""
from: https://adventofcode.com/2021/day/4#part2

--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time
counting its arms, the safe thing to do is to figure out which board will win last and choose that
one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually
called and its middle column is completely marked. If you were to keep playing until this point,
the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 =
1924.

Figure out which board will win last. Once it wins, what would its final score be?

"""
import os

class BingoBoard(object):
    def __init__(self, raw_board):
        super().__init__()
        self.board = [
            raw_board[0:5],
            raw_board[5:10],
            raw_board[10:15],
            raw_board[15:20],
            raw_board[20:25]
        ]
        self.marked = [[False for x in range(5)] for x in range(5)]

    def mark_number(self, picked_num):
        """Mark the picked number on the board, if it contains it"""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == picked_num:
                    self.marked[row][col] = True
    
    def is_winner(self):
        """Check if this is a winning bingo board"""
        # check each row
        for row in self.marked:
            if row == [True for x in range(len(row))]:
                return True

        # check each column
        for col in range(len(self.marked[0])):
            extracted_col = list()
            for row in range(len(self.marked)):
                extracted_col.append(self.marked[row][col])
            if extracted_col == [True for x in range(len(self.marked[0]))]:
                return True

        return False

    def get_sum_unmarked(self):
        """Calculate the sum of all the unmarked numbers on the board"""
        sum = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if not self.marked[row][col]:
                    sum += self.board[row][col]
        return sum


def main(filename):
    """Solve the problem!"""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    picked_numbers = list()
    boards = list()
    BOARD_DIM = 5
    with open(file_path) as input_file:
        picked_numbers = list(map(int, input_file.readline().split(',')))
        temp_board = list()
        for line in input_file:
            if line.isspace():
                continue
            temp_board += list(map(int, line.strip().replace("  ", " ").split()))
            if len(temp_board) == BOARD_DIM * BOARD_DIM:
                initialized_board = BingoBoard(temp_board)
                boards.append(initialized_board)
                temp_board = list()
    boards_still_playing = boards
    for picked in picked_numbers:
        losers = list()
        for board in boards_still_playing:
            board.mark_number(picked)
            if board.is_winner():
                # calculate "score" from the last board to win
                if len(boards_still_playing) == 1:
                    print("FINAL WINNER!")
                    print(board.get_sum_unmarked() * picked)
            else:
                losers.append(board)
        boards_still_playing = losers


if __name__ == "__main__":
    main('example.txt')
    main('input.txt')
