import numpy as np
from StringIO import StringIO

class cmdLineParse:
    def __init__(self,args):
        self.filename, self.vert, self.hor = self.parseCmd(args)
        self.firstFour = self.findFour()
        self.matrix = self.findMatrix()

    def parseCmd(self,args):
        return args[1], args[2], args[3]

    def findColumnsRows(self):
        #goes by columns,rows in this ex: 3 8\n
        #this will ONLY work if comment is not IN firstFour,
        for element in self.firstFour:
            if len(element.split()) == 2:
                return int(element.split()[0]), int(element.split()[1])

    def findMatrix(self):
        columns,rows = self.findColumnsRows()
        array = [ [500 for i in range(columns)] for i in range(rows) ]
        with open("matrixFile.txt","r") as outFile:
        #data = np.loadtxt("matrixFile.txt")
            iterator=0
            data = outFile.read().split()
            for i in range(rows):
                for j in range(columns):
                    array[i][j] = int(data[iterator])
                    iterator+=1
        #print array
        return array


        #pad with 500
        #array = np.reshape(rows,columns)
        #return array.astype(int)


    def findFour(self):
        currRow = 0
        row4 = 3
        array = []
        with open("matrixFile.txt","w") as mFile:
            with open(self.filename) as textFile:
                    for line in textFile:
                            if line[0] == '#':
                                print line[0]
                                continue
                            if currRow >= row4:
                                mFile.write(line)
                            else:
                                array.append(line)
                                currRow+=1
        return array

    def processNewFile(self,matrix,columns,rows):
        count=0
        with open(self.filename+"_processed.pgm","w") as newFile:
                newFile.write(self.firstFour[0])
                newFile.write(str(columns)+" "+str(rows)+"\n")
                newFile.write(self.firstFour[2])
                for i in range(rows):
                    for j in range(columns):
                        newFile.write(str(matrix[i][j])+" ")
                        if j==columns-1:
                            newFile.write("\n")


        #create new file concatending _processed.pgm at the end
