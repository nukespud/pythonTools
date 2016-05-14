# bwr.py, a BWR class

from matutils import *
from aliasblock import *
from celldatablock import *
from modelblock import *
from constructmodel import *
from compblock import *
from parmblock import *
from depletionblock import *
from burndatablock import *
from collapseblock import *
from homogblock import *
from adfblock import *
from controlblade import *
from dancoffs import *
from dancoffdetail import *
#
print "CPILE2 does not have numpy"
#from numpy import polyfit
import sys

class BWR:
  """This is a BWR class"""
  def __init__(self, sequence='tnewt',model='basic',fname='yourfile.inp',lib='v7',parms=''):
    self.seq = sequence
    self.model = model
    self.name = fname
    self.fuelpincomps={}
    self.cmpblock={}
    self.fuelpindims=[]
    self.fuelpinmats=[]
    self.matsdict={}
    self.fuelpinnums=[]
    self.pins={}
    self.fuelpiniddict={}
    self.othermats=[]
    self.allmats=[]
    self.libs = {'v5':'v5-238', 'v6':'v6-238', 'v7':'v7-238', 'cev7':'ce_v7'}
    self.lib = self.libs[lib]
    self.tparms='parm=({0})'.format(parms)
    self.collapseblock = ''
    self.otherpinnums = []
    self.otherpindims = []
    self.otherpinmats = []
    self.otherpinlocs = []
    self.otherpindict = {}
    self.templatedir = '/home/f4p/PYTHON_PATH/templates/'
    self.homogopt='n'
    self.homogblock=''
    self.adfopt='n'
    self.adfblock=''
    self.shellcmdse = ''
    self.shellcmdsb = ''
    self.tag = 0
    self.controlblade=None
    self.collapseopt='no'
    self.zlen=12.0*12.0*2.54
    self.pindims=[]
    self.pindfs= {}
    self.fuelpins = {}
    self.otherpins = {}
    self.mats = {}

  def hlopts(self,sequence='tnewt',model='basic',fname='yourfile.inp',lib='v7',parms=''):
    self.seq = sequence
    self.model = model
    self.name = fname
    self.lib = self.libs[lib]
    self.tparms='parm=({0})'.format(parms)

  def jobinfo(self,info):
    self.info = info

  def state(self,tfu=900,tmo=500,vf=0.45,powden=25):
    self.tfu = tfu
    self.tmo = tmo
    self.vf = vf
    self.rhof, self.rhog = h2orho(self.tmo)
    self.powden=powden

  def pitch(self,pinpitch=1.5,latpitch=15.24,offset=0):
    self.pinpitch = pinpitch
    self.latpitch = latpitch
    self.offset = offset

  def uo2(self, fuelname, type='fuel', den=10.5, enr=0.71):
    if fuelname in self.fuelpincomps: pass
    else :
      self.fuelpincomps[fuelname] = [enr]
      self.cmpblock[fuelname] = uo2stdcmp('1f'+fuelname,den,1,self.tfu,uenrichment(enr))
      self.allmats.append(fuelname)
    self.mats[fuelname] = {'enr':enr, 'temp':self.tfu,'den':den, 'mattext':uo2stdcmp('1f'+fuelname,den,1,self.tfu,uenrichment(enr)),'fltype':'uo2','type':type}

  def uo2gd(self, fuelname, type='fuel', den=10.5, enr=0.71, gd=0):
    if fuelname in self.fuelpincomps: pass
    else :
      self.fuelpincomps[fuelname] = [enr,gd]
      self.cmpblock[fuelname] = uo2gdstdcmp('1fgd'+fuelname,den,1,self.tfu,uenrichment(enr),gd)
      self.allmats.append(fuelname)
    self.mats[fuelname] = {'enr':enr, 'temp':self.tfu,'den':den, 'mattext':uo2gdstdcmp('1f'+fuelname,den,1,self.tfu,uenrichment(enr),gd),'fltype':'uo2gd','type':type}

  #  Modifed by Joshua Peterson
  #  This includes ss and inconel with user specificing percent ss
  # Zirconium with   inconel for inert rod.  Specify percent zirc2
  def inert_rd(self, name, type='inert_rd', den=5.97,tmp=1100,per_zirc2=.994):
    self.cmpblock[name] = inert_rdstdcmp(name,tmp=tmp,den=den,per_zirc2=per_zirc2)
    self.mats[name]= {'tmp':tmp,'mattext':inert_rdstdcmp(name,tmp=tmp,den=den,per_zirc2=per_zirc2),'type':type}
    self.allmats.append(name)
  
  # For Staineless steel Inert rod     Specify percent SS
  def inert_rd_ss(self, name, type='inert_rd', den=5.97,tmp=1100,per_ss=.994):
    self.cmpblock[name] = inert_rd_ss_stdcmp(name,tmp=tmp,den=den,per_ss=per_ss)
    self.mats[name]= {'tmp':tmp,'mattext':inert_rd_ss_stdcmp(name,tmp=tmp,den=den,per_ss=per_ss),'type':type}
    self.allmats.append(name) 
 
  
  # This is for cladding with stainless steel
  def ss(self, name, den=6.56,type='other'):
    if type == 'clad':
      self.cmpblock[name] = ss2stdcmp(name,tmp=(self.tfu*0.2 + self.tmo*0.8),den=den)
      self.mats[name] = {'tmp':(self.tfu*0.2 + self.tmo*0.8),'mattext':ss2stdcmp(name,tmp=(self.tfu*0.2 + self.tmo*0.8),den=den),'type':type}
    else:
      self.cmpblock[name] = ss2stdcmp(name,tmp=self.tmo,den=den)
      self.othermats.append(name)
      self.mats[name] = {'tmp':self.tmo,'mattext':ss2stdcmp(name,tmp=self.tmo,den=den),'type':type}
    self.allmats.append(name)  
  
  #  This allows the user to specify density instead of void fraction
  def h2o_den(self, name, type='other',den=.42):
    if type == 'mod':
      self.cmpblock[name] = h2ostdcmp(name,den=den, tmp=self.tmo)
      self.mats[name] = {'tmp':self.tmo,'den':den, 'mattext':h2ostdcmp(name,den=den, tmp=self.tmo),'type':type}
    else:
      self.cmpblock[name] = h2ostdcmp(name,den=twophaserho(0.0,self.tmo), tmp=self.tmo)
      self.othermats.append(name)
      self.mats[name] = {'tmp':self.tmo,'den':twophaserho(0.0,self.tmo), 'mattext':h2ostdcmp(name,den=twophaserho(0.0,self.tmo), tmp=self.tmo),'type':type}
    self.allmats.append(name) 
  
  # End of addition by Joshua
  
  def zirc2(self, name, den=6.56,type='other'):
    if type == 'clad':
      self.cmpblock[name] = zirc2stdcmp(name,tmp=(self.tfu*0.2 + self.tmo*0.8),den=den)
      self.mats[name] = {'tmp':(self.tfu*0.2 + self.tmo*0.8),'mattext':zirc2stdcmp(name,tmp=(self.tfu*0.2 + self.tmo*0.8),den=den),'type':type}
    else:
      self.cmpblock[name] = zirc2stdcmp(name,tmp=self.tmo,den=den)
      self.othermats.append(name)
      self.mats[name] = {'tmp':self.tmo,'mattext':zirc2stdcmp(name,tmp=self.tmo,den=den),'type':type}
    self.allmats.append(name)

  # Temp is either fraction of moderator (self.tfu*0.2 + self.tmo*0.8) and fuel or moderator if there is no fuel
  def zirc4(self, name, den=6.56,type='other'):
    if type == 'clad':
      self.cmpblock[name] = zirc4stdcmp(name,tmp=(self.tfu*0.2 + self.tmo*0.8),den=den)
      self.mats[name] = {'tmp':(self.tfu*0.2 + self.tmo*0.8),'mattext':zirc4stdcmp(name,tmp=(self.tfu*0.2 + self.tmo*0.8),den=den),'type':type}
    else:
      self.cmpblock[name] = zirc4stdcmp(name,tmp=self.tmo,den=den)
      self.othermats.append(name)
      self.mats[name] = {'tmp':self.tmo,'mattext':zirc4stdcmp(name,tmp=self.tmo,den=den),'type':type}
    self.allmats.append(name)
    

  def h2o(self, name, type='other'):
    if type == 'mod':
      self.cmpblock[name] = h2ostdcmp(name,den=twophaserho(self.vf,self.tmo), tmp=self.tmo)
      self.mats[name] = {'tmp':self.tmo,'den':twophaserho(self.vf,self.tmo), 'mattext':h2ostdcmp(name,den=twophaserho(self.vf,self.tmo), tmp=self.tmo),'type':type}
    else:
      self.cmpblock[name] = h2ostdcmp(name,den=twophaserho(0.0,self.tmo), tmp=self.tmo)
      self.othermats.append(name)
      self.mats[name] = {'tmp':self.tmo,'den':twophaserho(0.0,self.tmo), 'mattext':h2ostdcmp(name,den=twophaserho(0.0,self.tmo), tmp=self.tmo),'type':type}
    self.allmats.append(name)

  def he(self, name, den=0.0001, type='other'):
    if type == 'gap':
      self.cmpblock[name] = hestdcmp(name,den=0.0001, tmp=(self.tfu*0.2 + self.tmo*0.8))
      self.mats[name] = {'tmp':(self.tfu*0.2 + self.tmo*0.8),'den':0.0001, 'mattext':hestdcmp(name,den=den, tmp=(self.tfu*0.2 + self.tmo*0.8)),'type':type}
    self.allmats.append(name)

  def b4c(self, name, den=2.49, type='other'):
    self.cmpblock[name] = b4cstdcmp(name,den=den,vf=1.0,tmp=self.tmo)
    self.othermats.append(name)
    self.allmats.append(name)
    self.mats[name] = {'tmp':self.tmo,'den':den, 'mattext':b4cstdcmp(name,den=den,vf=1.0,tmp=self.tmo),'type':type}

  def lattice(self,lat):
    self.fuellat=lat

  def fuelpin(self,pinnum,dims,mats,df=0):
    if pinnum in self.fuelpinnums:
      pass
