# Name : Siarhei Hancharou
# Assignment #: 3
# Submission Date : 10/25/2020
#
# Description of program :
# You can set the diagonal length of the matrix yourself.
# If you choose the length of the matrix equal to 3, you play the classic
# game tik tak toe, with the option to choose the difficulty level 1 or 2.
# Level 1 - the computer randomly places 0.
# Level 2 - the program tries to win, at least make a draw.
# board - A two-dimensional list that is defined by the length of the diagonal.
# diagonal - The length of the diagonal, we set the value of the matrix
#   in which the player and the computer will play.Since the matrix is square,
#   the diagonal length is equal to the number of columns and rows.
# A Python tic-tac-toe game.

import random


# Brief introduction to the game. Print out once at the beginning to
# describe the game to the player.
def description():
    print('--------------------------------------')
    print('Description of the game to the player.')
    print('--------------------------------------')
    print('Set the length of the matrix diagonal.\n'
          'To select the classic game of TIC TAC TOE specify the length\n'
          'of the diagonal is equal = 3.\n'
          '   When choosing a classic game, you will be given the\n'
          'opportunity to choose the level of difficulty of the game.\n'
          'Level 1 the computer randomly puts 0\n'
          'level 2 the computer will try to win against you.\n')


# This function display the current Board to the player.
def print_board(board):
    # prints the current board
    for row in board:
        for col in row:
            print(col, end=' ')
        print()


# The function returns " 0 " or " x " if one of the rows has three
# 0 or x characters. So that I know exactly who won.
# If no one won returns False
def check_rows(board, diagonal):
    for row in range(len(board)):
        count_0 = 0
        count_x = 0
        for col in range(len(board[row])):
            if board[row][col] == '0':
                count_0 += 1
            if board[row][col] == 'x':
                count_x += 1
            if count_x == diagonal or count_0 == diagonal:
                won = board[row][col]
                return won
    else:
        return False


# The function returns " 0 " or " x " if one of the columns has three
# 0 or x characters. so that I know exactly who won.
# If no one won returns False
def check_cols(board, diagonal):
    for col in range(len(board[0])):
        count_0 = 0
        count_x = 0
        for row in range(len(board)):
            if board[row][col] == '0':
                count_0 += 1
            if board[row][col] == 'x':
                count_x += 1
            if count_x == diagonal or count_0 == diagonal:
                won = board[row][col]
                return won
    return False


# Boolean function to check diagonals 1 and 2 for a win.
# If True, the function returns '0' or 'x' so I know who won.
def check_diag_1_2(board, diagonal):
    for row in range(1):
        count_0 = 0
        count_x = 0
        # Checking the main diagonal.
        for col_1 in range(len(board)):
            if board[col_1][col_1] == '0':
                count_0 += 1
            if board[col_1][col_1] == 'x':
                count_x += 1
            if count_x == diagonal or count_0 == diagonal:
                won = board[col_1][col_1]
                return won

        count_0 = 0
        count_x = 0

        for col_2 in range(len(board)):
            if board[col_2][len(board) - col_2 - 1] == '0':
                count_0 += 1
            if board[col_2][len(board) - col_2 - 1] == 'x':
                count_x += 1
            if count_x == diagonal or count_0 == diagonal:
                won = board[col_2][len(board) - col_2 - 1]
                return won

    return False


