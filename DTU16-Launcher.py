# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 22:51:54 2021

@author: plinio silva
"""

import subprocess as sp
from subprocess import PIPE, STDOUT
import time
import datetime
import os
import re

cwd = os.getcwd()

filename = 'test1234.txt'
timeini = "2021-05-11 10:00:00"
timeend = "2021-06-11 10:00:00"
timestep = "900"
latlon = "-24.2 -42.1"
carisfile = "caris.tid"



#%%
def jd2datetime(init_datetime,date):
    date = float(date)
    tt = init_datetime + datetime.timedelta(days = date)
    tt = tt.replace(microsecond=0)
    return tt
        
#%%Referencia do tempo em 1985. O time.time() retorna segundos desde 1970, entao esse ira converter. 
timedelta = time.strptime("1 1 1985 00:00:00", "%d %m %Y %H:%M:%S")
timedelta = time.mktime(timedelta) 

#converte de timestamp (1970) para datetime
datetime.datetime.fromtimestamp(0)
#converte de datetime para timestamp (1970)
round(datetime.datetime.now().timestamp())
#%%Converting datetime to timestamp
ini = datetime.datetime.strptime(timeini,"%Y-%m-%d %H:%M:%S").timestamp()
ini = ini - timedelta
ini = "%.0f"%ini

end = datetime.datetime.strptime(timeend,"%Y-%m-%d %H:%M:%S").timestamp()
end = end - timedelta
end = "%.0f"%end

#%%
# p = sp.Popen(r'C:\Users\plinio silva\Desktop\DTU16\gettidewin.exe', close_fds = True,stdin=PIPE, stdout=PIPE, stderr=PIPE,shell = True,cwd= cwd,universal_newlines = True)
p = sp.Popen(r'gettidewin.exe', close_fds = True,stdin=PIPE, stdout=PIPE, stderr=PIPE,shell = True,cwd= cwd,universal_newlines = True)
time.sleep(1)
p.stdin.write("%s\n"%filename)
time.sleep(1)
p.stdin.write("%s\n"%ini)
time.sleep(1)
p.stdin.write("%s\n"%end)
time.sleep(1)
p.stdin.write("%s\n"%timestep)
time.sleep(1)
p.stdin.write("%s\n"%latlon)

r,e  = p.communicate(timeout = 3600)
print(r)
print(e)

#%%
with open(filename) as f:
    data = f.read()
    f.close()
    
temp = re.findall("([\d.]+)[\s]+([-\d.A-Z]+)",data)
tide = list(map(lambda x: float(x[1]),temp))

init_datetime = datetime.datetime(1985,1,1)
time = list(map(lambda x: jd2datetime(init_datetime,x[0]),temp))

#%%
with open(carisfile,'w') as f:
    f.write('--------\n')
    for ix,aux in enumerate(tide):
        pass
        tide[ix]
        d = time[ix].strftime("%Y/%m/%d")
        t = time[ix].strftime("%H:%M:%S")
        temp = "%s\t%s\t%.4f\n"%(d,t,tide[ix])
        f.write(temp)
        pass
    f.close()



