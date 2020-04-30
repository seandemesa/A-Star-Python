import math
import random
import pygame
pygame.init()

class Spot():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.neighbors = []
        self.previous = None
        self.f = 0
        self.g = 0
        self.h = 0
        self.wall = False
        self.isUserCreatedWall = False
        self.randomNum = random.randint(0, 9)
        if self.randomNum <= 3:
            self.wall = True
    #neighbors = []



    def showSpot(self, color):
        if self.wall == True:
            color = (0, 0, 0)
        pygame.draw.rect(gameDisplay, color, [self.i * w, self.j * h,  w,  h])


    def addNeighbors(self, grid):
        self.i = i
        self.j = j
        if i < columns - 1:
            self.neighbors.append(grid[i + 1][j])
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if j < rows - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])
        if i > 0 and j > 0:
            self.neighbors.append(grid[i - 1][j - 1])
        if i < columns - 1 and j > 0:
            self.neighbors.append(grid[i + 1][j - 1])
        if i > 0 and j < rows - 1:
            self.neighbors.append(grid[i - 1][j + 1])
        if i < columns - 1 and j < rows - 1:
            self.neighbors.append(grid[i + 1][j + 1])



def heuristic(a, b):
    distance = math.sqrt((b.i - a.i)**2 + (b.j - a.j)**2)
    return distance


#pygame stuff
displayX = 1000
displayY = 1000
gameDisplay = pygame.display.set_mode((displayX, displayY))
gameDisplay.fill((255,255,255))
clock = pygame.time.Clock()
gameExit = False


userInputGridSize = int(input("Enter a scale (1, 2, 3, 4, or 5) for the grid/matrix \n(where 1 is the smallest scaling, and 5 is the largest)\n"))
toggleArrayScaleValue = userInputGridSize - 1
matrixSizesArray = [10, 20, 25, 50, 100]
rows = matrixSizesArray[toggleArrayScaleValue]
columns = matrixSizesArray[toggleArrayScaleValue]
path = []

white = (255, 255, 255)
black = (0, 0, 0)

w = int(displayX / columns)
h = int(displayY / rows)


grid = []
def createGrid(someGrid, col, row):
    for i in range(0, col):
        someGrid.append([])
        for j in range(0, row):
            newSpot = Spot(i, j)
            someGrid[i].append(newSpot)

createGrid(grid, columns, rows)

def deleteArrayContents(someArr):
    gridLength = len(someArr) - 1
    for i in range(0, gridLength):
        someArr.pop(0)


for i in range(0, columns):
    for j in range(0, rows):
        #addNeighbors(grid[i][j])
        grid[i][j].addNeighbors(grid)
        #print("the neighbors of node ", i, ", ", j, "are ")
        #if i <= 1:
            #for k in range(0, len(grid[i][j].neighbors)):
             #   print("the length of node ",i, ", ", j, " 's neighbors list is ", len(grid[i][j].neighbors))
             #print(grid[i][j].neighbors[k].i, " ", grid[i][j].neighbors[k].j)


openSet = []
closedSet = []

startNode = grid[0][0]
startNode.showSpot((255, 14, 93))
endNode = grid[columns - 1][rows - 1]
endNode.showSpot((0, 150, 200))
startNode.wall = False
endNode.wall = False
noSolution = False

openSet.append(startNode)

stopLooping = True
mouseIsClicked = False
OptimalPathFound = False
gridScaleWasAdjusted = False

stopText = False
font = pygame.font.SysFont(None, w + 5)
def text_to_screen(msg, locX, locY, width):
    screen_text = font.render(msg, True, (0, 0, 0))
    gameDisplay.blit(screen_text, [(locX * width) + int(width/4), locY * h])

BigFont = pygame.font.SysFont(None, int(displayX/20))
def text_to_screen_big(msg, locX, locY, color):
    screen_text = BigFont.render(msg, True, color)
    gameDisplay.blit(screen_text, [locX, locY])


