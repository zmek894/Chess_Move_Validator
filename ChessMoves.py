import re

def main():
    #Get and validate board state
    regex = "^[KQRBNP][a-h][1-8]$"
    print("Enter pieces in as 'Rf1, Kg1, Pf2'.")
    print("WHITE:", end = " ")
    whitePieces = str(input()).split(", ")
    
    if not validateInput(whitePieces, regex):
        print("Error: Invalid input")
        return

    print("BLACK:", end = " ")
    blackPieces = str(input()).split(", ")

    if not validateInput(blackPieces, regex):
        print("Error: Invalid input")
        return
    
    #Get and validate piece to move
    print("PIECE TO MOVE:", end = " ")
    movePiece = str(input())
    if not re.search(regex, movePiece):
        print("Error: Invalid input")
        return

    #Lowercase white pieces
    for i in range(len(whitePieces)):
        whitePieces[i] = whitePieces[i][:1].lower() + whitePieces[i][1:]

    #Create piece master list where piece is [type, column, row]
    listPieces = [[]]*(len(whitePieces) + len(blackPieces))
    for i in range(len(whitePieces)):
        p = whitePieces[i]
        listPieces[i] = [p[:1], ord(p[1:2])-96, int(p[2:])]
    for i in range(len(whitePieces), len(whitePieces) + len(blackPieces)):
        p = blackPieces[i-len(whitePieces)]
        listPieces[i] = [p[:1], ord(p[1:2])-96, int(p[2:])]

    #Create board
    board = [[" " for i in range(8)] for j in range(8)]
    for i in range(len(listPieces)):
        p = listPieces[i]
        if board[p[2]-1][p[1]-1] != " ":
            print("Error: More than one piece on a single space")
            return
        board[p[2]-1][p[1]-1] = p[0]
    print("\n" + boardToStr(board))

    #Reformat piece to move
    pMove = [movePiece[:1], ord(movePiece[1:2])-96, int(movePiece[2:])]
    if board[pMove[2]-1][pMove[1]-1] == pMove[0].lower():
        pMove[0] = pMove[0].lower() #is a white  piece
    if board[pMove[2]-1][pMove[1]-1] != pMove[0]:
        print("Error: Piece to move does not match board")
        return

    #Evaluate possible moves
    if re.search("^[Kk]$", pMove[0]):
        board = cardinalMove(pMove, board, True)
        board = diagonalMove(pMove, board, True)
    elif re.search("^[Qq]$", pMove[0]):
        board = cardinalMove(pMove, board, False)
        board = diagonalMove(pMove, board, False)
    elif re.search("^[Rr]$", pMove[0]):
        board = cardinalMove(pMove, board, False)
    elif re.search("^[Bb]$", pMove[0]):
        board = diagonalMove(pMove, board, False)
    elif re.search("^[Nn]$", pMove[0]):
        board = knightMove(pMove, board)
    elif pMove[0] == "p":
        board = pawnMove(pMove, board, True)
    elif pMove[0] == "P":
        board = pawnMove(pMove, board, False)

    print("\n" + boardToStr(board))

    #Generate list of possible moves
    posMoves = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == "*":
                posMoves.append(chr(col+97)+str(row+1))
    print("Possible moves for "+movePiece+": "+listToStr(posMoves))
    
def listToStr(moveList):
    output = ""
    for i in range(0,len(moveList)):
        output += ", " + moveList[i]
    return output[2:]

def pawnMove(piece, board, whitePiece):
    if whitePiece:
        pawnForward = lambda row, spaces : row + spaces
        regex = "^[KQRBNP]$"
        initialRow = 2
    else:
        pawnForward = lambda row, spaces : row - spaces
        regex = "^[kqrbnp]$"
        initialRow = 7

    space = [piece[2]-1, piece[1]-1] #[row, column]
    
    fRow = pawnForward(space[0],1)
    f2Row = pawnForward(space[0],2)
    rCol = space[1] + 1
    lCol = space[1] - 1

    if fRow < 8 and fRow >= 0:
        #Check space in front
        if board[fRow][space[1]] == " ":
            board[pawnForward(space[0],1)][space[1]] = "*"
         
        #Check capture spaces
        if re.search(regex, board[fRow][rCol]) and rCol < 8 and rCol >= 0:
            board[fRow][rCol] = "*"
        if re.search(regex, board[fRow][lCol]) and lCol < 8 and lCol >= 0:
            board[fRow][lCol] = "*"

        #Check if initial row
        if space[0]+1 == initialRow:
            if board[fRow][space[1]] == "*" and board[f2Row][space[1]] == " ":
                board[f2Row][space[1]] = "*"

    return board