#      self.pindfs[pinnum] = df
    else:
      self.fuelpinnums.append(pinnum)
      self.fuelpindims.append(dims)
      self.fuelpinmats.append(mats)
      self.fuelpiniddict[mats[0]]=pinnum
    self.pindfs[pinnum] = df
    if self.mats[mats[0]]['fltype'] == 'uo2': rings = self.flrings
    elif self.mats[mats[0]]['fltype'] == 'uo2gd': rings = self.gdrings
    self.fuelpins[pinnum] = {'dims':dims, 'mats': mats, 'df' : df, 'flrings':rings}

  def pin(self,pinnum,dims,mats,xyloc=[0.0,0.0]):
    self.otherpinnums.append(pinnum)
    self.otherpindims.append(dims)
    self.otherpinmats.append(mats)
    self.otherpinlocs.append(xyloc)
    self.otherpindict[pinnum] = [dims,mats,xyloc]
    self.otherpins[pinnum] = {'dims': dims, 'mats': mats, 'xyloc' : xyloc}

  def wr(self,pinnum,dims,mats,xyloc=[0.0,0.0]):
    self.pin(pinnum,dims,mats,xyloc)

  def options(self,gdrings=5,flrings=1, gridsperpin=4,fluxplots='no',dfdetail='no'):
    self.gdrings=gdrings
    self.flrings=flrings
    self.gridsperpin = gridsperpin
    self.fluxplots = fluxplots
    self.dfdetail = dfdetail

  def burnups(self,max=50,steps=[]):
    self.maxburnup=max
    self.busteps=steps

  def collapse(self,groupcollapse):
    self.collapseblock = getcollpaseblock(groupcollapse,self.tparms,self.lib)
    self.collapseopt='yes'

  def homog(self):
    self.homogopt='y'

  def adf(self):
    self.adfopt='y'

  def channel(self,apitch=15.25, wchan=13.4061, tchan=0.2032, ricorner=0.9652, tcorner=0.2032, wcutout=0):
    self.apitch   = apitch
    self.wchan    = wchan
    self.tchan    = tchan
    self.ricorner = ricorner
    self.tcorner  = tcorner
    self.wcutout  = wcutout

  def gen2gdata(self):
    self.collapseopt='yes'
    self.collapse('2g')
    self.homog()
    self.adf()
    self.shellcmdse = '=shell \n  cp $TMPDIR/txtfile16 $RTNDIR/$root_name.t16 \n  cp $TMPDIR/xfile016 $RTNDIR/$root_name.x16 \nend'

  def cb(self,type='basic',tubeir=0.17526, tubeor=0.23876, tubep=0.47752, npins=21, halfspan=12.5825, halft=0.39624, sheatht=0.14224, cst=0.39624, csw=2.21234, tipr=0,
         pois=['cbpois','b4c',2.49*0.7],clad=['cbclad','zirc2'],struct=['cbstru','zirc2'],outmod=['mod1']):
    try:
      eval(type)
    except NameError:
      if type=='basic':
        self.controlblade=controlbladeclass(self.latpitch,tubeir=tubeir,tubeor=tubeor,tubep=tubep,npins=npins,halfspan=halfspan,halft=halft,sheatht=sheatht,cst=cst,csw=csw,tipr=tipr,pois=pois,clad=clad,struct=struct,outmod=outmod)
      else:
        print "\n   *****Control blade type is not defined!*****\n"
    else:
      self.controlblade = eval(type)
      self.controlblade.assempitch = self.latpitch
