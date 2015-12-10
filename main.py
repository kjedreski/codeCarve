#Program: Seam Carving
#Developer: Kevin Jedreski
#Purpose: run seam carve on pgm images and then create new pgm images
#how: to run: >> python main.py imagename verticalseams horizontalseams



import sys
from sys import argv
from cmdLineParse import cmdLineParse
from seamCarve import *
#bring it command line arguments
parsed = cmdLineParse(sys.argv)
#get rows and columns
columns, rows = parsed.findColumnsRows()
#generate seamcarve  object
picture = seamCarve(columns, rows,parsed.vert,parsed.hor, parsed.matrix)
#init matrix and find energy matrix
picture.travel()

for i in range(int(parsed.vert)):
    picture.travel()
    #find cumlative energy matrix
    picture.cumlativeCalcVertical()
    #carve
    picture.carveVertically()
    #reduce columns by 1
    picture.columns-=1
for i in range(int(parsed.hor)):
    picture.travel()
    #carve
    picture.cumlativeCalcHorizontal()
    picture.carveHorizontalyl()
    #reduce rows by 1
    picture.rows-=1
#deletes empty subarrays
picture.cleanUp()
#now process new file
parsed.processNewFile(picture.matrix,picture.columns,picture.rows)
