# start by creating board and end bounds

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != " ":
                return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    start_bounded = True
    end_bounded = True
    bounded = ""

    x_start = x_end - d_x * length
    y_start = y_end - d_y * length

    if 0 <= (x_end + d_x) < len(board):
        if 0 <= (y_end + d_y) < len(board):
            if board[y_end + d_y][x_end + d_x] == " ":
                end_bounded = False

    if 0 <= x_start < len(board):
        if 0 <= y_start < len(board):
            if board[y_start][x_start] == " ":

                start_bounded = False

    if start_bounded and end_bounded:
        bounded = "CLOSED"
    elif start_bounded and not end_bounded or not start_bounded and end_bounded:
        bounded = "SEMIOPEN"
    elif not start_bounded and not end_bounded:
        bounded = "OPEN"

    return bounded


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    y_cur = y_start
    x_cur = x_start

    start_count = False
    seq_len = 0

    #runs until the end of the board
    while 0 <= y_cur < len(board) and 0 <= x_cur < len(board):
        #start of the sequence
        if board[y_cur][x_cur] == col and start_count == False:
            start_count = True
            seq_len += 1

        #ongoing sequence
        elif board[y_cur][x_cur] == col and start_count == True:
            seq_len += 1

        #end of the sequence
        elif board[y_cur][x_cur] != col and start_count == True:
            start_count = False

            if seq_len == length:
                if is_bounded(board, (y_cur - d_y), (x_cur - d_x), length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, (y_cur - d_y), (x_cur - d_x), length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1

            seq_len = 0

        y_cur += d_y
        x_cur += d_x

    #end of the board, but sequence is still ongoing
    if start_count == True:
            if seq_len == length:
                if is_bounded(board, (y_cur - d_y), (x_cur - d_x), length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, (y_cur - d_y), (x_cur - d_x), length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1

    return(open_seq_count, semi_open_seq_count)


def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0

    #check all rows
    for y in range(len(board)):
        result = detect_row(board, col, y, 0, length, 0, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]
        # if result != (0, 0):
        #     print("Rows:", result, y)

    #check all columns
    for x in range(len(board)):
        result = detect_row(board, col, 0, x, length, 1, 0)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]
        # if result != (0, 0):
        #     print("Cols:", result, x)

    #check all diagonals
    #top half including centre diagonals
    for i in range(len(board) - 1):
        #top-left to bottom-right
        result = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]
        # if result != (0, 0):
        #     print("Diagonals, top half, top-bottom:", result, i)

        #bottom-left to top-right
        result = detect_row(board, col, (len(board) - 1 - i), 0, length, -1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]
        # if result != (0, 0):
        #     print("Diagonals, top half, bottom-top:", result, i)

    #bottom half not including centre diagonals
    for j in range(1, len(board) - 1):
        #top-left to bottom-right
        result = detect_row(board, col, j, 0, length, 1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]
        # if result != (0, 0):
        #     print("Diagonals, bottom half, top-bottom:", result, j)

        #bottom-left to top-right
        result = detect_row(board, col, len(board) - 1, j, length, -1, 1)
        open_seq_count += result[0]
        semi_open_seq_count += result[1]
        # if result != (0, 0):
        #     print("Diagonals, bottom half, bottom-top:", result, j)

    return open_seq_count, semi_open_seq_count


def search_max(board):

    max_score = -10000000
    move_y = 0
    move_x = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                board[i][j] = "b"
                if score(board) > max_score:
                    max_score = score(board)
                    move_y = i
                    move_x = j
                board[i][j] = " "

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    counter = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != " ":
                counter += 1

    if score(board) == 100000:
        return "Black won"
    elif score(board) == -100000:
        return "White won"
    elif counter == 0:
        return "Draw"
    else:
        return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))



def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res


        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


### TESTS

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


### WEIRD BOARDS
    # *0|1|2|3|4|5|6|7*
    # 0 | | | | | | | *
    # 1 | | | | | | | *
    # 2w| |w|w| | |w| *
    # 3 |b| |b|w|b| | *
    # 4 | |b|b|b|w| | *
    # 5 | | |b|w|b|b| *
    # 6 |w|b|b|b| |w| *
    # 7 |w|w|w| | | | *
    # *****************
    # Black stones
    # Open rows of length 2: 1
    # Semi-open rows of length 2: 2
    # Open rows of length 3: 0
    # Semi-open rows of length 3: 2
    # Open rows of length 4: 0
    # Semi-open rows of length 4: 1
    # Open rows of length 5: 0
    # Semi-open rows of length 5: 0
    # White stones
    # Open rows of length 2: 1
    # Semi-open rows of length 2: 3
    # Open rows of length 3: 1
    # Semi-open rows of length 3: 1
    # Open rows of length 4: 0
    # Semi-open rows of length 4: 0
    # Open rows of length 5: 0
    # Semi-open rows of length 5: 0

    # Computer move: (7, 4)
    # doesn't play winning move


# if __name__ == '__main__':
#     # play_gomoku(8)
#
#     board = []
#     for i in range(8):
#         board.append([" "]*8)
#     put_seq_on_board(board, 0, 0, 0, 1, 1, "b")
#     put_seq_on_board(board, 1, 1, 0, 1, 2, "b")
#     put_seq_on_board(board, 3, 6, 0, 1, 1, "b")
#     put_seq_on_board(board, 0, 3, 0, 1, 3, "b")
#     put_seq_on_board(board, 6, 6, 0, 1, 1, "b")
#     put_seq_on_board(board, 2, 3, 1, 1, 3, "b")
#     put_seq_on_board(board, 7, 4, 0, 1, 4, "b")
#     put_seq_on_board(board, 2, 5, 0, 1, 2, "b")
#     put_seq_on_board(board, 5, 2, 1, 1, 2, "b")
#
#     put_seq_on_board(board, 7, 0, 0, 1, 1, "w")
#     put_seq_on_board(board, 0, 6, 0, 1, 1, "w")
#     put_seq_on_board(board, 7, 2, 0, 1, 2, "w")
#     put_seq_on_board(board, 2, 2, 1, 1, 4, "w")
#     put_seq_on_board(board, 3, 2, 1, 1, 3, "w")
#     put_seq_on_board(board, 3, 1, 1, 1, 3, "w")
#     put_seq_on_board(board, 0, 7, 1, 0, 3, "w")
#     put_seq_on_board(board, 6, 0, 0, 1, 2, "w")
#     put_seq_on_board(board, 2, 0, 1, 0, 3, "w")
#     put_seq_on_board(board, 3, 5, 1, 1, 3, "w")
#     put_seq_on_board(board, 1, 4, 0, 1, 2, "w")
#     print_board(board)
#     analysis(board)