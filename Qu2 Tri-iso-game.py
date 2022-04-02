import random   # Imports well.. random


# classes

class Player:

    def __init__(self, playerNumber, maxMoves, triangleRow, triangleColumn, side, score) -> None:
        self.playerNumber = playerNumber
        self.maxMoves = maxMoves
        self.triangleRow = triangleRow
        self.triangleColumn = triangleColumn
        self.side = side
        self.score = score

    def __str__(self) -> str:
        return f"Player {self.playerNumber} is at triangle [{self.triangleColumn}, {self.triangleRow}] on side {self.side} and can move a maximum amount of {self.maxMoves} time(s)."

class Triangle:

    def __init__(self, row, column, own) -> None:
        self.row = row
        self.column = column
        self.own = own

    def __str__(self, orient) -> str:
        return f"This triangle is at [{self.column}, {self.row}] is a {orient} like triangle and, is owned by {self.own}."

    def fillTriangle(self, playerNumber):
        self.own = playerNumber

class Pointy(Triangle):

    orient = 0

    def __str__(self, orient = 0) -> str:
        return super().__str__(orient)

class Flat(Triangle):

    orient = 1

    def __str__(self, orient = 1) -> str:
        return super().__str__(orient)


# global variables

rows = 16 # DO NOT MAKE THE GRID A RECTANGLE (unless its a pointy one)
columns = 16 # WE ALREADY TRIED (and failed)

nPlayers = 6    # (1 ≤ p ≤ 5)
moves = 3       # (1 ≤ m ≤ 5,000)

playersDict = {
}

trianglesArray = []


# functions

def createTriangles(rows, columns):
    for i in range(rows):
        trianglesArray.append([])
        for j in range(columns):
            if j % 2 == i % 2:
                trianglesArray[i].append(Pointy(i, j, -1))
            else:
                trianglesArray[i].append(Flat(i, j, -1))

    trianglesArray[rows//2+1][columns//2+1].fillTriangle(0)

def createPlayers(nPlayers):
    for i in range(1, nPlayers + 1):    # the central triangle is owned by 0 and therefore can't be a player
        playersDict.update({i: Player(i, random.randint(1,100), rows//2+1, columns//2+1, 0, 0)})

def printTriangles(rows, columns):
    for i in range(rows):
        for j in range(columns):
            print(trianglesArray[i][j])

def printPlayers():
    for i in playersDict:
        print(playersDict[i])

def detectTri(n):
    row = playersDict[n].triangleRow
    column = playersDict[n].triangleColumn
    side = playersDict[n].side
    orient = trianglesArray[row][column].orient
    moveSi = [1, 1, 0, 0, 2, 2]

    if  orient == 0:
        print("Triangle is pointy")
        if side == 0:
            print("Player on side 0")
            checkTri = [trianglesArray[row][column], trianglesArray[row][column+1], trianglesArray[row-1][column+1], trianglesArray[row-1][column], trianglesArray[row-1][column-1], trianglesArray[row][column-1]]
            # moveSi = [0, 1, 1, 0, 0, 2]
            startLoop = 0
            adjTri = checkTri[5]
        elif side == 1:
            print("Player on side 1")
            checkTri = [trianglesArray[row+1][column+1], trianglesArray[row+1][column+2], trianglesArray[row][column+2], trianglesArray[row][column+1], trianglesArray[row][column], trianglesArray[row+1][column]]
            # moveSi = [2, 1, 1, 1, 1, 2]
            startLoop = 4
            adjTri = checkTri[3]
        else:
            print("Player on side 2")
            checkTri = [trianglesArray[row+1][column-1], trianglesArray[row+1][column], trianglesArray[row][column], trianglesArray[row][column-1], trianglesArray[row][column-2], trianglesArray[row+1][column-2]]
            # moveSi = [2, 1, 2, 0, 0, 2]
            startLoop = 2
            adjTri = checkTri[1]
    else:
        print("Triangle is flat")
        if side == 0:
            print("Player on side 0")
            checkTri = [trianglesArray[row][column-1], trianglesArray[row][column], trianglesArray[row-1][column], trianglesArray[row-1][column-1], trianglesArray[row-1][column-2], trianglesArray[row][column-2]]
            # moveSi = [2, 0, 1, 0, 0, 2]
            startLoop = 1
            adjTri = checkTri[0]
        elif side == 1:
            print("Player on side 1")
            checkTri = [trianglesArray[row][column+1], trianglesArray[row][column+2], trianglesArray[row-1][column+2], trianglesArray[row-1][column+1], trianglesArray[row-1][column], trianglesArray[row][column]]
            # moveSi = [0, 1, 2, 1, 1, 0]
            startLoop = 5
            adjTri = checkTri[4]
        else:
            print("Player on side 2")
            checkTri = [trianglesArray[row+1][column], trianglesArray[row+1][column+1], trianglesArray[row][column+1], trianglesArray[row][column], trianglesArray[row][column-1], trianglesArray[row+1][column-1]]
            # moveSi = [2, 1, 1, 2, 0, 2]
            startLoop = 3
            adjTri = checkTri[2]

    return checkTri, moveSi, startLoop, adjTri

def traverse(n):
    checkTri, moveSi, startLoop, adjTri = detectTri(n)

    for i in range(startLoop, startLoop+6):
        if checkTri[(i+1)%6].own == -1:
            playersDict[n].triangleRow = checkTri[i%6].row
            playersDict[n].triangleColumn = checkTri[i%6].column
            playersDict[n].side = moveSi[i%6]
            print(f"Player {n} is moving to triangle [{playersDict[n].triangleColumn}, {playersDict[n].triangleRow}], side {playersDict[n].side}")
            return adjTri

def reposition(n):
    for b in trianglesArray:
        for c in b:
            if c.own != -1:
                playersDict[n].triangleRow = c.row
                playersDict[n].triangleColumn = c.column
                playersDict[n].side = 0
                print(f"Player {n} has been reposition to triangle [{c.column}, {c.row}]")
                return

def score(n, adjTri):
    if (trianglesArray[adjTri.row-1][adjTri.column-1].own == n and trianglesArray[adjTri.row-1][adjTri.column+1].own) or (trianglesArray[adjTri.row+1][adjTri.column-1].own == n and trianglesArray[adjTri.row+1][adjTri.column+1].own) == n:
        playersDict[n].score += 1
        print(f"Player {n} has scored a point! Their score is {playersDict[n].score}.")
    

def move(n):
    for a in range(playersDict[n].maxMoves):
        if a == 0:
            adjTri = traverse(n)
        else:
            traverse(n)
    adjTri.own = n
    print(f"Triangle [{adjTri.column}, {adjTri.row}] is now owned by {n}")
    score(n, adjTri)

    for a in range(1, len(playersDict)+1):
        checkTri, moveSi, startLoop, adjTri = detectTri(a)
        if adjTri.own != -1:
            reposition(a)




# main program

# setting up the game
createTriangles(rows, columns)
createPlayers(2)
playersDict[1].maxMoves = 16
playersDict[2].maxMoves = 2
# playersDict[1].triangleColumn = 5
# playersDict[1].triangleRow = 5
# playersDict[2].triangleRow = 5
# playersDict[2].triangleColumn = 5


#playing the game

move(1)
move(2)
move(1)
move(2)
move(1)
move(2)

printPlayers()


