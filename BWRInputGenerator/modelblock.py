from aliasblock import *

def myround(x, base): return int(base * round(float(x)/base))

def getglobalgrid(pinpitch,asspitch,gridsperpin=4.0):
  idealgridsize = pinpitch/gridsperpin
  grids = myround(asspitch/idealgridsize, gridsperpin)
  return ' {0} {0} '.format(grids,grids)

def getnewtcylinders(ids,radii):
  textout = ''
  for i in range(0,len(ids)):
    textout += '  cylinder {0} {1} \n'.format(ids[i], radii[i])
  return textout

def getk6cylinders(ids,radii,zlen):
  textout = ''
  for i in range(0,len(ids)):
    textout += '  cylinder {0} {1}  {2} {3} \n'.format(ids[i], radii[i],zlen,0.0)
  return textout


def getmedia(cylids,mats):
  textout = ''
  for i in range(0,len(cylids)):
    if i == 0:
      textout += '  media {0} 1  {1} \n'.format(mats[i],cylids[i])
    else:
      textout += '  media {0} 1 -{1} {2} \n'.format(mats[i],cylids[i-1],cylids[i])
  return textout

def diagonals(latsize):
  thisnum = -1
  diags = []
  for i in range(1,10+1):
    thisnum += i
    diags.append(thisnum)
  return diags


def getallpins(pins,seq,geom='2d',zlen=None):
  allpinstext = ''
  for id in pins:
    thisunit = 'unit ' + str(id) + ' \n'
    cylinderids = range(1,len(pins[id][0]))
    radii, mats = pins[id][0][0:-1], pins[id][1][0:-1]
    boundary = '  boundary  {0} \n'.format(cylinderids[-1])
    if geom == '2d':
      allpinstext += thisunit + getnewtcylinders(cylinderids,radii) + getmedia(cylinderids,mats) + boundary
    elif geom == '3d':
      allpinstext += thisunit + getk6cylinders(cylinderids,radii,zlen) + getmedia(cylinderids,mats) + boundary
  return allpinstext

def getpinids(arrtype):
  pinids=[]
  for i in range(0,arrtype):
    firstid=10+i
    for j in range(0,i+1): pinids.append(firstid+j*10)
  return pinids

def arrsize(array):
  return int(((1+8*len(array))**(0.5)-1)/2)

def getholespos(array,pitch):
  latsize = arrsize(array)
  if latsize%2 == 0: posmult = [x+0.5 for x in range(-latsize/2,latsize/2)]
  elif latsize%2 == 1: posmult = range(-(latsize/2),latsize/2+1)
  xposs = [x*pitch for x in posmult]
  yposs = [x*-1*pitch for x in posmult]
  xyposmult = [[[i,j] for i in xposs] for j in yposs]
  return xyposmult

def getfullarray(array):
  size = arrsize(array)
  pinids = getpinids(size)
  blankarr = [[1 for i in range(0,size)] for j in range(0,size)]
  for i in range(0,len(pinids)):
    if len(list(str(pinids[i]))) < 3:
      yindex = int(list(str(pinids[i]))[0])-1
      xindex = int(list(str(pinids[i]))[1])
    else:
      yindex = int(list(str(pinids[i]))[0]+list(str(pinids[i]))[1])-1
      xindex = int(list(str(pinids[i]))[2])
    blankarr[yindex][xindex] = array[i]
    blankarr[xindex][yindex] = array[i]
  return blankarr

def getholetext(fulllat,pinpos,allpins,offset):
  holetext = ''
  for i in range(0,len(fulllat[0])):
    for j in range(0,len(fulllat)):
      if len(all_indices(fulllat[i][j],allpins.keys())) != 0:
        if fulllat[i][j] != 0: holetext += "  hole {0}  origin x={1:>8.4f}  y={2:>8.4f} \n".format(fulllat[i][j],pinpos[i][j][0]+offset,pinpos[i][j][1]-offset)
  return holetext

def getpns(aliases):
  pns=[]
  for alias in aliases:
    if alias.find('gap') != -1:
      pns.append(0)
    elif alias.find('mod') != -1:
      pns.append(2)
    else:
      pns.append(1)
  return pns

def getcoms(aliases):
  coms=[]
  for alias in aliases:
    if alias.find('$f') != -1:
      enrgd = alias.replace('$f','').split('gd')
      if len(enrgd) > 1:
        coms.append('{0}% enr, {1}wt% Gd2O3 fuel'.format(float(enrgd[0])/100.0,float(enrgd[1])/10.0))
      else:
        coms.append('{0}% enr fuel'.format(float(enrgd[0])/100.0))
    elif alias.find('$1f') != -1:
      enrgd = alias.replace('$1f','').split('gd')
      if len(enrgd) > 1:
        coms.append('One {0}% enr, {1}wt% Gd2O3 fuel'.format(float(enrgd[0])/100.0,float(enrgd[1])/10.0))
      else:
        coms.append('One {0}% enr fuel'.format(float(enrgd[0])/100.0))
    else:
      coms.append(alias.replace('$',''))
  return coms

