import os.path
class Results:
    def __init__(self,ThisFilePath):
        f = open(os.path.join(ThisFilePath,"StructureProjection","Results.txt"),"r")
        Lines = f.readlines()
        self.Names = []
        self.NbOfROIs = int(Lines[0].split("\n")[0])
        self.NbOfContours = int(Lines[1].split("\n")[0])
        self.ROIsData = []
        for i in range(self.NbOfROIs):
            Data = []
            z = i*(self.NbOfContours+1)+2
            self.Names.append(Lines[z].split("\n")[0])
            for j in range(self.NbOfContours):
                l = Lines[z+1+j].split("\n")[0]
                l = l.split("\t")
                l.pop()
                Data.append(l)
                
            self.ROIsData.append(Data)
