

#create a board object to represent the minesweeper game
#this is so that we can just say "create a new board object", or
#"dig here", or "render this gmae for this object"
import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #create the board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        #initialize a set to keep track of which locations uncovered
        #(row,col) tuples saved into this set
        self.dug = set() #if we dig at 0,0 then self.dug = {(0,0)}
        for i in range(dim_size):
                print(self.board[i], ' ')

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self, row, col):
        #top left: (row - 1, col - 1)
        #top middle: (row - 1, col)
        #top right: (row - 1 , col + 1)
        #right: (row, col + 1)
        #bot right: (row + 1 , col  + 1)
        #bot middle: (row + 1, col)
        #bot left: (row + 1 , col - 1)
        #left: (row, col - 1)

        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1,row + 1) + 1):
            for c in range( max(0, col - 1), min(self.dim_size - 1,col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def make_new_board(self):
        #construct a new board based on the dim size and num bombs
        #we should construct the list of lists here( or whatever representation you prefer,
        #but since we have a 2-D board, list of lists is most natural)

        #generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        #plants the boms
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            location = random.randint(0, self.dim_size**2 - 1 )
            row = location // self.dim_size
            col = location % self.dim_size

            if board[row][col] == '*':
                #this means we've actually planted a bomb there already so keep going
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board

    def dig(self, row, col):

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        #scanning for adjacent if being able to hop
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self):
        #create new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        # now let's put this together in a string
        # string_rep = "\n".join(map(str, visible_board))
        # return string_rep
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '   ' + '-' * str_len + '\n' + string_rep + '   ' + '-' * str_len

        return string_rep


def play( dim_size = 10, num_bombs = 1):
    #Step 1: Create the board an plant the boms
    board = Board(dim_size, num_bombs)

    safe = True
    #Step 2: Show the user the board and ask for where they want to dig
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(r',(\w\s)*', input('Where would you like to dig, enter as rol,col: '))
        row,col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row > dim_size - 1 or col < 0 or col > dim_size - 1:
            continue
        # if it's valid, dig
        safe = board.dig(row,col)
        # Step 3a: if location is a bomb, show game over message
        if not safe:
            break

    if safe:
        print("CONGRAT! YOU WIN")
        print(board)
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

    else:
        print("SORRY GAME OVER!")
        #reavel the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

    #Step 3b: If location is not a bomb, dig recursively until each square is at least
    #       next to a bomb
    #Step 4: Repeat step 2 and 3a/b until there are no more places to dig -> VICTORY

if __name__ == '__main__':
    play()