#    self.controlbladeclass
  def dfs(self,dfarray):
    self.dfdict = {}
    for i in range(0,len(dfarray)):
      self.dfdict[dfarray[i][0]] = [float(x) for x in dfarray[i][1].split()]

  def end(self):
    cbunitstext=''
    cbholestext=''
    print "\n  Generating your file with the name '{0}'".format(self.name)
    self.tag += 1
    homogid = 999
#   make the moderator material
    if self.tag == 1:
      if len(all_indices('mod',self.allmats)) == 0: self.h2o('mod',type='mod')
      if len(all_indices('mod1',self.allmats)) == 0: self.h2o('mod1')
      if len(all_indices('gap',self.allmats)) == 0: self.he('gap',type='gap')
      if len(all_indices('clad',self.allmats)) == 0: self.zirc2('clad',type='clad')
      if len(all_indices('can',self.allmats)) == 0: self.zirc2('can', type='struct')
      if self.controlblade != None:
        for mat in self.controlblade.cbmats():
          if len(mat) == 1:
            pass
          elif len(mat) == 2 and len(all_indices(mat[0],self.allmats)) == 0:
            eval("self.{0}('{1}',type='')".format(mat[1],mat[0]))
          elif len(mat) == 3 and len(all_indices(mat[0],self.allmats)) == 0:
            eval("self.{0}('{1}',den={2}, type='')".format(mat[1],mat[0],mat[2]))
          else:
            print "\n  I'm stuck.  This code was written with an utomost \n  importance on robustsness and usefull error messages; \n  so it probably isn't the developers' fault..."
        cbunitstext=self.controlblade.getcbtext()[0]
        cbholestext=self.controlblade.getcbtext()[1]

    self.fuellat = [int(i) for i in self.fuellat.split()]
    pinids = getpinids(arrsize(self.fuellat))

    for key in self.fuelpins:
      self.fuelpins[key]['listindicies'] = all_indices(key,self.fuellat)
      self.fuelpins[key]['latindices'] = [pinids[loc] for loc in self.fuelpins[key]['listindicies']]

    if self.dfdetail == 'yes':
      dfdetail = dancoffdetailclass(self.fuellat, self.dfdict, twophaserho(self.vf,self.tmo), self.fuelpins, self.mats)
      self.fuellat = dfdetail.fuellat