def knightMove(piece, board):
    #space = [row, column]
    #2 Up,1 Right
    incrementer = lambda space : [space[0]+2,space[1]+1]
    boundTest = lambda space : (space[0] < 8) and (space[1] < 8)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Up, 1 Left
    incrementer = lambda space : [space[0]+2,space[1]-1]
    boundTest = lambda space : (space[0] < 8) and (space[1] >= 0)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Down, 1 Right
    incrementer = lambda space : [space[0]-2,space[1]+1]
    boundTest = lambda space : (space[0] >= 0) and (space[1] < 8)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Down, 1 Left
    incrementer = lambda space : [space[0]-2,space[1]-1]
    boundTest = lambda space : (space[0] >= 0) and (space[1] >= 0)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Right, 1 Up
    incrementer = lambda space : [space[0]+1,space[1]+2]
    boundTest = lambda space : (space[0] < 8) and (space[1] < 8)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Right, 1 Down
    incrementer = lambda space : [space[0]-1,space[1]+2]
    boundTest = lambda space : (space[0] >= 0) and (space[1] < 8)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Left, 1 Up
    incrementer = lambda space : [space[0]+1,space[1]-2]
    boundTest = lambda space : (space[0] < 8) and (space[1] >= 0)
    board = standardMove(board, piece, True, incrementer, boundTest)

    #2 Left, 1 Down
    incrementer = lambda space : [space[0]-1,space[1]-2]
    boundTest = lambda space : (space[0] >= 0) and (space[1] >= 0)
    board = standardMove(board, piece, True, incrementer, boundTest)

    return board

def cardinalMove(piece, board, isKing):
    #Up
    incrementer = lambda space : [space[0]+1,space[1]]
    boundTest = lambda space : space[0] < 8
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    #Down
    incrementer = lambda space : [space[0]-1,space[1]]
    boundTest = lambda space : space[0] >= 0
    board = standardMove(board, piece, isKing, incrementer, boundTest)  

    #Left
    incrementer = lambda space : [space[0],space[1]-1]
    boundTest = lambda space : space[1] >= 0
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    #Right
    incrementer = lambda space : [space[0],space[1]+1]
    boundTest = lambda space : space[1] < 8
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    return board

def diagonalMove(piece, board, isKing):
    #Up-Right
    incrementer = lambda space : [space[0]+1,space[1]+1]
    boundTest = lambda space : space[0] < 8 and space[1] < 8
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    #Down-Right
    incrementer = lambda space : [space[0]-1,space[1]+1]
    boundTest = lambda space : space[0] >= 0 and space[1] < 8
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    #Up-Left
    incrementer = lambda space : [space[0]+1,space[1]-1]
    boundTest = lambda space : space[0] < 8 and space[1] >= 0
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    #Down-Left
    incrementer = lambda space : [space[0]-1,space[1]-1]
    boundTest = lambda space : space[0] >= 0 and space[1] >= 0
    board = standardMove(board, piece, isKing, incrementer, boundTest)

    return board

def standardMove(board, piece, moveOnce, incrementer, boundTest):
    collision = False
    space = [piece[2]-1, piece[1]-1] #[row, column]
    space = incrementer(space)
    inBounds = boundTest(space)
    while (not collision) and inBounds:
        if board[space[0]][space[1]] == " ":
            board[space[0]][space[1]] = "*"
            space = incrementer(space)
            inBounds = boundTest(space)
        else:
            collision = True
            if takePiece(board[space[0]][space[1]], piece[0]):
                board[space[0]][space[1]] = "*"
        if moveOnce:
            break #king and knight only moves "1" space
    return board

def takePiece(pTypeBoard, pTypeMove):
    if re.search(pTypeMove, "^[K|Q|R|B|N|P]$"): #is a black peice
        return bool(re.search(pTypeBoard, "^[k|q|r|b|n|p]$")) #return true if white piece
    else: #vice versa
        return bool(re.search(pTypeBoard, "^[K|Q|R|B|N|P]$"))

def validateInput(pieces, regex):
    valid = True
    for piece in pieces:
        if valid:
            valid = bool(re.search(regex, piece))
    return valid

def boardToStr(board):
    strBoard = "Lowercase = white, Uppercase = black\n"
    for i in range(7,-1,-1):
        strBoard += " +---+---+---+---+---+---+---+---+\n" + str(i+1)
        for j in range(8):
            strBoard += "| " + board[i][j] + " "
        strBoard +="|\n"
    strBoard += " +---+---+---+---+---+---+---+---+\n"
    strBoard += "   a   b   c   d   e   f   g   h\n"
    return strBoard
        

if __name__ == '__main__' :
    main()  