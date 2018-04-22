#!/usr/bin/python
from Tkinter import *
from math import *
from time import *
from sys import *
# dimensions of window (always a square)
windowDim = 800
# number of pixels in a gridpoint
tileSize = 10
buttonYOffset = 30

# array of gridpoints that stores direction for each tile
flowMap = []

filename = argv[1]
#filename = "./antMaps/automapcopy.txt"

# make and populate map basis
gridArray = []
for i in xrange(windowDim / tileSize):
    gridArray.append([])
    for j in xrange(windowDim / tileSize):
        gridArray[i].append(0)

# Tkinter handling
root = Tk()
#window = Frame(root, width=windowDim, height=windowDim)
window = Frame(root)
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
x = (screenwidth - windowDim)/2
y = (screenheight - windowDim - buttonYOffset)/2
root.geometry('%dx%d+%d+%d' % (windowDim, windowDim + buttonYOffset, x, y))
window.pack()
canvas = Canvas(window, height=windowDim, width=windowDim)
canvas.pack()

class FlowingTile:
    def __init__(self, x, y):
        self.xFlow = 0
        self.yFlow = 0
        # determine direction of flow for this tile
        if(x % 2 == 0):
            if( y % 2 == 0):
                self.xFlow = 1
            else:
                self.yFlow = 1
        else:
            if(y % 2 == 0):
                self.yFlow = -1
            else:
                self.xFlow = -1
    def flip(self):
        self.xFlow *= -1;
        self.yFlow *= -1;

def drawDirectionMarker(rowIndex, columnIndex, arrowColor):
    ''' Draw quarter circles pointing in flow direction '''
    lowerX = rowIndex * tileSize
    upperX = lowerX + tileSize
    lowerY = columnIndex * tileSize
    upperY = lowerY + tileSize
    centerX = (lowerX + upperX) / 2
    centerY = (lowerY + upperY) / 2
    endX = centerX
    endY = centerY
    # pointing in positive X (right)
    if flowMap[rowIndex][columnIndex].xFlow == 1:
        startAngle = -45
        endX = upperX

    #pointing in negative X (left)
    elif flowMap[rowIndex][columnIndex].xFlow == -1:
        startAngle = 135
        endX = lowerX

    #pointing in positive Y (down)
    elif flowMap[rowIndex][columnIndex].yFlow == 1:
        startAngle = 225
        endY = upperY

    #pointing in negative Y (up)
    elif flowMap[rowIndex][columnIndex].yFlow == -1:
        startAngle = 45
        endY = lowerY

    canvas.create_arc(lowerX, lowerY, upperX, upperY,
        start = startAngle, extent=90, style="arc", outline=arrowColor)
    canvas.create_line(centerX, centerY, endX, endY, fill=arrowColor)


def setup():
    ''' draw grid & populate flow array'''
    middle = windowDim / 2
    canvas.create_rectangle(middle, middle, middle + tileSize, middle + tileSize, fill="red")
    for i in xrange(windowDim/tileSize):
        # fill in grid
        canvas.create_line(0,tileSize * i, windowDim, tileSize * i)
        canvas.create_line(tileSize * i, 0, tileSize * i, windowDim)

        # add a new row to the flowMap
        flowMap.append([])
        # add a new row to the colorMap
        for j in xrange(windowDim/tileSize):
            # populate the flowMap with FlowingTile instances
            flowMap[i].append(FlowingTile(i,j))
            # populate the colorMap (values represent corners clockwise from top right)
            drawDirectionMarker(i, j, "black")

def click(event):
    x = event.x
    y = event.y
    # int division gets rid of decimal
    squareX = x / tileSize
    squareY = y / tileSize
    middle = windowDim / tileSize / 2
    flowMap[squareX][squareY].flip()
    if (gridArray[squareX][squareY]):
        gridArray[squareX][squareY] = 0
        fillColor = "white"
        arrowColor = "black"
    else:
        gridArray[squareX][squareY] = 1
        fillColor = "blue"
        arrowColor = "white"

    gridX = squareX * tileSize
    gridY = squareY * tileSize
    canvas.create_rectangle(gridX, gridY, gridX + tileSize, gridY + tileSize,
        fill=fillColor)
    #print "Coords: (", x, ",", y, ")"
    #print "Rows:", len(flowMap), "Columns:", len(flowMap[0])
    drawDirectionMarker(squareX, squareY, arrowColor)


def load():
    gridSize = windowDim / tileSize
    middle = gridSize / 2

    # parse map file
    # coords to be flipped are stored on individual rows
    # - x and y are space delimited
    #mapPath = "./antMaps/map1.txt"
    mapPath = filename
    mapFile = open(mapPath, 'r')
    flipCoords = []
    for line in mapFile:
        # last index will be length of list before anything gets appended
        lastIndex = len(flipCoords)
        # separate coords into x and y
        flipCoords.append(line.split(' '))
        # turn the interpreted strings into ints
        x = middle + int(flipCoords[lastIndex][0])
        y = middle + int(flipCoords[lastIndex][1])
        flipCoords[lastIndex][0] = x
        flipCoords[lastIndex][1] = y
        screenX = tileSize * x
        screenY = tileSize * y
        canvas.create_rectangle(screenX, screenY, screenX + tileSize, screenY + tileSize, fill="blue")
    #flipCoords = [[middle, middle], [middle + 1, middle],
    #        [middle, middle + 1], [middle + 1, middle + 1],
    #        [middle - 1, middle], [middle, middle - 1],
    #        [middle - 1, middle - 1], [middle + 1, middle - 1],
    #        [middle - 1, middle + 1]]
    for i in xrange(len(flipCoords)):
        x = flipCoords[i][0]
        y = flipCoords[i][1]
        currentTile = flowMap[x][y]
        gridArray[x][y] = 1
        currentTile.flip()
        drawDirectionMarker(x, y, "white")

def save():
    f = open(filename, 'w')
    # delete the current contents of the file and replace them with new ones
    f.seek(0)
    f.truncate()
    size = windowDim / tileSize
    middle = size / 2
    for x in xrange(size):
        for y in xrange(size):
            if gridArray[x][y]:
                relativeX = x - middle
                relativeY = y - middle
                f.write("%d %d\n" % (relativeX, relativeY))

    f.close()


setup()
b = Button(root, text="save", command=save)
b.pack(side=BOTTOM)
canvas.focus_set()
canvas.bind("<Button-1>", click)
load()
#canvas.bind("<Key>", redrawDirectionMarker)
#canvas.bind("<B1-Motion>", drag)
root.call('wm', 'attributes', '.', '-topmost', True)
root.mainloop()
