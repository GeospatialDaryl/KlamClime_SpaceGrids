# =============================
# This python script creates a figure of vertical temperature profiles of the test model output. The output is not intended to be an accurate approximation of reality, but is for test purposes.
# =============================

import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import griddata

# This is the SG module:
import spacegrids as sg

# run sg.info() to obtain a dictionary of project names vs project paths. The names are read from text file called "projname" in each (sub)directory of ~/PROJECTS/. The presence of this small text file is used to indicate a project directory. 

#D = sg.info()
D = sg.info(rootdir = r"X:\\_05_KlamClime\\05_Data_Spacegrids")

# start a project object P using the path to that project as argument. This path is easily referenced via the project name and the dictionary D obtained above.
# SG will look through all the subdirectories of that path that contain netcdf files to create experiment objects. (If you put a directory masks in your project path, it will load the masks inside that directory as well.)
# note that D['something'] in the following is a path.

P = sg.Project(D['my_project'],expnames = 'DP*')

# Give the experiment objects convenient names E, E2:

E = P['DPO'];E2 = P['DPC']

# bring axes into namespace. e.g. X,Y,Z. The experiment objects will contain a list of axes in their axes attribute.
for c in E.axes:
  exec c.name + ' = c'

varname = 'O_temp'

# We can load fields from the netcdf file. This is where we do the actual IO and load these fields into the memory:

P.load([varname])

#Take vertical profiles of global horizontal averages (convert to Celcius):

mT = E[varname]/(X*Y) 
mT2 = E2[varname]/(X*Y) 

dmT = mT2 - mT

mST = E[varname][Z,0]/X
mST2 = E2[varname][Z,0]/X

# Informative report on deep ocean temperature difference on stdout:
kk=16
print 'T difference 1 at depth '+str((Z*mT.gr)[kk]) +' is ' +str(dmT[kk])

# Parameter preparation for figure layout:

lbl = ord('a')

pan = 0

height = 2
width = 2

rows = 2
cols = 2

# start creating subplots and plot:

ax = plt.subplot2grid((height, width), (int(np.floor(pan/cols)), pan%cols) )

plt.yticks(np.arange(-7000,0,1000),np.arange(-7,0,1))

plt.title('('+ chr(lbl) +') Ocean temperature profile ')

plt.grid()

p1, = sg.plot(mT, color = 'k')
p2, = sg.plot(mT2, color = 'r')

plt.xlabel('$^\circ C$')
plt.ylabel('Depth (m)')

plt.legend([p1,p2],['DP open','DP closed'],loc=4)

lbl += 1
pan += 1

ax = plt.subplot2grid((height, width), (int(np.floor(pan/cols)), pan%cols) )

plt.title('('+ chr(lbl) +') Zonal avg. SST  ')

plt.grid()

p1, = sg.plot(mST, color = 'k')
p2, = sg.plot(mST2, color = 'r')

plt.xticks([-90,-60,-30,0,30,60,90])

plt.ylabel('$^\circ C$')
plt.xlabel('Latitude')


# could use this to prepare for a next panel in future:
lbl += 1
pan += 1



plt.show()
