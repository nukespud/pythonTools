# burndatablock.py

import sys
import math

def autodeplsteps(basestep=0.312, bigstep=3.0 ,maxbu=50, maxsubbu=25, powden=25):
  # defaults and polynomial based on a 5Wt% gd mini lattice calculation
  fx = '0.00006358452098 - 4.584790264E-6*x - 9.129766491E-8*x**2 + 2.012447523E-8*x**3 - 9.228367237E-10*x**4 + 2.087975499E-11*x**5 - 2.015787414E-13*x**6'
  fpx = '-4.584790264E-6 - 1.825953298E-7*x + 6.03734257E-8*x**2 - 3.691346895E-9*x**3 + 1.043987749E-10*x**4 - 1.209472448E-12*x**5'
  x=0
  y0=eval(fx)
  x=basestep
  y1=eval(fx)
  rise = y1 - y0
  blocktext = ''
  totbu = 0
  steps = 0
  startstep = 0.01
  blocktext += 'read burndata \n'
  blocktext += '  power={0}  burn={1:.5f}'.format(powden, startstep) + ' nlib=1  down=0  end \n'
  while totbu < maxbu:
    if totbu < maxsubbu:
      x = totbu
      step = rise/eval(fpx)
    else:
      step = bigstep
    if step > bigstep:
      step = bigstep
    totbu = totbu + step
    steps = steps + 1
    blocktext += '  power={0}  burn={1:.5f}'.format(powden, step/(powden/1000.)) + ' nlib=1  down=0  end \n'
  blocktext += '  power={0}  burn={1:.5f}'.format(powden, step/(powden/1000.)) + ' nlib=1  down=0  end \n'
  blocktext += 'end burndata \n'
  return blocktext

def midpoints(array):
  points = array
  mps = [0] + [ (points[i] + points[i+1])/2.0   for i in range(0,len(points)-1) ]
  mps += [ 2*array[-1] - mps[-1] ]
  return mps

def userdeplsteps(powden, busteps):
  blocktext = 'read burndata \n'
  mps = midpoints(busteps)
  for i in range(0,len(mps)-1):
    blocktext += '  power={0}  burn={1:.5f}'.format(powden, (mps[i+1] - mps[i])/(powden/1000.0)) + ' nlib=1  down=0  end \n'
  blocktext += 'end burndata \n'
  return blocktext

class burndatablockclass:
  def __init__(self,powden=25, maxbu=50, busteps=[]):
    self.text = ''
    if len(busteps) != 0:
      self.text = userdeplsteps(powden, busteps)
    else:
      self.text += autodeplsteps(powden=powden, maxbu=maxbu,basestep=0.35)
