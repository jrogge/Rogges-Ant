#!/usr/bin/python
from Tkinter import *
from math import *
from time import *
# dimensions of window (always a square)
windowDim = 800
# number of pixels in a gridpoint
tileSize = 10
buttonYOffset = 30

filename = "./antMaps/automap.txt"

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

def setup():
    ''' draw grid'''
    for i in xrange(windowDim/tileSize):
        # fill in grid
        canvas.create_line(0,tileSize * i, windowDim, tileSize * i)
        canvas.create_line(tileSize * i, 0, tileSize * i, windowDim)

def click(event):
    x = event.x
    y = event.y
    # int division gets rid of decimal
    squareX = x / tileSize
    squareY = y / tileSize
    gridArray[squareX][squareY] = 1

    gridX = squareX * tileSize
    gridY = squareY * tileSize
    canvas.create_rectangle(gridX, gridY, gridX + tileSize, gridY + tileSize,
            fill="blue")

def save():
    f = open(filename, 'w')
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
canvas.bind("<Button-1>", click)
#canvas.bind("<B1-Motion>", drag)
root.call('wm', 'attributes', '.', '-topmost', True)
root.mainloop()