# Void function to control the computer's moves uses randint for next move.
# The function has the board and level arguments.
# If the level is 1, then the computer uses random.randint for your next move.
# If level 2, then the computer uses random.randint, but in pre-winning
# situations I used hardcode, unfortunately I didn't come up with another
# way to automate this situation.
def comp_move(board, level, diagonal):
    # Computer moves first / last.

    # If Level = 1: x and y are selected randomly until a coordinate
    # not occupied by 0 or x is selected.
    if level == 1:
        comp_moves = True
        while comp_moves:
            x = random.randint(0, diagonal - 1)
            y = random.randint(0, diagonal - 1)
            if board[x][y] != 'x' and board[x][y] != '0':
                board[x][y] = '0'
                print()
                print('Computer move to ', '(', x, ',', y, ')', sep='')
                print_board(board)
                comp_moves = False
    # If the level is equal to 2, then the computer selects coordinates
    # randomly but up to a certain point, in pre-win situations,
    # I hardcode selected coordinates with priority for the computer.
    if level == 2:
        # We enter variables to make it easier to specify
        # coordinates in the future.
        one = 0, 0
        two = 0, 1
        three = 0, 2
        four = 1, 0
        five = 1, 1
        six = 1, 2
        seven = 2, 0
        eight = 2, 1
        nine = 2, 2

        ch_list = (one, two, three, four, five, six, seven, eight, nine)
        comp_moves_2 = True
        while comp_moves_2:
            # Output repeated lines of code to a separate function boar().
            def bord():
                board[x][y] = '0'
                print()
                # Displaying for the player how the computer moved.
                print('Computer move to ', '(', x, ',', y, ')', sep='')
                # Displaying for the player the current board.
                print_board(board)

            #  In pre-win situations when the computer or a player in the
            #  line is occupied by two fields, we hardcode specify which
            #  one to choose, if it is occupied randomly, any available
            #  cell is selected.
            #  We check all the  if  for the computer.
            if board[0][1] == board[0][2] == '0' and board[0][0] == '-' \
                    or board[1][0] == board[2][0] == '0' and board[0][0] == '-' \
                    or board[1][1] == board[2][2] == '0' and board[0][0] == '-':
                x, y = one
                bord()
                break

            if board[0][0] == board[0][2] == '0' and board[0][1] == '-' \
                    or board[1][1] == board[2][1] == '0' and board[0][1] == '-':
                x, y = two
                bord()
                break

            if board[0][0] == board[0][1] == '0' and board[0][2] == '-' \
                    or board[2][0] == board[1][1] == '0' and board[0][2] == '-' \
                    or board[1][2] == board[2][2] == '0' and board[0][2] == '-':
                x, y = three
                bord()
                break

            if board[0][0] == board[2][0] == '0' and board[1][0] == '-' \
                    or board[1][1] == board[1][2] == '0' and board[1][0] == '-':
                x, y = four
                bord()
                break

            if board[2][0] == board[0][2] == '0' and board[1][1] == '-' or \
                    board[0][1] == board[2][1] == '0' and board[1][1] == '-' or \
                    board[1][0] == board[1][2] == '0' and board[1][1] == '-' or \
                    board[0][0] == board[2][2] == '0' and board[1][1] == '-':
                x, y = five
                bord()
                break

            if board[1][0] == board[1][1] == '0' and board[1][2] == '-' or \
                    board[0][2] == board[2][2] == '0' and board[1][2] == '-':
                x, y = six
                bord()
                break

            if board[1][1] == board[0][2] == '0' and board[2][0] == '-' or \
                    board[2][1] == board[2][2] == '0' and board[2][0] == '-' or \
                    board[0][0] == board[1][0] == '0' and board[2][0] == '-':
                x, y = seven
                bord()
                break

            if board[0][1] == board[1][1] == '0' and board[2][1] == '-' or \
                    board[2][0] == board[2][2] == '0' and board[2][1] == '-':
                x, y = eight
                bord()
                break

            if board[2][0] == board[2][1] == '0' and board[2][2] == '-' or \
                    board[0][0] == board[1][1] == '0' and board[2][2] == '-' or \
                    board[0][2] == board[1][2] == '0' and board[2][2] == '-':
                x, y = nine
                bord()
                break
            #  We check all the if for the player.
            if board[1][1] == board[2][2] == 'x' and board[0][0] == '-' \
                    or board[1][0] == board[2][0] == 'x' and board[0][0] == '-' \
                    or board[0][1] == board[0][2] == 'x' and board[0][0] == '-':
                x, y = one
                bord()
                break

            if board[0][0] == board[0][2] == 'x' and board[0][1] == '-' \
                    or board[1][1] == board[2][1] == 'x' and board[0][1] == '-':
                x, y = two
                bord()
                break

            if board[2][0] == board[1][1] == 'x' and board[0][2] == '-' \
                    or board[0][0] == board[0][1] == 'x' and board[0][2] == '-' \
                    or board[1][2] == board[2][2] == 'x' and board[0][2] == '-':
                x, y = three
                bord()
                break

            if board[0][0] == board[2][0] == 'x' and board[1][0] == '-' \
                    or board[1][1] == board[1][2] == 'x' and board[1][0] == '-':
                x, y = four
                bord()
                break

            if board[2][0] == board[0][2] == 'x' and board[1][1] == '-' or \
                    board[0][1] == board[2][1] == 'x' and board[1][1] == '-' or \
                    board[0][0] == board[2][2] == 'x' and board[1][1] == '-' or \
                    board[1][0] == board[1][2] == 'x' and board[1][1] == '-':
                x, y = five
                bord()
                break

            if board[1][0] == board[1][1] == 'x' and board[1][2] == '-' or \
                    board[0][2] == board[2][2] == 'x' and board[1][2] == '-':
                x, y = six
                bord()
                break

            if board[0][0] == board[1][0] == 'x' and board[2][0] == '-' or \
                    board[1][1] == board[0][2] == 'x' and board[2][0] == '-' or \
                    board[2][1] == board[2][2] == 'x' and board[2][0] == '-':
                x, y = seven
                bord()
                break

            if board[2][0] == board[2][2] == 'x' and board[2][1] == '-' or \
                    board[0][1] == board[1][1] == 'x' and board[2][1] == '-':
                x, y = eight
                bord()
                break

            if board[2][0] == board[2][1] == 'x' and board[2][2] == '-' or \
                    board[0][0] == board[1][1] == 'x' and board[2][2] == '-' or \
                    board[0][2] == board[1][2] == 'x' and board[2][2] == '-':
                x, y = nine
                bord()
                break

            else:
                x, y = random.choice(ch_list)
                if board[x][y] != 'x' and board[x][y] != '0':
                    bord()
                    comp_moves_2 = False
    #  Returning the modified list
    return board

