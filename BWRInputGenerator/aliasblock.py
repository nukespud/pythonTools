# aliasblock.py

from celldatablock import pinrings
from math import *

def arrsize(array):
  return int(((1+8*len(array))**(0.5)-1)/2)

def getpinids(arrtype):
  pinids=[]
  for i in range(0,arrtype):
    firstid=10+i
    for j in range(0,i+1): pinids.append(firstid+j*10)
  return pinids

def all_indices(value, qlist):
  indices = []
  idx = -1
  while True:
    try:
      idx = qlist.index(value, idx+1)
      indices.append(idx)
    except ValueError:
      break
  return indices

def prettyprint(aliasnums,latsize):
  blankarr = [['    ' for x in range(0,latsize)] for x in range(0,latsize)]
  thisblock = '  ' + aliasnums.split()[0]
  aliasnamelen = len(aliasnums.split()[0])
  aliasnums = aliasnums.split()[1:len(aliasnums.split())-1]
  aliasnums = [str(int(x) - 10) for x in aliasnums]
  for i in range(0,len(aliasnums)):
    if int(aliasnums[i]) < 10:
      aliasnums[i] = '0' + aliasnums[i]
  for num in aliasnums:
    blankarr[int(list(num)[0])][int(list(num)[1])] = ' ' + str(int(num)+10) + ' '
  for part in blankarr:
    thisblock += ''.join(part) + '\n' + " "*aliasnamelen + "  "
  thisblock += 'end'
  return thisblock.replace('\n'+" "*aliasnamelen+'  end','  end\n')

def getallpinids(singlepins,lattice,pinids):
  allpins = {}
  for i in range(0,len(lattice)):
    if lattice[i] != 0: allpins[pinids[i]] = singlepins[lattice[i]]
  return allpins

def getalldeplpinids(singlepins,lattice,pinids,alldeplpins,allnodeplpins):
  allpins = {}
  for key in alldeplpins:
    allpins[key] = [ allnodeplpins[key][0], alldeplpins[key][1] + allnodeplpins[key][1][len(alldeplpins[key][1]):] ]
  return allpins

class onefuelaliasclass:
  def __init__(self,start):
    self.onefuelaliases=[start]
  def get(self):
    self.onefuelaliases.append(self.onefuelaliases[len(self.onefuelaliases)-1]+1)
    return self.onefuelaliases[len(self.onefuelaliases)-1]

class otheraliasclass:
  def __init__(self,start):
    self.otheraliases=[start]
  def get(self):
    self.otheraliases.append(self.otheraliases[len(self.otheraliases)-1]+1)
    return self.otheraliases[len(self.otheraliases)-1]

class aliasblockclass:
  def __init__(self, fuelpins, mats):
    fuelaliases=[]
    onefuelaliases=[]
    onefuelaliasnum = onefuelaliasclass(700)
    gapaliases=[]
    cladaliases=[]
    modaliases=[]
    # these limit the total number of gap/clad/mod mixtures to 25
    gapcladmodstart=[800,825,850]
    otheraliasesnum = otheraliasclass(1000)
    otheraliases = []

    numaliases=0
    eachpindict={}
    singlepindict = {}


    for key in fuelpins:
      fuelpins[key]['newtdims'] = pinrings(fuelpins[key]['dims'][0],fuelpins[key]['flrings']) + fuelpins[key]['dims'][1:]
      fuelpins[key]['newt1fmats'] = [onefuelaliasnum.get() for i in range(0,fuelpins[key]['flrings'])] + [gapcladmodstart[0]+numaliases,gapcladmodstart[1]+numaliases,gapcladmodstart[2]+numaliases]
      fuelpins[key]['deplpins'] = {}
      for index in fuelpins[key]['latindices']:
        if fuelpins[key]['flrings'] == 1:
          fuelpins[key]['deplpins'][index] = [index]
        elif fuelpins[key]['flrings'] > 1:
          fuelpins[key]['deplpins'][index] = [index*10 + i + 1 for i in range(0,fuelpins[key]['flrings'])]
      gapaliases.append(gapcladmodstart[0]+numaliases)
      cladaliases.append(gapcladmodstart[1]+numaliases)
      modaliases.append(gapcladmodstart[2]+numaliases)
      numaliases = numaliases + 1

    for key in mats:
      if mats[key]['type'] == 'fuel':
        for pin in fuelpins:
          if key == fuelpins[pin]['mats'][0]:
            mats[key]['1flnums'] = fuelpins[pin]['newt1fmats'][0:-3]
            thesemats=[]
            for index in fuelpins[pin]['latindices']:
              thesemats +=  fuelpins[pin]['deplpins'][index]
            mats[key]['flnums'] = thesemats
      elif mats[key]['type'] == 'gap':
        mats[key]['matnums'] = gapaliases
      elif mats[key]['type'] == 'clad':
        mats[key]['matnums'] = cladaliases
      elif mats[key]['type'] == 'mod':
        mats[key]['matnums'] = modaliases
      else:
        mats[key]['matnums'] = [otheraliasesnum.get()]


    deplaliasblocktext = 'read alias\n'
    nodeplaliasblocktext = 'read alias\n'
    oneflaliases = []
    flaliases = []
    otheraliases = []
    for i in range(0,3):
      for key in mats:
        if mats[key]['type'] == 'fuel':
          if i == 0:
            deplaliasblocktext += '  $1f{0}   {1} end\n'.format(key, ' '.join( [str(num) for num in mats[key]['1flnums']] ) )
            nodeplaliasblocktext += '  $1f{0}   {1} end\n'.format(key, ' '.join( [str(num) for num in mats[key]['1flnums']] ) )
            oneflaliases.append(['$1f{0}'.format(key)] + [str(num) for num in mats[key]['1flnums']] )
          elif i == 1:
            deplaliasblocktext += '  $f{0}   {1} end\n'.format(key, ' '.join( [str(num) for num in mats[key]['flnums']] ) )
            flaliases.append( ['$f{0}'.format(key)] + [str(num) for num in mats[key]['flnums']])
        else:
          if i == 2:
            deplaliasblocktext += '  ${0}   {1} end\n'.format(key, ' '.join( [str(num) for num in mats[key]['matnums']] ) )
            nodeplaliasblocktext += '  ${0}   {1} end\n'.format(key, ' '.join( [str(num) for num in mats[key]['matnums']] ) )
            otheraliases.append( ['${0}'.format(key)] + [str(num) for num in mats[key]['matnums']] )
    deplaliasblocktext += 'end alias\n'
    nodeplaliasblocktext += 'end alias\n'

    self.depltext = deplaliasblocktext
    self.nodepltext = nodeplaliasblocktext
    self.oneflaliases = oneflaliases
#    print self.oneflaliases
    self.flaliases = flaliases
    self.otheraliases = otheraliases

