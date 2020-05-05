def checkStatus(board):
    num_x = 0
    for x in board:
        for i in x:
            if i == "X":
                num_x += 1
    num_o = 0
    for x in board:
        for i in x:
            if i == "O":
                num_o += 1
    results = [checkVertical(board)[0], checkHorizontal(board)[0], checkDiagonal1(board)[0], checkDiagonal2(board)[0]]
    num_of_true = 0
    for x in results:
        num_of_true += x
    # Determine response
    if abs(num_x - num_o) >= 2 or num_of_true > 1:
        if abs(num_x - num_o) >= 2:
            return "Impossible"
        else:
            if results[0] > 1 or results[1] > 0:
                return "Impossible"
            else:
                if results[2] == 1:
                    return checkDiagonal1(board)[1] + " wins"
                else:
                    return checkDiagonal2(board)[2] + " wins"
    elif checkVertical(board)[0]:
        return checkVertical(board)[1] + " wins"
    elif checkHorizontal(board)[0]:
        return checkHorizontal(board)[1] + " wins"
    elif checkDiagonal1(board)[0]:
        return checkDiagonal1(board)[1] + " wins"
    elif checkDiagonal2(board)[0]:
        return checkDiagonal2(board)[1] + " wins"
    else:
        blank_present = False
        for x in board:
            for i in x:
                if i == "_":
                    blank_present = True
        if blank_present:
            return "Game not finished"
        else:
            return "Draw"

def checkVertical(board):
    num_of_wins = 0
    winning_piece = "_"
    i = 0
    while i < 3:
        check_piece = board[0][i]
        if check_piece == "_":
            i += 1
            continue
        j = 0
        column_flag = True
        while j < 3 and column_flag == True:
            if board[j][i] != check_piece:
                column_flag = False
            j += 1
        if column_flag == True:
            num_of_wins += 1
            winning_piece = check_piece
        i += 1
    return [num_of_wins, winning_piece]
def checkHorizontal(board):
    num_of_wins = 0
    winning_piece = "_"
    i = 0
    while i < 3:
        check_piece = board[i][0]
        if check_piece == "_":
            i += 1
            continue
        j = 0
        column_flag = True
        while j < 3 and column_flag == True:
            if board[i][j] != check_piece:
                column_flag = False
            j += 1
        if column_flag == True:
            num_of_wins += 1
            winning_piece = check_piece
        i += 1
    return [num_of_wins, winning_piece]

def checkDiagonal1(board):
    check_piece = board[0][0]
    if check_piece == "_":
        return [0]
    else:    
        j = 0
        while j < 3:
            if check_piece != board[j][j]:
                return [0]
            j += 1
        return [1, check_piece]
def checkDiagonal2(board):
    i = 2
    j = 0
    check_piece = board[i][j]
    if check_piece == "_":
        return [0]
    else:    
        while j < 3:
            if board[i][j] != check_piece:
                return [0]
            i -= 1
            j += 1
        return [1, check_piece]
def coordinatesCheck(x_coord, y_coord, board):
    try:
        x_coord = int(x_coord)
        y_coord = int(y_coord)
    except ValueError:
        print("You should enter numbers!")
        return False
    if x_coord > 3 or y_coord > 3 or x_coord < 1 or y_coord < 1:
        print("Coordinates should be from 1 to 3!")
        return False
    if board[3-y_coord][x_coord-1] != "_":
        print("This cell is occupied! Choose another one!")
        return False
    return True
    
# Makes board
board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
print("---------")
print("| " + " ".join(board[0]) + " |")
print("| " + " ".join(board[1]) + " |")
print("| " + " ".join(board[2]) + " |")
print("---------")
count = 0
while True:
    player_piece = ""
    if count % 2 == 0:
        player_piece = "X"
    else:
        player_piece = "O"
    coordinates = input("Enter the coordinates: > ").split()
    x_coord = coordinates[0]
    y_coord = coordinates[1]
    valid_input = coordinatesCheck(x_coord, y_coord, board)
    while not valid_input:
        coordinates = input("Enter the coordinates: > ").split()
        x_coord = coordinates[0]
        y_coord = coordinates[1]
        valid_input = coordinatesCheck(x_coord, y_coord, board)
    x_coord = int(x_coord)
    y_coord = int(y_coord)
    board[3 - y_coord][x_coord - 1] = player_piece
    print("---------")
    print("| " + " ".join(board[0]) + " |")
    print("| " + " ".join(board[1]) + " |")
    print("| " + " ".join(board[2]) + " |")
    print("---------")
    count += 1
    if checkStatus(board) != "Game not finished":
        break
print(checkStatus(board))
