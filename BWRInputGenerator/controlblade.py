# control blade class

def controlbladetext(cbtype,cbunit,tubeir=0.17526, tubeor=0.23876, tubep=0.47752, npins=21, halfspan=12.5825, halft=0.39624, sheatht=0.14224, cst=0.39624, csw=2.21234, tipr=0,
                 pois='cbpois',clad='cbclad',struct='cbstru',outmod='mod1'):
  cbtext = ''
  pincyltext=''
  pinmedtext=''
  cuboidids=[10,20,30]
  ircylids=[]
  orcylids=[]
  pinxpos=[]
  if cbtype=='right':
    cbtext += 'unit {0}\n'.format(cbunit)
    if halft != cst: cbtext += '  cuboid   {4}  {0} {1}  -{2} -{3}  <zdims>\n'.format(csw,cst,cst,halft,cuboidids[0])
    cbtext += '  cuboid   {4}  {0} {1}  {2} -{3}  <zdims>\n'.format(halfspan-sheatht,csw+sheatht,0.0,halft-sheatht,cuboidids[1])
    cbtext += '  cuboid   {4}  {0} {1}  {2} -{3}  <zdims>\n'.format(halfspan,0.0,0.0,halft,cuboidids[2])
    for i in range(0,npins):
      ircylids.append(cuboidids[2]+i*2+1)
      orcylids.append(cuboidids[2]+i*2+2)
      if i == 0:  pinxpos.append(csw+sheatht+tubep/2.0)
      else: pinxpos.append(pinxpos[-1]+tubep)
      pincyltext += '  cylinder {0}  {1}  <zdims>                chord -y=0  origin x={2}\n'.format(ircylids[-1],tubeir,pinxpos[-1])
      pincyltext += '  cylinder {0}  {1}  <zdims>                chord -y=0  origin x={2}\n'.format(orcylids[-1],tubeor,pinxpos[-1])
      pinmedtext += '  media  <{1}>  1   {0}\n'.format(ircylids[-1],pois)
      pinmedtext += '  media  <{2}>  1  -{0} {1}\n'.format(ircylids[-1],orcylids[-1],clad)
    cbtext += pincyltext
    cbtext += pinmedtext
    if halft != cst:  cbtext += '  media    <{1}> 1  {0}\n'.format(cuboidids[0],outmod)
    cbtext += '  media    <{2}> 1  {1}  {0}\n'.format(cuboidids[1],' '.join([str(-x) for x in orcylids]),outmod)
    if halft != cst:
      cbtext += '  media    <{3}> 1 -{0} -{1}  {2}\n'.format(cuboidids[0],cuboidids[1],cuboidids[2],struct)
    else:
      cbtext += '  media    <{2}> 1 -{0}  {1}\n'.format(cuboidids[1],cuboidids[2],struct)
    cbtext += '  boundary {0}\n'.format(cuboidids[2])
  elif cbtype=='bottom':
    cbtext += 'unit {0}\n'.format(cbunit)
    if halft != cst: cbtext += '  cuboid   {4}  {0} {1}   {3} {2}  <zdims>\n'.format(csw,halft,cst,halft,cuboidids[0])
    cbtext += '  cuboid   {4}  {0} {1}  {3}  {2}  <zdims>\n'.format(halfspan-sheatht,csw+sheatht,0.0,halft-sheatht,cuboidids[1])
    cbtext += '  cuboid   {4}  {0} {1}  {3}  {2}  <zdims>\n'.format(halfspan,halft,0.0,halft,cuboidids[2])
    for i in range(0,npins):
      ircylids.append(cuboidids[2]+i*2+1)
      orcylids.append(cuboidids[2]+i*2+2)
      if i == 0:  pinxpos.append(csw+sheatht+tubep/2.0)
      else: pinxpos.append(pinxpos[-1]+tubep)
      pincyltext += '  cylinder {0}  {1}  <zdims>                chord +y=0  origin x={2}\n'.format(ircylids[-1],tubeir,pinxpos[-1])
      pincyltext += '  cylinder {0}  {1}  <zdims>                chord +y=0  origin x={2}\n'.format(orcylids[-1],tubeor,pinxpos[-1])
      pinmedtext += '  media  <{1}>  1   {0}\n'.format(ircylids[-1],pois)
      pinmedtext += '  media  <{2}>  1  -{0} {1}\n'.format(ircylids[-1],orcylids[-1],clad)
    cbtext += pincyltext
    cbtext += pinmedtext
    if halft != cst:  cbtext += '  media    <{1}> 1  {0}\n'.format(cuboidids[0],outmod)
    cbtext += '  media    <{2}> 1  {1}  {0}\n'.format(cuboidids[1],' '.join([str(-x) for x in orcylids]),outmod)
    if halft != cst:
      cbtext += '  media    <{3}> 1 -{0} -{1}  {2}\n'.format(cuboidids[0],cuboidids[1],cuboidids[2],struct)
    else:
      cbtext += '  media    <{2}> 1 -{0}  {1}\n'.format(cuboidids[1],cuboidids[2],struct)
    cbtext += '  boundary {0}\n'.format(cuboidids[2])
  else:
    print '***You have a stuck control blade!!! Improper cbtype...***'
  return cbtext

class controlbladeclass:
  def __init__(self,assempitch,tubeir=0.17526, tubeor=0.23876, tubep=0.47752, npins=21, halfspan=12.5825, halft=0.39624, sheatht=0.14224, cst=0.39624, csw=2.21234, tipr=0,
               pois=['cbpois','b4c',2.49*0.7],clad=['cbclad','zirc2'],struct=['cbstru','zirc2'],outmod=['mod1']):
    self.cbunits=[996,997]
    self.assempitch=assempitch
    self.tubeir=tubeir
    self.tubeor=tubeor
    self.tubep=tubep
    self.npins=npins
    self.halfspan=halfspan
    self.halft=halft
    self.sheatht=sheatht
    self.cst=cst
    self.csw=csw
    self.tipr=tipr
    self.pois=pois
    self.clad=clad
    self.struct=struct
    self.outmod=outmod

  def getcbtext(self):
    self.rightcbunit=controlbladetext('right',self.cbunits[0],tubeir=self.tubeir, tubeor=self.tubeor, tubep=self.tubep, npins=self.npins, halfspan=self.halfspan, halft=self.halft, sheatht=self.sheatht, cst=self.cst, csw=self.csw, tipr=self.tipr,
                 pois=self.pois[0],clad=self.clad[0],struct=self.struct[0],outmod=self.outmod[0])
    self.bottomcbunit=controlbladetext('bottom',self.cbunits[1],tubeir=self.tubeir, tubeor=self.tubeor, tubep=self.tubep, npins=self.npins, halfspan=self.halfspan, halft=self.halft, sheatht=self.sheatht, cst=self.cst, csw=self.csw, tipr=self.tipr,
                 pois=self.pois[0],clad=self.clad[0],struct=self.struct[0],outmod=self.outmod[0])
    self.rightcbhole='  hole {0}  origin x=-{1} y={1}\n'.format(self.cbunits[0],self.assempitch/2.0)
    self.bottomcbhole='  hole {0}  origin x=-{1} y={1} rotate a1=-90\n'.format(self.cbunits[1],self.assempitch/2.0)
    self.cbunittext = self.rightcbunit + self.bottomcbunit
    self.cbholetext = self.rightcbhole + self.bottomcbhole
    return self.cbunittext, self.cbholetext

  def cbmats(self):
    return [self.pois,self.clad,self.struct,self.outmod]


pb2oem=controlbladeclass(15.24)
