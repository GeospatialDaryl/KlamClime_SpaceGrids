import spacegrids as sg
import matplotlib
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import ogr

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

def showMeTime(inputTime):
    sg.contourf(sg.squeeze(F[scalar,int(inputTime)]))
    clb = plt.colorbar()
    clb.set_label(F.units)
    plt.show()

showMeTime(1)
showMeTime(2)