#  The function takes the coordinates of the pair from the player
#  and passes it to the list.
def my_turn_move(board, diagonal):
    # I don't know why I need to make 1 and 2 global,
    # but the IDE suggested it to me. I tried to figure it out.
    global x, y
    while True:
        #  We check that the numbers 0, 1 ,2 are entered.
        #  not other characters or other numbers.
        #  Only entering the correct numbers will break the cycle.
        try:
            if diagonal < 10:
                r = input("Enter in cell for your move as a coordinate pair\n"
                          "(e.g.00 ,10 etc ):\n")
                print(r)
                x = int(r[0])
                y = int(r[1])

            if 10 <= diagonal <= 100:
                r = input("Enter in cell for your move as a coordinate pair\n"
                          "(e.g.0000 ,0010  etc ):\n")
                x = int(r[:2])
                print(x)
                y = int(r[2:])
                print(y)

            if board[x][y] != 'x' and board[x][y] != '0':
                board[x][y] = 'x'

                print_board(board)
                break
            else:
                print('This cell is occupied select another one.')

        except ValueError or IndexError:
            print('Enter the numbers as directed!')

    return board


# Function to check if there is a winning state on the board.
def check_if_win(board, diagonal):
    #  Return '0' or 'x', depending on who won.
    if check_rows(board, diagonal):
        return check_rows(board, diagonal)

    if check_cols(board, diagonal):
        return check_cols(board, diagonal)

    if check_diag_1_2(board, diagonal):
        return check_diag_1_2(board, diagonal)


# The function calculates the maximum number of moves that a player
# can make in the matrix of a given long diagonal.
# We will need this to determine the draw in the game.
# Returns the maximum number of steps and this is assigned
# to the max_move variable.
def max_move_player(diagonal):
    max_move = 0
    incr = 2
    for i in range(2, diagonal + 1):
        if i == 2:
            max_move = 2
        if i > 2:
            max_move += incr
            if i % 2 != 0:
                incr += 2
    return max_move


# Game function of tic -tac -toe.
def tic_tac_toe():
    description()

    #  The loop can be interrupted by selecting repeat = n.
    while True:
        print('***********************')
        print('Welcome to Tic-Tac-Toe!')
        print('***********************')

        diagonal = int(input('How long is the diagonal of the matrix:\n'))
        cols = diagonal
        rows = cols
        #  Initializing the list where all the elements will be '-'
        board = [['-'] * cols for i in range(rows)]

        #  When choosing a classic TIC TAC TOE matrix, where the diagonal
        #  length is 3. We can choose two levels of difficulty.
        #  The level is passed to the comp_move(board, level, diagonal)
        #  function so that the computer can determine which
        #  strategy to choose.
        level = 1
        if diagonal == 3:
            level = int(input('Enter the level of difficulty 1 or 2:\n'))
            while level != 1 and level != 2:
                level = int(input('Enter the level of difficulty 1 or 2:\n'))

        #  The cycle can only be interrupted by a single win or a draw.
        #  Variable total_moves is for counting moves.
        total_moves = 0
        while True:

            if diagonal % 2 == 0:
                if total_moves == max_move_player(diagonal):
                    print("Almost, but this time it's a draw.")
                    break

            #  Computer move.
            comp_move(board, level, diagonal)

            #  If the check_if_win(board, diagonal) function returned
            #  the winner '0' then the computer won.
            if check_if_win(board, cols) == '0':
                print("Don't worry, you'll be lucky next time!")
                break

            #  If total_moves = 4, then the computer has made the
            #  last step and all cells are occupied. If the
            #  check_if_win(board) function did not return a win for
            #  one of the each it means a draw.

            if total_moves == max_move_player(diagonal):
                print("Almost, but this time it's a draw.")
                break

            #  Player move.
            my_turn_move(board, diagonal)
            total_moves += 1

            #  If the check_if_win(board, diagonal) function
            #  returned the winner 'x',then the player won.
            #  I did 'if' logically below so that after my turn
            #  the computer did not make a move
            if check_if_win(board, cols) == 'x':
                print("Congratulations! You've won!")
                break

        print()
        #  If you want to repeat the game, enter any character,
        #  if not, then 'n'
        repeat = input("Do you want to try again ? enter "
                       "'any' yes or 'n' no.\n")
        if repeat == "n":
            break


# # play the game
tic_tac_toe()
