import spacegrids as sg
import matplotlib
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import ogr
import numpy as np
from shapelyCheckWithin import *


def translateToNcIndex(inputPt):  #point as tuple (X,Y)
    
    Kx = -374495.83635354
    Ky = -616153.3341887
    #print pathToFC[-8:-4]
    #SHCID = int(pathToFC[-8:-4])

    def translateX(inputXcoord):
        Kx = -374495.83635354
        shiftX = inputXcoord - Kx
        coordX = int(math.floor(shiftX/270.0))
        return coordX

    def translateY(inputYcoord):
        Ky = -616153.3341887
        shiftY = inputYcoord - Ky
        coordY = int(math.floor(shiftY/270.0))
        return coordY
        
    cY = translateX(inputPt[0])
    cY = translateY(inputPt[1])
    return (cX, cY)



def showMeTime(inputTime):
    sg.contourf(sg.squeeze(F[scalar,int(inputTime)]))
    clb = plt.colorbar()
    clb.set_label(F.units)
    plt.show()

class ShapeContainer:
    def __init__(self, inputSHP):
        import fiona
        from shapely.geometry import shape, Point
        
        self.path = inputSHP
        self.c = fiona.open(inputSHP, 'r')
        self.f = self.c[0]
        self.geom = shape(self.f['geometry'])
    def checkPoint(self,inputPt):
        return self.geom.contains(inputPt)

inputSHP = r"J:\inputSHP_HUC10_Phase1\Albers_plyPhase1_HUC10s_SID1013.shp"   

D = sg.info(rootdir = r"X:\\_05_KlamClime\\05_Data_Spacegrids")   #D is Directory
P = sg.Project(D['shcid1013'])                                    #P is Project
dir(P)
print P.ls()
#[(a,type(P.__getattribute__(a))) for a in dir(P)]
P.load("CNRM_rcp85_Monthly_snw")
P.load('CNRM_rcp85_Monthly_tmx')
E = P['CNRM']
F = E['CNRM_rcp85_Monthly_tmx']

for c in E.axes:
  exec c.name + ' = c'


val = F[0,:,:].value

zeros = val*np.nan
zeros = zeros[0,:,:]

crdX = F.grid[2]
crdY = F.grid[1]
listCoords = []

crdsX = crdX.value
crdsY = crdY.value

thisShp = ShapeContainer(inputSHP)

#get dims
nRow = zeros.shape[0]
nCol = zeros.shape[1]

print "n rows = ", nRow
print "n cols = ", nCol

listRows = range(0,nRow)
listCols = range(0,nCol)

#for i in listRows:  # by Row, outer loop by Y 0 -> 107 -Fixed Y, 
#    for j in listCols:      # indx[0],coord[1],objPnt[2]

# i counts row (Y coord)
# j counts col (X coord)
j = 0
for i in listRows:         # 0->107
    for j in listCols:     # 0->83 
        Y = crdsY[i]
        X = crdsX[j]
        #print ( (i,j) ,(X,Y) )
        listCoords.append( ( (i,j) , (X,Y) , Point(X,Y) ) )

  
for items in listCoords:
    indx = items[0]
    i = indx[0]
    j = indx[1]
    test = thisShp.checkPoint(items[2])
    #print indx, items[1], test
    if( test ):
        indx = items[0]
        zeros[i,j] = 1.
        #STOP
    #print listCoords[0]

val0 = val[0,:,:]
masked = val0 * zeros
CS = plt.contourf(masked)
clb =plt.colorbar()
clb.set_label("max Temp deg C")
plt.show()

#showMeTime(1)
#showMeTime(2)

































