import spacegrids as sg
import matplotlib
import datetime
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

class SpaceGridsProj:
    def __init__(self, rootdir = r"X:\\_05_KlamClime\\05_Data_Spacegrids", verbose = True):
        self.verbose = verbose
        self.D = sg.info(rootdir)                                              #D is Directory
        #dir(P)
        #print P.ls()
        #[(a,type(P.__getattribute__(a))) for a in dir(P)]
        self.activeF = {'snw' : "", # april 1 snowpack
                        'ppt' : "", # precip
                        'tmx' : "", # t max
                        'run' : "", # runoff
                        'aet' : "", # actual et
                        'pet' : "", # potential et
                        'cwd' : "", # climatic water deficit
                        'pck' : "", # 
                        'rcg' : ""} # GW recharge

    def loadProject(self, proj = 'shcid1013'):
        self.P = sg.Project(self.D[proj])                                    #P is Project


    def loadDataSet(self, dS = ('CNRM_rcp85_Monthly_tmx') ):
        #self.P.load("CNRM_rcp85_Monthly_snw")
        self.P.load(dS)
        self.file = dS+".nc"
        splitie = dS.split("_")
        self.model = splitie[0]
        self.emissions = splitie[1]   
        self.variable = splitie[-1]
        self.activeF[self.variable] = dS
        self.E = self.P[self.model]
        self.F = self.E[dS]
        
        self.axes = []
        for c in self.E.axes:
          exec c.name + ' = c'
          self.axes.append(c)

    def buildCalendar(self):
        '''   Data model for calendar:  tuple
                    (  <int index> , <datetime dateT>, <int lenghtMonth> )
        '''
        Y,M,D = self.F.grid[0].units.split(" ")[-1].split("-")
        self.origin_t = datetime.date(int(Y),int(M), int(D) )
        self.t_axis = CNRM.F.grid[0].value
        self.n_t = len(self.t_axis)

        axisVals = list(self.F.grid[0].value)
        axisVals.append(30)  # 30 days in Sept (last record)

        self.listCal = []
        thisDate =  self.origin_t

        for indx in range(0,self.n_t):
            dateT = thisDate + datetime.timedelta(days=1)*axisVals[indx]
            days_in_month = axisVals[indx + 1] - axisVals[indx]
            self.listCal.append( ( indx, dateT, days_in_month ) )

    def extractDF(self, tIndx):
        '''  Extract an XY dataframe by the tIndx of the listCal
        '''
        val = self.F[tIndx,:,:].value
        val1 = val[0,:,:]
        return val1


    def buildMask(self, inputSHP):

        val = self.F[0,:,:].value

        zeros = val*np.nan
        zeros = zeros[0,:,:]
        
        self.zeros = zeros           # save this properly dimmed template

        self.crdX = self.F.grid[2]
        self.crdY = self.F.grid[1]
        self.listCoords = []

        crdsX = self.crdX.value
        crdsY = self.crdY.value

        self.dimX = len(crdsX)
        self.dimY = len(crdsY)

        thisShp = ShapeContainer(inputSHP)

        #get dims
        nRow = zeros.shape[0]
        nCol = zeros.shape[1]

        if(self.verbose):
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
                self.listCoords.append( ( (i,j) , (X,Y) , Point(X,Y) ) )

          
        for items in self.listCoords:
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


        self.mask = zeros
        

    def plotParameter(self, timeStep = 0, label = "max Temp deg C", masked = False):
        plotDate = self.listCal[timeStep][1]
        val = self.F[timeStep,:,:].value
        val0 = val[0,:,:]
        if(masked):
            val1 = val0 * self.mask
        else:
            val1 = val0
        self.testArray = val1
        CS = plt.contourf(val1)
        clb =plt.colorbar()
        clb.set_label(label)
        plt.xlabel("Easting")
        plt.ylabel("Northing")
        thisTitle = self.model+" "+self.emissions+" "+plotDate.isoformat()
        plt.title(thisTitle)
        plt.show()

    def _init_me(self):
        self.loadProject()
        self.loadDataSet()
        self.buildMask(inputSHP)
        self.buildCalendar()

    def timeToIndxT(self, inputTime):
        for i,x in enumerate(self.listCal):
            if(x[1] == inputTime):
                return i
            
    def animator(self, obj2DSeries):
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        var = obj2DSeries
        v = np.linspace(0,50,20, endpoint = True)
        z = var[0,:,:]
        fig = plt.figure()
        im = plt.contourf(z, v)
        plt.colorbar()
        ax = plt.axes(xlim =(0, self.dimX), ylim = (0, self.dimY))
        plt.xlabel(r'x')
        plt.ylabel(r'y')
        
        #animation

        global first
        first = True
        def animate(i):
            global first
            z = var[i,:,:]
            #cont = plt.contourf(z)
            cont = plt.contourf(z,v)
            plt.title(str(i))
            return cont

        self.anim = animation.FuncAnimation(fig, animate, frames = range(1,var.shape[0]))
        
        plt.show()
        self.anim.save("test.mp4")
        
    def yearAccumulator(self, listFilterMonths = [6,7,8] ):
        minYear = self.origin_t.year + 1
        maxYear = 2099
        listObjYr = []
        listYears = range(minYear, maxYear)
        n_Years = len(listYears)
        for yrs in listYears:
            listObjYr.append( (yrs, listFilterMonths) ) #

        res = self.zeros
        thisMonth = self.zeros
                        #   nYears,    nRow,                   nCol,    
        thisOne =np.zeros(  (n_Years,self.zeros.shape[0], self.zeros.shape[1]) )
        i = 0
        for yrs in listObjYr:
            #  grab
            for mnths in yrs[1]:
                #print yrs,mnths,1
                indxT = self.timeToIndxT(datetime.date(yrs[0],mnths,1))
                #print indxT
                dF = self.extractDF( indxT )
                maxes = np.fmax(thisMonth, dF  )
                thisMonth = maxes
                #print maxes
            thisOne[i,...] = thisMonth
            i = i + 1
        return thisOne

CNRM = SpaceGridsProj()
#CNRM.loadProject()
#CNRM.loadDataSet()
#CNRM.buildMask(inputSHP)
#CNRM.buildCalendar()
CNRM._init_me()
CNRM.thisOne = CNRM.yearAccumulator()
#CNRM.animator(CNRM.thisOne)
#CNRM.plotParameter(9,masked = True)



#showMeTime(1)
#showMeTime(2)

































