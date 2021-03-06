import math
class seamCarve:
    def __init__(self,columns,rows,vert,horiz,matrix):
        self.vert = vert
        self.horiz = horiz
        self.matrix = matrix
        self.columns = columns
        self.rows = rows
        #self.matrix = self.matrix.tolist()
        self.trackEnergy = []
#The
#first step is to traverse the image from the second row to the last row
#and compute the cumulative minimum energy M for all possible
#connected seams for each entry (i, dj):
#For the boundary cases, the difference = 0 if one of the pixel is outside of
#the given image.

    def cleanUp(self):
        self.matrix = [x for x in self.matrix if x!=[]]

    def returnEnergy(self,i,j):
        #test for bounds, if they go out of bounds
        #make difference 0
        if j+1 >= self.columns:
            d = 0
        else:
            d =abs(self.matrix[i][j]-self.matrix[i][j+1])
        if i+1 >= self.rows:
            b = 0
        else:
            b = abs(self.matrix[i][j]-self.matrix[i+1][j])
        if i-1 < 0:
            a = 0
        else:
            a = abs(self.matrix[i][j]-self.matrix[i-1][j])
        if j-1 < 0:
            c = 0
        else:
            c = abs(self.matrix[i][j]-self.matrix[i][j-1])
        return a+b+c+d

    def travel(self):
        #init empty 2d array, this will track the energy for each index
        #in picture
        trackEnergy = [[0 for x in range(self.columns)] \
         for x in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                trackEnergy[i][j] = self.returnEnergy(i,j)
        self.trackEnergy = trackEnergy

    def cumlativeCalcHorizontal(self):
            #for j in range(self.rows):
        #self.matrix = self.matrix.tolist()
        for j in range(self.columns):
            for i in range(self.rows):
                    if j == 0:
                        continue
                    else:
                        #check for negative rows:
                        if i-1 <0:
                            self.trackEnergy[i][j]+=min( self.trackEnergy[i][j-1]\
                            ,self.trackEnergy[i+1][j-1])
                        elif i+1 == self.rows:
                            self.trackEnergy[i][j]+=min( self.trackEnergy[i-1][j-1],\
                            self.trackEnergy[i][j-1]  )
                        else:
                            self.trackEnergy[i][j]+=min( self.trackEnergy[i-1][j-1],\
                            self.trackEnergy[i][j-1]  ,self.trackEnergy[i+1][j-1])
        #here we simply calculate the new matrix
    def cumlativeCalcVertical(self):
                for i in range(0,self.rows):
                    for j in range(0,self.columns):
                            if i == 0:
                                continue
                            else:
                                if  j-1 < 0:
                                    if i == self.rows-1:
                                        self.trackEnergy[i][j]+=min( self.trackEnergy[i-1][j+1]\
                                        ,self.trackEnergy[i-1][j])
                                    else:
                                        self.trackEnergy[i][j]+=min( self.trackEnergy[i-1][j+1]\
                                        ,self.trackEnergy[i-1][j])
                                elif j+1 == self.columns:
                                    self.trackEnergy[i][j]+=min( self.trackEnergy[i-1][j],\
                                    self.trackEnergy[i-1][j-1]  )
                                else:
                                    self.trackEnergy[i][j]+=min( self.trackEnergy[i-1][j-1],\
                                    self.trackEnergy[i-1][j+1]  ,self.trackEnergy[i-1][j])
#Hence, in the second step we backtrack from this minimum entry on
#M to find the path of the optimal seam
#note: vertical first, choose f(x) for this step
    def carveVertically(self):
        y = self.rows
        x = self.columns
        removeMe = []
        #step 1:
        #find min value in last column as starting point
        #find last column
        lastrow = y-1
        #find starting point:
        tempCol = []
        for i in range(x):
            tempCol.append(self.trackEnergy[lastrow][i])
        startPt = tempCol.index(min(tempCol))

        #startPt=1
        #step 2:
        # iterate through row, branch 3 and find min, store in removeMe
        # iterate till you hit the other side.
        # check for edge cases, you may have to branch twice
        #for i in range(self.columns):
            #for j in range(self.rows):
        i = self.rows-1
        #self.shiftLeft(i,)
        #startPt here is a column
        self.matrix[i][startPt]=-1
        self.shiftLeft(i,startPt)
    #    print "energy matrix: {}\n regular matrix: {}\n".format(self.trackEnergy,self.matrix)
        #for index errors
        error=0
        while i > 0:
                try:
                    restore = startPt
                    removeMe.append(
                        min( self.trackEnergy[i-1][startPt-1],\
                        self.trackEnergy[i-1][startPt]  ,self.trackEnergy[i-1][startPt+1])
                        )
                    lastEle = len(removeMe)
                    if removeMe[lastEle-1] == self.trackEnergy[i-1][startPt-1]:
                        if startPt-1 < 0:
                            error = len(self.matrix)+1
                            startPt = error
                        self.shiftLeft(i-1,startPt-1)
                        startPt = startPt-1
                    elif removeMe[lastEle-1]==self.trackEnergy[i-1][startPt]:
                        self.shiftLeft(i-1,startPt)
                    elif removeMe[lastEle-1]==self.trackEnergy[i-1][startPt+1]:
                        self.shiftLeft(i-1,startPt+1)
                        startPt = startPt+1
                except IndexError:
                    #restore startPt, if it went out of bounds
                    if startPt == error:
                        startPt = restore
                    #test for right or left branch error
                    #test for columns goiong out of bounds
                #    print "In error: checking bound of IndexError:{},{}".format(i,startPt)
                    if startPt-1 < 0:
                        removeMe.append(
                            min( self.trackEnergy[i-1][startPt]  ,self.trackEnergy[i-1][startPt+1]))
                        lastEle = len(removeMe)
                        if removeMe[lastEle-1]==self.trackEnergy[i-1][startPt]:
                                self.shiftLeft(i-1,startPt)
                        elif removeMe[lastEle-1]==self.trackEnergy[i-1][startPt+1]:
                                self.shiftLeft(i-1,startPt+1)
                                startPt = startPt+1
                    #now check bounds right
                    elif startPt+1 >= self.columns:
                    #    print "index out of bounds error: Right*************"
                        removeMe.append(
                            min( self.trackEnergy[i-1][startPt-1],
                            self.trackEnergy[i-1][startPt]  )
                            )
                        lastEle = len(removeMe)
                        if removeMe[lastEle-1] == self.trackEnergy[i-1][startPt-1]:
                            self.shiftLeft(i-1,startPt-1)
                            startPt = startPt-1
                        else:
                            removeMe[lastEle-1]==self.trackEnergy[i-1][startPt]
                            self.shiftLeft(i-1,startPt)
                finally:
                    i-=1

    def carveHorizontalyl(self):
        y = self.rows
        x = self.columns
        #self.matrix[y][x]
        #removeMe keeps track of each seam,
        #we will then iterate through the tuple removeMe
        #and remove each indice, and then shift
        removeMe = []
        #step 1:
        #find min value in last column as starting point
        #find last column
        lastcol = x-1
        #find starting point:
        tempCol = []
        for i in range(y):
            tempCol.append(self.trackEnergy[i][lastcol])
        startPt = tempCol.index(min(tempCol))
        #step 2:
        # iterate through row, branch 3 and find min, store in removeMe
        # iterate till you hit the other side.
        # check for edge cases, you may have to branch twice
        #for i in range(self.columns):
            #for j in range(self.rows):
        j = self.columns-1
        #self.matrix = self.matrix.tolist()
        self.shiftup(j,startPt)
        while j > 0:
            if startPt+1 == self.rows:
                removeMe.append(
                    min( self.trackEnergy[startPt-1][j-1],\
                    self.trackEnergy[startPt][j-1]  )
                    )
                lastEle = len(removeMe)
                if removeMe[lastEle-1] == self.trackEnergy[startPt-1][j-1]:
                    self.shiftup(j-1,startPt-1)
                elif removeMe[lastEle-1]==self.trackEnergy[startPt][j-1]:
                    self.shiftup(j-1,startPt)
            elif startPt-1 < 0:
                    removeMe.append(
                        min( self.trackEnergy[startPt][j-1]  ,self.trackEnergy[startPt+1][j-1])
                        )
                    lastEle = len(removeMe)
                    if removeMe[lastEle-1]==self.trackEnergy[startPt][j-1]:
                        self.shiftup(j-1,startPt)
                    elif removeMe[lastEle-1]==self.trackEnergy[startPt+1][j-1]:
                        self.shiftup(j-1,startPt+1)
            else:
                removeMe.append(
                    min( self.trackEnergy[startPt-1][j-1],\
                    self.trackEnergy[startPt][j-1]  ,self.trackEnergy[startPt+1][j-1])
                    )
                lastEle = len(removeMe)
                if removeMe[lastEle-1] == self.trackEnergy[startPt-1][j-1]:
                    self.shiftup(j-1,startPt-1)
                elif removeMe[lastEle-1]==self.trackEnergy[startPt][j-1]:
                    self.shiftup(j-1,startPt)
                elif removeMe[lastEle-1]==self.trackEnergy[startPt+1][j-1]:
                    self.shiftup(j-1,startPt+1)
            j-=1

    def shiftup(self,col,row):
        for i in range(row+1,self.rows):
            self.matrix[i-1][col] = self.matrix[i][col]
        del self.matrix[self.rows-1][col]

    def shiftLeft(self,col,row):
        del self.matrix[col][row]