#main game loop to draw grid
while not gameExit:

    pygame.draw.rect(gameDisplay, white, [displayX, displayY, 0, 0])

    startNode.wall = False
    endNode.wall = False

    mouseLocX = math.floor(pygame.mouse.get_pos()[0] / w)
    mouseLocY = math.floor(pygame.mouse.get_pos()[1] / h)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            gameExit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseIsClicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseIsClicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #option to start with random generated walls
                print("Starting A* search - option 1 pressed")
                stopLooping = False

            if event.key == pygame.K_2: #option to start with just user generated walls
                print("Starting A* search - option 2 pressed")
                stopLooping = False

                for i in range(0, columns):
                    for j in range(0, rows):
                        if not grid[i][j].isUserCreatedWall:
                            grid[i][j].wall = False

            # if event.key == pygame.K_o:
            #     if toggleArrayScaleValue != 0:
            #         deleteArrayContents(grid)
            #         pygame.draw.rect(gameDisplay, white, [endNode.i * w, endNode.j * h, w, h])
            #         toggleArrayScaleValue = toggleArrayScaleValue - 1
            #         rows = matrixSizesArray[toggleArrayScaleValue]
            #         columns = matrixSizesArray[toggleArrayScaleValue]
            #         w = int(displayX / columns)
            #         h = int(displayY / rows)
            #         createGrid(grid, rows, columns)
            #         endNode = grid[columns - 1][rows - 1]
            #         gridScaleWasAdjusted = True
            #
            # if event.key == pygame.K_p:
            #     if toggleArrayScaleValue < len(matrixSizesArray) - 1:
            #         deleteArrayContents(grid)
            #         pygame.draw.rect(gameDisplay, white, [endNode.i * w, endNode.j * h, w, h])
            #         toggleArrayScaleValue = toggleArrayScaleValue + 1
            #         rows = matrixSizesArray[toggleArrayScaleValue]
            #         columns = matrixSizesArray[toggleArrayScaleValue]
            #         w = int(displayX / columns)
            #         h = int(displayY / rows)
            #         createGrid(grid, rows, columns)
            #         endNode = grid[columns - 1][rows - 1]
            #         gridScaleWasAdjusted = True

            if event.key == pygame.K_s: #option to place starting node elsewhere from default (which is top left)
                startNode.showSpot((white))
                startNode = grid[mouseLocX][mouseLocY]
                openSet.pop()
                openSet.append(startNode)

            elif event.key == pygame.K_e: #option to place end node elsewhere from default (which is bottom right)
                endNode.showSpot((white))
                endNode = grid[mouseLocX][mouseLocY]

    if mouseIsClicked: #creating walls on mouse click + drag
        grid[mouseLocX][mouseLocY].wall = True
        grid[mouseLocX][mouseLocY].isUserCreatedWall = True
        pygame.draw.rect(gameDisplay, (0, 0, 0), [mouseLocX * w, mouseLocY * h,  w,  h])




    if len(openSet) > 0 and not stopLooping: #keep going - openSet still has nodes to visit
        lowestIndex = 0
        for i in range(0, len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]

        if current == endNode: #finished, now find the optimal path backwards
            stopLooping = True
            OptimalPathFound = True
            print("Open set is now empty; all paths checked. Optimal path is as follows.")



        openSet.remove(current)
        closedSet.append(current)


        newNeighbors = current.neighbors
        for i in range(0, len(newNeighbors)):
            #print("Length of neighbors is currently: ", len(newNeighbors))
            neighbor = newNeighbors[i]
            if closedSet.count(neighbor) == 0 and not neighbor.wall: #if the closed set does NOT include neighbor
                tempG = current.g + 1

                newPath = False
                if openSet.count(neighbor) >= 1:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        newPath = True
                else:
                    neighbor.g = tempG
                    newPath = True
                    openSet.append(neighbor)

                if newPath:
                    neighbor.h = heuristic(neighbor, endNode)   #euclidean distance or manhattan distance
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current
                #print("Just checked node ", neighbor.i, ", ", neighbor.j, "which has an f value of ", neighbor.f)

        for i in range(0, rows):#draw the white ("empty") spaces first
            for j in range(0, columns):
                grid[i][j].showSpot((white))

        path = []
        tempNode = current
        path.append(tempNode.previous)
        while tempNode.previous:
            path.append(tempNode.previous)
            tempNode = tempNode.previous


        for i in range(0, len(closedSet)):
            closedSet[i].showSpot((255, 99, 71))

        for i in range(0, len(openSet)):
            openSet[i].showSpot((79, 200, 120))

        for i in range(0, len(path)):
            if path[i] != None:
                path[i].showSpot((106, 90, 205))


    else:  #no solution
        if not noSolution and not OptimalPathFound and len(openSet) == 0:
            print("There is no route to the destination node")
            noSolution = True

    x = 0
    y = 0


    # if gridScaleWasAdjusted:
    #     pygame.draw.rect(gameDisplay, white, [endNode.i * w, endNode.j * h,  w,  h])
    #     startNode.showSpot((white))
    #     gridScaleWasAdjusted = False
    #     endNode = grid[columns - 1][rows - 1]
    #     #print("Start node is at ", startNode.i, " ",startNode.j, " and end node is at ", endNode.i, " ",endNode.j)

    endNode.showSpot((0, 150, 200))
    text_to_screen("e", endNode.i, endNode.j, w)
    startNode.showSpot((255, 140, 0))
    text_to_screen("s", startNode.i, startNode.j, w)

    z = 0
    for i in range(0, rows):
        #vertical lines
        pygame.draw.line(gameDisplay, black, [w + z, 0], [w + z, displayY], 1)
        #horizontal lines
        pygame.draw.line(gameDisplay, black, [0, h + z], [displayX, h + z], 1)
        z = z + w

    magenta = (255, 0, 255)
    if (stopLooping or noSolution or OptimalPathFound) and not stopText:
        text_to_screen_big("Visualization and User Interaction of A* Search", 100, 200, magenta)
        text_to_screen_big("-Created by Sean de Mesa-", 120, 250, magenta)
        text_to_screen_big("Click & hold mouse to create walls", 100, 500, magenta)
        text_to_screen_big("(S) + (hover mouse) to change starting node", 100, 600, magenta)
        text_to_screen_big("(top left is default)", 100, 650, (255, 140, 0))
        text_to_screen_big("(E) + (hover mouse) to change end node", 100, 700, magenta)
        text_to_screen_big("(bottom right is default)", 100, 750, (0, 150, 200))
        text_to_screen_big("Press 1 or 2 to start", 100, 800, magenta)
        text_to_screen_big("1 - Randomly generated walls + user-created walls", 100, 850, (125, 125, 60))
        text_to_screen_big("2 - Begin w/ user-created walls, if any", 100, 900, (125, 125, 60))
        stopText = True



    pygame.display.update()
    clock.tick(60)



print("end")