def getnewtmaterials(aliases,seq):
  aliasnames = [ part[0].split()[0] for part in aliases ]
  pns = getpns(aliasnames)
#  coms = getcoms(aliasnames)
  materialstext = 'read materials \n'
  for i in range(0,len(aliasnames)):
    if seq == 'tnewt':
      if aliasnames[i].find('$f') == -1:
        materialstext += "  mix={0:<12}  pn={1}  com='{2}'  end\n".format(aliasnames[i], pns[i], aliasnames[i].replace('$',''))
    elif seq == 'tdepl':
      if aliasnames[i].find('$1f') == -1:
        materialstext += "  mix={0:<12}  pn={1}  com='{2}'  end\n".format(aliasnames[i], pns[i], aliasnames[i].replace('$',''))
  materialstext += 'end materials \n'
  return materialstext

def offsetgeom(file,offset):
  f = file
  for i in range(0,len(f)):
    if f[i].find('<pos>') != -1 or f[i].find('<mos>') != -1:
      thisline = f[i].split(' ')
      for j in range(0,len(thisline)):
        if thisline[j].find('<pos>') != -1:
          thisline[j-1] = '{0}'.format(float(thisline[j-1]) + offset)
          thisline[j] = ''
        if thisline[j].find('<mos>') != -1:
          thisline[j-1] = '{0}'.format(float(thisline[j-1]) - offset)
          thisline[j] = ''
      thispart = '' + ' '.join(thisline) + '\n'
      f[i] = thispart.replace('\n\n','\n')
#      f[i] = '  ' + ' '.join(thisline) + '\n'
  return f

def makechangeom(file,apitch, wchan, tchan, ricorner, tcorner, wcutout):
  dims = {}
  wcutoutmod = wcutout
  if wcutout == 0: wcutoutmod = tcorner*0.5
  dims['ricorner']   = ricorner
  dims['rocorner']   = ricorner + tcorner
  dims['boxcorner']  = (ricorner + tcorner)*1.05
  if wcutout == 0:
    dims['hwcutout']   = (tcorner*0.5)/2.0
    dims['tcutout']    = tcorner
  else:
    dims['hwcutout']   = wcutout/2.0
    dims['tcutout']    = tcorner - tchan
  dims['hwichan']    = wchan/2.0
  dims['hwochan']    = dims['hwichan'] + tcorner
  dims['hwassem']    = apitch/2.0
  dims['cornorig']    = dims['hwichan'] - ricorner
  dims['cutoutorig'] = dims['hwochan']
  dims['cornboxedge'] = dims['cornorig'] + dims['rocorner']*1.05
  for i in range(0,len(file)):
    for key in dims:
      file[i] = file[i].replace('<' + key + '>',str(dims[key]))
    if wcutout == 0: file[i] = file[i].replace("  hole 999","'  hole 999")
  return file

def getotherpins(otherpins,offset,zlen=None):
  counter,unitnum,surfstart = 0, 1000, 10
  holesnums = {}
  otherpintext = ''
  pinnumloc = {}
  for key in otherpins:
    unitnum += 1
    thisunit = 'unit ' + str(unitnum) + ' \n'
    cylinderids = range(1,len(otherpins[key][0])+1)
    radii, mats = otherpins[key][0], otherpins[key][1]
    boundary = '  boundary  {0} \n'.format(cylinderids[-1])
    if zlen==None:
      otherpintext += thisunit + getnewtcylinders(cylinderids,radii) + getmedia(cylinderids,mats) + boundary
    else:
      otherpintext += thisunit + getk6cylinders(cylinderids,radii,zlen) + getmedia(cylinderids,mats) + boundary
    pinnumloc[unitnum] = [otherpins[key][2][0] + offset, otherpins[key][2][1] - offset]
  return otherpintext,pinnumloc

def getotherpinholes(otherholes):
  otherholetext = ''
  for hole in otherholes:
    otherholetext += '  hole {0} origin x= {1} y= {2} \n'.format(hole,otherholes[hole][0],otherholes[hole][1])
  return otherholetext

