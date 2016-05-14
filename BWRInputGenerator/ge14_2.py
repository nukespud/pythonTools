from bwrtemplates import *

mplus = ge14

mplus.jobinfo('Test Template Model, GE14')
mplus.hlopts(sequence='csas6',fname='ge14.kenoce.inp',lib='cev7',parms='')
mplus.state(tfu=950,tmo=540,vf=0.80)
mplus.options(gdrings=5,gridsperpin=4,fluxplots='yes',dfdetail='no')
mplus.cb(type='basic',cst=0.1)
mplus.offset = 0.25

mplus.uo2('f1', den=10.40, enr=2.4)
mplus.uo2('f2', den=10.40, enr=2.8)
mplus.uo2('f3', den=10.40, enr=3.2)
mplus.uo2('f4', den=10.40, enr=3.6)
mplus.uo2('f5', den=10.40, enr=3.95)
mplus.uo2('f6', den=10.40, enr=4.4)
mplus.uo2('f7', den=10.40, enr=4.9)

mplus.uo2gd('f8',  den=10.40, enr=4.4, gd=7)
mplus.uo2gd('f9',  den=10.40, enr=4.4, gd=8)
mplus.uo2gd('f10', den=10.40, enr=4.9, gd=7)

mplus.pindims=[0.43815,0.44704,0.51308]

mplus.fuelpin(1,  mplus.pindims,['f1','gap','clad'])
mplus.fuelpin(2,  mplus.pindims,['f2','gap','clad'])
mplus.fuelpin(3,  mplus.pindims,['f3','gap','clad'])
mplus.fuelpin(4,  mplus.pindims,['f4','gap','clad'])
mplus.fuelpin(5,  mplus.pindims,['f5','gap','clad'])
mplus.fuelpin(6,  mplus.pindims,['f6','gap','clad'])
mplus.fuelpin(7,  mplus.pindims,['f7','gap','clad'])
mplus.fuelpin(8,  mplus.pindims,['f8','gap','clad'])
mplus.fuelpin(9,  mplus.pindims,['f9','gap','clad'])
mplus.fuelpin(10, mplus.pindims,['f10','gap','clad'])

mplus.wr('W1',[1.16840,1.24460],['mod1','can'],[-mplus.pinpitch,-mplus.pinpitch])
mplus.wr('W2',[1.16840,1.24460],['mod1','can'],[mplus.pinpitch,mplus.pinpitch])

mplus.lattice("""1
				 3  6
				 5  6 10
				 6  7  7  7
				 6  7 10  7  7
				 6  7  7  0  0  7
				 6  7  8  0  0  7 10
				 6  6  7  7 10  7  7  7
				 4  6  8  7  7 10  7  9  7
				 2  4  6  7  7  7  7  6  4  2""")

mplus.burnups()
mplus.gen2gdata()

mplus.end()

