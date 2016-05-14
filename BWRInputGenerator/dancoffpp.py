# dancoffpp.f90

import sys
import os

danfiles = str(sys.argv[1])
arrsize = int(sys.argv[2])
pitch = float(sys.argv[3])

os.system('grep -h "Unit\|92235" {0} > danfile'.format(danfiles))

f = open('./danfile').readlines()
danpos = []
#arrsize=10
#pitch = 1.2954
minxy = [100.0,100.0]
danarray = [[0.00 for i in range(0,arrsize)] for j in range(0,arrsize)]
strout = ''

#for el in danarray: print el

for i in range(0,len(f),2):
  danpos.append([float(f[i].split()[5]), float(f[i].split()[7]),float(f[i+1].split()[2])])
  if float(f[i].split()[5]) < minxy[0] : minxy[0] = float(f[i].split()[5])
  if float(f[i].split()[7]) < minxy[1] : minxy[1] = float(f[i].split()[7])

for i in range(0,len(danpos)):
  danpos[i][0] = danpos[i][0] - minxy[0] + pitch/2.0
  danpos[i][1] = danpos[i][1] - minxy[1] + pitch/2.0
#  print danpos[i]

for i in range(0,len(danpos)):
  xpos = danpos[i][0]
  ypos = danpos[i][1]
  for j in range(0,arrsize):
    if j*pitch < xpos and xpos < (j+1)*pitch:
      xind = j
    if j*pitch < ypos and ypos < (j+1)*pitch:
      yind = j
  danarray[yind][xind] = danpos[i][2]

for i in range(len(danarray)-1,-1,-1):
  strout = ''
  for dan in danarray[i][0:len(danarray)-i]:
    strout += ' {0:4.3f} '.format(dan)
  print strout



