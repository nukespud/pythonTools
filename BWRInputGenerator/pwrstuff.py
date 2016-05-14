i2cm = 2.54

from bwr import *
lwr = BWR(sequence='tdepl',model='basic',name='testpwr.inp', parms='check,weight')
lwr.jobinfo('this is junk')
lwr.state(tfu=950,tmo=540,vf=0.40)
lwr.pitch(pinpitch=1.26,latpitch=6.0*i2cm,offset=0.187*i2cm*0.5)
lwr.channel(apitch=6.0*i2cm, wchan=5.278*i2cm, tchan=0.08*i2cm, ricorner=0.38*i2cm, tcorner=0.08*i2cm)
lwr.options(gdrings=5,gridsperpin=5,fluxplots='yes')

lwr.uo2('f1', den=10.42, enr=2.79)
lwr.uo2('f2', den=10.42, enr=1.94)
lwr.uo2('f3', den=10.42, enr=1.5)

lwr.zirc2('clad')
lwr.zirc2('can', type='struct')
lwr.h2o('mod',type='mod')
lwr.h2o('mod1',type='cool')
lwr.he('gap')

pindims=[0.4096, 0.418, 0.475]

lwr.fuelpin(1,  pindims,['f1','gap','clad'])
lwr.fuelpin(2,  pindims,['f2','gap','clad'])
lwr.fuelpin(3,  pindims,['f3','gap','clad'])

lwr.lattice("""1
               1 1
               1 1 1
               1 1 1 2
               1 1 1 1 1
               1 1 2 1 1 2
               1 1 1 1 1 1 1
               1 1 1 1 1 1 1 1
               1 1 2 1 1 2 1 1 3""")

lwr.burnups()

lwr.end()