def getnewtcorns():
  cornersurfs =  '  cylinder  6 <ricorner>  <zdims>   chord +x= <cornorig> <pos> chord +y= <cornorig> <mos>  origin x=  <cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cylinder  7 <rocorner>  <zdims>   chord +x= <cornorig> <pos> chord +y= <cornorig> <mos>  origin x=  <cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cuboid    8 <cornboxedge> <pos> <cornorig> <pos>  <cornboxedge> <mos> <cornorig> <mos>  <zdims> \n'
  cornersurfs += '  cylinder  9 <ricorner>  <zdims>   chord -x= -<cornorig> <pos> chord +y= <cornorig> <mos>  origin x= -<cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cylinder 10 <rocorner>  <zdims>   chord -x= -<cornorig> <pos> chord +y= <cornorig> <mos>  origin x= -<cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cuboid   11 -<cornorig> <pos> -<cornboxedge> <pos> <cornboxedge> <mos> <cornorig> <mos>  <zdims> \n'
  cornersurfs += '  cylinder 12 <ricorner>  <zdims>   chord -x= -<cornorig> <pos> chord -y= -<cornorig> <mos>  origin x= -<cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cylinder 13 <rocorner>  <zdims>   chord -x= -<cornorig> <pos> chord -y= -<cornorig> <mos>  origin x= -<cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cuboid   14 -<cornorig> <pos> -<cornboxedge> <pos> -<cornorig> <mos> -<cornboxedge> <mos>  <zdims> \n'
  cornersurfs += '  cylinder 15 <ricorner>  <zdims>   chord +x=  <cornorig> <pos> chord -y= -<cornorig> <mos>  origin x=  <cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cylinder 16 <rocorner>  <zdims>   chord +x=  <cornorig> <pos> chord -y= -<cornorig> <mos>  origin x=  <cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cuboid   17 <cornboxedge> <pos> <cornorig> <pos>  -<cornorig> <mos> -<cornboxedge> <mos>  <zdims> \n'
  return cornersurfs

def getkenocorns():
  cornersurfs =  '  cylinder  6 <ricorner>  <zdims>   origin x=  <cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cylinder  7 <rocorner>  <zdims>   origin x=  <cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cuboid    8 <cornboxedge> <pos> <cornorig> <pos>  <cornboxedge> <mos> <cornorig> <mos>  <zdims> \n'
  cornersurfs += '  cylinder  9 <ricorner>  <zdims>   origin x= -<cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cylinder 10 <rocorner>  <zdims>   origin x= -<cornorig> <pos>  y=  <cornorig> <mos> \n'
  cornersurfs += '  cuboid   11 -<cornorig> <pos> -<cornboxedge> <pos> <cornboxedge> <mos> <cornorig> <mos>  <zdims> \n'
  cornersurfs += '  cylinder 12 <ricorner>  <zdims>   origin x= -<cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cylinder 13 <rocorner>  <zdims>   origin x= -<cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cuboid   14 -<cornorig> <pos> -<cornboxedge> <pos> -<cornorig> <mos> -<cornboxedge> <mos>  <zdims> \n'
  cornersurfs += '  cylinder 15 <ricorner>  <zdims>   origin x=  <cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cylinder 16 <rocorner>  <zdims>   origin x=  <cornorig> <pos>  y= -<cornorig> <mos> \n'
  cornersurfs += '  cuboid   17 <cornboxedge> <pos> <cornorig> <pos>  -<cornorig> <mos> -<cornboxedge> <mos>  <zdims> \n'
  return cornersurfs

def getkeno2dplot(assempitch,zlen):
  rtntext = 'read plot \n'
  rtntext += "  ttl='z={0} cm' \n".format(zlen/2.0)
  rtntext += '  TYP=XY \n'
  rtntext += '  XUL=-{0} YUL={0}  ZUL={1} \n'.format(assempitch/2.0 + assempitch*0.02,zlen/2.0)
  rtntext += '  XLR={0}  YLR=-{0} ZLR={1} \n'.format(assempitch/2.0 + assempitch*0.02,zlen/2.0)
  rtntext += '  NAX=2560 end \n'
  rtntext += 'end plot'
  return rtntext

class modelblockclass:
  def __init__(self, fuellat, fuelpins, mats, pinpitch, offset, otherpins, aliases=[], geom='basic',seq='tnewt',zlen=None):

    allpins = {}
    if seq == 'tdepl' or seq == 't6depl':
      for key in fuelpins:
        for index in fuelpins[key]['latindices']:
          allpins[index] = [fuelpins[key]['newtdims'] + [pinpitch], [ str(x) for x in fuelpins[key]['deplpins'][index] + fuelpins[key]['newt1fmats'][-3:]]]
    else:
      for key in fuelpins:
        allpins[key] = [fuelpins[key]['newtdims'] + [pinpitch], [str(x) for x in fuelpins[key]['newt1fmats']]]

    fulllat = getfullarray(fuellat)
    holepos = getholespos(fuellat,pinpitch)

    self.holetext = getholetext(fulllat,holepos,allpins,offset)
    self.allnewtpinstext = getallpins(allpins,seq,geom='2d')
    self.allk6pinstext = getallpins(allpins,seq,geom='3d',zlen=zlen)
    self.newtmaterials = getnewtmaterials(aliases,seq)
    self.otherpinstext = getotherpins(otherpins,offset,zlen)[0]
    self.otherpinholes = getotherpinholes( getotherpins(otherpins,offset)[1] )
    self.newtcornsurfs = getnewtcorns()
    self.kenocornsurfs = getkenocorns()
