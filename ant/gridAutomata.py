#!/usr/bin/python
from Tkinter import *
from math import *
from time import *
# dimensions of window (always a square)
windowDim = 800
# number of pixels in a gridpoint
tileSize = 10
# starting coords of the ant
startX = windowDim / (tileSize * 2)
startY = windowDim / (tileSize * 2)
# array of gridpoints that stores direction for each tile
flowMap = []
# array of gridpoints that determines the color of arc to draw
# needed so tracing back over a corner is done in a different color
# color progresses in the rainbow, is done mod 5 so loops back on itself
colorMap = []
# maps colors from the colorMap to actual colors
colorDict = { 0:"red", 1:"orange", 2:"yellow", 3:"green", 4:"blue", 5:"purple",
        6:"black"}
# remove magic number from mod calculations in changing color (lines 149 - 170)
numColors = len(colorDict)

class Corner():
    def __init__(self):
        self.TOPRIGHT = 0
        self.BOTTOMRIGHT = 1
        self.BOTTOMLEFT = 2
        self.TOPLEFT = 3

corner = Corner()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

ant = Point(startX, startY)
previousTile = Point(startX, startY)

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

# Tkinter handling
root = Tk()
window = Frame(root, width=windowDim, height=windowDim)
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
x = (screenwidth - windowDim)/2
y = (screenheight - windowDim)/2
root.geometry('%dx%d+%d+%d' % (windowDim, windowDim, x, y))
window.pack()
canvas = Canvas(window, height=windowDim, width=windowDim)
canvas.pack()

def setup():
    ''' draw grid and populate the flow array '''
    for i in xrange(windowDim/tileSize):
        # fill in grid
        canvas.create_line(0,tileSize * i, windowDim, tileSize * i)
        canvas.create_line(tileSize * i, 0, tileSize * i, windowDim)

        # add a new row to the flowMap
        flowMap.append([])
        # add a new row to the colorMap
        colorMap.append([])
        for j in xrange(windowDim/tileSize):
            # populate the flowMap with FlowingTile instances
            flowMap[i].append(FlowingTile(i,j))
            # populate the colorMap (values represent corners clockwise from top right)
            colorMap[i].append([0, 0, 0, 0])

def flipTile(tile):
    tile.xFlow *= -1
    tile.yFlow *= -1

def drawDirectionMarkers():
    ''' Draw quarter circles pointing in flow direction '''
    for rowIndex in xrange(windowDim/tileSize):
        for columnIndex in xrange(windowDim/tileSize):
            # pointing in positive X (right)
            if flowMap[rowIndex][columnIndex].xFlow == 1:
                startAngle = -45

            #pointing in negative X (left)
            elif flowMap[rowIndex][columnIndex].xFlow == -1:
                startAngle = 135

            #pointing in positive Y (down)
            elif flowMap[rowIndex][columnIndex].yFlow == 1:
                startAngle = 225

            #pointing in negative Y (up)
            elif flowMap[rowIndex][columnIndex].yFlow == -1:
                startAngle = 45

            lowerX = rowIndex * tileSize
            upperX = lowerX + tileSize
            lowerY = columnIndex * tileSize
            upperY = lowerY + tileSize
            canvas.create_arc(lowerX, lowerY, upperX, upperY,
                    start = startAngle, extent=90, style="arc")

def drawArc(currentPos):
     # draw ant's path

    # center represents the center of rotation of the quarter circle the ant goes through
    centerX = (previousTile.x + ant.x + 1) / 2
    centerY = (previousTile.y + ant.y + 1) / 2
    center = Point(centerX, centerY)
    
    # bbox is the Tkinter way of saying the box enclosing the ellipse
    bboxTopLeft = Point(centerX * tileSize - tileSize / 2,
            centerY * tileSize - tileSize/2)
    bboxLowerRight = Point(centerX * tileSize + tileSize / 2,
            centerY * tileSize + tileSize/2)

    # the base position from which we get our path color
    colorTile = colorMap[currentPos.x][currentPos.y]
    
    if (center.x > currentPos.x):
        # top left
        if (center.y > currentPos.y):
            startAngle = 90
            arcColor = colorDict[colorTile[corner.TOPLEFT]]
            colorTile[corner.TOPLEFT] = (colorTile[corner.TOPLEFT] + 1) % numColors
        # bottom left
        else:
            startAngle = 180
            arcColor = colorDict[colorTile[corner.BOTTOMLEFT]]
            colorTile[corner.BOTTOMLEFT] = (colorTile[corner.BOTTOMLEFT] + 1) % numColors
    else:
        # top right
        if (center.y > currentPos.y):
            startAngle = 0
            arcColor = colorDict[colorTile[corner.TOPRIGHT]]
            colorTile[corner.TOPRIGHT] = (colorTile[corner.TOPRIGHT] + 1) % numColors
        # bottom right
        else:
            startAngle = 270
            arcColor = colorDict[colorTile[corner.BOTTOMRIGHT]]
            colorTile[corner.BOTTOMRIGHT] = (colorTile[corner.BOTTOMRIGHT] + 1) % numColors

    canvas.create_arc(bboxTopLeft.x, bboxTopLeft.y,
            bboxLowerRight.x, bboxLowerRight.y,
            start=startAngle, extent=90, style="arc", outline=arcColor)
   
                
def progressAnt():
    ''' move the ant forward and turn based on the flow of the current tile
        draw the path the ant takes '''
    currentTile = flowMap[ant.x][ant.y]
    currentPos = Point(ant.x, ant.y)
    # change x and y based on the flow of the current tile
    ant.x += currentTile.xFlow
    ant.y += currentTile.yFlow
    # reverse direction of tile after moving from it
    # this method works because currentTile is a reference, not a copy
    flipTile(currentTile)
    
    drawArc(currentPos)

    previousTile.x = currentPos.x
    previousTile.y = currentPos.y

def tamper():
    gridSize = windowDim / tileSize
    middle = gridSize / 2

    # parse map file
    # coords to be flipped are stored on individual rows
    # - x and y are space delimited
    #mapPath = "./antMaps/map1.txt"
    mapPath = "./antMaps/automapcopy.txt"
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
        currentTile = flowMap[flipCoords[i][0]][flipCoords[i][1]]
        flipTile(currentTile)

def run():
    numSteps = 50
    while(True):
        for i in xrange(numSteps):
            progressAnt()
        canvas.update()

def click(event):
    run()
    #progressAnt()
    #canvas.update()

setup()
tamper()
canvas.bind("<Button-1>", click)
drawDirectionMarkers()
root.call('wm', 'attributes', '.', '-topmost', True)
root.mainloop()
