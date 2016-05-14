# celldatablock.py

from math import *

def pinrings(radius,numrings):
  rings=[]
  areabasering = pi*radius**2/float(numrings)
  for i in range(1,numrings+1):
    rings.append((areabasering*float(i)/pi)**0.5)
  return rings

def wigseitz(pitch):
  return pitch/(pi)**0.5


def latticecell(mixes,dims,df=0):
  latcelltext = ''
  latcelltext += '\n  latticecell squarepitch  pitch={0:>10.5f}  {1}\n'.format(dims[3],mixes[3])
  latcelltext += '                           fuelr={0:>10.5f}  {1}\n'.format(dims[0],mixes[0])
  latcelltext += '                           gapr= {0:>10.5f}  {1}\n'.format(dims[1],mixes[1])
  latcelltext += '                           cladr={0:>10.5f}  {1} end\n'.format(dims[2],mixes[2])
  if df != 0: latcelltext += '  centrmdata dan2pitch({0})={1:5.3f} end centrmdata\n'.format(mixes[0],df)
  return latcelltext

def multiregioncell(mixes,dims,df=0):
  multiregtext = ''
  multiregtext += '\n  multiregion cylindrical right_bdy=white end'
  dims[-1] = wigseitz(dims[-1])
  for i in range(0,len(mixes)):
    multiregtext += '\n      {0}  {1:>10.7f}'.format(mixes[i],dims[i])
  multiregtext += ' end zone\n'
  if df != 0: multiregtext += '  centrmdata dan2pitch({0})={1:5.3f} end centrmdata\n'.format(mixes[-4],df)
  return multiregtext

class celldatablockclass:
  "This is the celldata block class"
  def __init__(self, pins,mats,pitch):
    self.latcells = ''
    self.mrcells = ''
    self.allcells = ''
    for key in pins:
      if pins[key]['flrings'] <= 1:
        self.latcells += latticecell(pins[key]['newt1fmats'], pins[key]['newtdims'] + [pitch] ,df=pins[key]['df'])
      elif pins[key]['flrings'] > 1:
        self.mrcells += multiregioncell(pins[key]['newt1fmats'], pins[key]['newtdims'] + [pitch] ,df=pins[key]['df'])

    self.allcells = "read celldata \n" + self.latcells + self.mrcells + "\n end celldata"


