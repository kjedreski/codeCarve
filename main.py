import sys
from sys import argv
from cmdLineParse import cmdLineParse
from seamCarve import *

#Todo: fixed parse first 4 function!!!\
#!!!!!!!!! first 4 arent properly being parsed, fix this -- later...

parsed = cmdLineParse(sys.argv)
#print "filename:{}\n vertical seam:{}\n horizontal seam: {}\n matrix \n{}"\
#.format(parsed.filename,parsed.vert,parsed.hor,parsed.matrix)
#unpack split()
columns, rows = parsed.findColumnsRows()

picture = seamCarve(columns, rows,parsed.vert,parsed.hor, parsed.matrix)
picture.travel()
#print "energy matrix: {}\n".format(picture.trackEnergy)
#picture.carveVertically()

#print "loop:"
#Signing off on horizontal slicing,
#todo:: fix iterative vertical slicing

#travel calc's energy matrix
#cunlative calc's cumlative energy matrix
#carve

#signing off on vertical carving,
#what i'm noticing now is, energy grid isn't resetting
for i in range(int(parsed.vert)):
    picture.travel()
    picture.cumlativeCalcVertical()
    picture.carveVertically()
    picture.columns-=1
for i in range(int(parsed.hor)):
    picture.travel()
    picture.cumlativeCalcHorizontal()
    picture.carveHorizontalyl()
    picture.rows-=1
    #print "after carving: {}".format(i)
#deletes empty subarrays
picture.cleanUp()
#for i in picture.matrix:
    #print i
#print "new file stage --------------"
parsed.processNewFile(picture.matrix,picture.columns,picture.rows)
#now process new file