#   generate and print the alias block

    aliasblock = aliasblockclass(self.fuelpins, self.mats)

    compblock = compblockclass(self.mats,seq=self.seq)

    celldatablock = celldatablockclass(self.fuelpins, self.mats,self.pinpitch)

    if self.seq == 'tdepl' or self.seq == 't6depl': burnupsteps = burndatablockclass(self.powden,self.maxburnup,self.busteps)

    newtparmblock = getnewtparmblock(xycmfd=self.gridsperpin,prtflux=self.fluxplots,collapse=self.collapseopt)
    kenoparmblock = getkenoparmblock()

    self.otherpindict = switchmats(self.otherpindict,self.mats)

    if self.seq == 'tdepl':
      modelblock = modelblockclass(pinids,self.fuelpins,self.mats,self.pinpitch,self.offset,self.otherpindict,aliases=aliasblock.flaliases+aliasblock.otheraliases, seq=self.seq)
      depletionblock = depletionblocktext(self.fuelpins, self.mats, aliasblock.oneflaliases,aliasblock.flaliases, self.gdrings)
      if self.homogopt == 'y': self.homogblock = gethomogblock(homogid,self.mats,self.seq)
      if self.adfopt == 'y': self.adfblock = getadfblock(homogid,self.latpitch)
    elif self.seq == 'tnewt':
      modelblock = modelblockclass(self.fuellat, self.fuelpins,self.mats,self.pinpitch,self.offset,self.otherpindict, aliases=aliasblock.oneflaliases+aliasblock.otheraliases, seq=self.seq)
      if self.homogopt == 'y': self.homogblock = gethomogblock(homogid,self.mats,self.seq)
      if self.adfopt == 'y': self.adfblock = getadfblock(homogid,self.latpitch)
    elif self.seq == 't6depl':
      print '\n***** WARNING: T6-depl is not fully-support yet.  The input file created will likely end in a TRITON error. *****\n'
      modelblock = modelblockclass(pinids,self.fuelpins,self.mats,self.pinpitch,self.offset,self.otherpindict, seq=self.seq,zlen=self.zlen)
      depletionblock = depletionblocktext(self.fuelpins, self.mats, aliasblock.oneflaliases,aliasblock.flaliases, self.gdrings)
    elif self.seq == 'csas6':
      modelblock = modelblockclass(self.fuellat, self.fuelpins,self.mats,self.pinpitch,self.offset,self.otherpindict, seq=self.seq,zlen=self.zlen)
    elif self.seq == 'mcd':
      modelblock = modelblockclass(self.fuellat, self.fuelpins,self.mats,self.pinpitch,self.offset,self.otherpindict, seq=self.seq,zlen=self.zlen)
    else: print 'SEQUENCE NAME NOT RECOGNISED  - You lock it up!'

    f = open(self.name, mode="w")

    try:
      with open(self.templatedir + self.model) as testtemplate: pass
      geomtemplate = open(self.templatedir + self.model).readlines()
    except IOError as e:
      sys.exit('\n\n  ***** Template ' + self.templatedir + self.model + ' not found!!! *****\n\n')

    if self.seq == 'tdepl' or self.seq == 'tnewt':
      geomtemplate = [w.replace('<cornsurfs>',modelblock.newtcornsurfs) for w in geomtemplate]
    else:
      geomtemplate = [w.replace('<cornsurfs>',modelblock.kenocornsurfs) for w in geomtemplate]

    if self.model == 'basic':
      geomtemplate = makechangeom(geomtemplate,self.apitch, self.wchan, self.tchan, self.ricorner, self.tcorner, self.wcutout)
    geomtemplate = offsetgeom(geomtemplate,self.offset)

    if self.seq == 'tnewt':
      f.write( constructmodel(geomtemplate,
                              sequence='t-newt',
                              tparms=self.tparms,
                              xslib=self.lib,
                              aliasblock=aliasblock.nodepltext,
                              compblock=compblock.compblocktext,
                              celldatablock=celldatablock.allcells,
                              depletionblock='',
                              burndatablock='',
                              branchblock='',
                              fuelpins=modelblock.allnewtpinstext,
                              fuelpinholes=modelblock.holetext,
                              otherpins=modelblock.otherpinstext,
                              otherpinholes=modelblock.otherpinholes,
                              cbunits=cbunitstext,
                              cbholes=cbholestext,
                              collapseblock=self.collapseblock,
                              homogblock=self.homogblock,
                              adfblock=self.adfblock,
                              transparmblock=newtparmblock,
                              matrepls=aliasblock.otheraliases,
                              newtmats=modelblock.newtmaterials,
                              zdims='',
                              globalgrid=getglobalgrid(self.pinpitch, self.latpitch, gridsperpin=self.gridsperpin),
                              jobinfo=self.info,
                              modelstart='read model \n' + self.info,
                              modelend='end model',
                              dancoffs='',
                              keno2dplot='',
                              shellcmdse=self.shellcmdse,
                              shellcmdsb=self.shellcmdsb ) )
    elif self.seq == 'tdepl':
      f.write( constructmodel(geomtemplate,
                              sequence='t-depl',
                              tparms=self.tparms,
                              xslib=self.lib,
                              aliasblock=aliasblock.depltext,
                              compblock=compblock.compblocktext,
                              celldatablock=celldatablock.allcells,
                              depletionblock=depletionblock,
                              burndatablock=burnupsteps.text,
                              branchblock='',
                              fuelpins=modelblock.allnewtpinstext,
                              fuelpinholes=modelblock.holetext,
                              otherpins=modelblock.otherpinstext,
                              otherpinholes=modelblock.otherpinholes,
                              cbunits=cbunitstext,
                              cbholes=cbholestext,
                              collapseblock=self.collapseblock,
                              homogblock=self.homogblock,
                              adfblock=self.adfblock,
                              transparmblock=newtparmblock,
                              matrepls=aliasblock.otheraliases,
                              newtmats=modelblock.newtmaterials,
                              zdims='',
                              globalgrid=getglobalgrid(self.pinpitch, self.latpitch, gridsperpin=self.gridsperpin),
                              jobinfo=self.info,
                              modelstart='read model \n' + self.info,
                              modelend='end model',
                              dancoffs='',
                              keno2dplot='',
                              shellcmdse=self.shellcmdse,
                              shellcmdsb=self.shellcmdsb ) )
    elif self.seq == 't6depl':
      f.write( constructmodel(geomtemplate,
                              sequence='t6-depl',
                              tparms=self.tparms,
                              xslib=self.lib,
                              aliasblock=aliasblock.depltext,
                              compblock=compblock.compblocktext,
                              celldatablock=celldatablock.allcells,
                              depletionblock=depletionblock,
                              burndatablock=burnupsteps.text,
                              branchblock='',
                              fuelpins=modelblock.allk6pinstext,
                              fuelpinholes=modelblock.holetext,
                              otherpins=modelblock.otherpinstext,
                              otherpinholes=modelblock.otherpinholes,
                              cbunits=cbunitstext,
                              cbholes=cbholestext,
                              collapseblock='',
                              homogblock='',
                              adfblock='',
                              transparmblock=kenoparmblock,
                              matrepls=aliasblock.otheraliases,
                              newtmats='',
                              zdims='{0} {1}'.format(self.zlen,0.0),
                              globalgrid='',
                              jobinfo=self.info,
                              modelstart='read model \n',
                              modelend='end data',
                              dancoffs='',
                              keno2dplot='',
                              shellcmdse=self.shellcmdse,
                              shellcmdsb=self.shellcmdsb ) )
    elif self.seq == 'csas6':
      f.write( constructmodel(geomtemplate,
                              sequence='csas6',
                              tparms=self.tparms,
                              xslib=self.lib,
                              aliasblock='',
                              compblock=compblock.compblocktext,
                              celldatablock=celldatablock.allcells,
                              depletionblock='',
                              burndatablock='',
                              branchblock='',
                              fuelpins=modelblock.allk6pinstext,
                              fuelpinholes=modelblock.holetext,
                              otherpins=modelblock.otherpinstext,
                              otherpinholes=modelblock.otherpinholes,
                              cbunits=cbunitstext,
                              cbholes=cbholestext,
                              collapseblock='',
                              homogblock='',
                              adfblock='',
                              transparmblock=kenoparmblock,
                              matrepls=aliasblock.otheraliases,
                              newtmats='',
                              zdims='{0} {1}'.format(self.zlen,0.0),
                              globalgrid='',
                              jobinfo=self.info,
                              modelstart='',
                              dancoffs='',
                              keno2dplot=getkeno2dplot(self.latpitch,self.zlen),
                              modelend='end data',
                              shellcmdse=self.shellcmdse,
                              shellcmdsb=self.shellcmdsb ) )
    elif self.seq == 'mcd':
      f.write( constructmodel(geomtemplate,
                              sequence='mcdancoff',
                              tparms=self.tparms,
                              xslib=self.lib,
                              aliasblock='',
                              compblock=compblock.compblocktext,
                              celldatablock=celldatablock.allcells,
                              depletionblock='',
                              burndatablock='',
                              branchblock='',
                              fuelpins=modelblock.allk6pinstext,
                              fuelpinholes=modelblock.holetext,
                              otherpins=modelblock.otherpinstext,
                              otherpinholes=modelblock.otherpinholes,
                              cbunits=cbunitstext,
                              cbholes=cbholestext,
                              collapseblock='',
                              homogblock='',
                              adfblock='',
                              transparmblock=getmcdparmblock(),
                              matrepls=aliasblock.otheraliases,
                              newtmats='',
                              zdims='{0} {1}'.format(self.zlen,0.0),
                              globalgrid='',
                              jobinfo=self.info,
                              modelstart='',
                              modelend='end data',
                              keno2dplot=getkeno2dplot(self.latpitch,self.zlen),
                              dancoffs=getdancofftext(modelblock.holetext),
                              shellcmdse=self.shellcmdse,
                              shellcmdsb=self.shellcmdsb ) )

    f.close()
    print "  Done..."

