#!/usr/bin/env python
#
#
#     Code: DensityConvert
#
#     Author:  Joshua Peterson
#
#     Date:    April 25, 2016
#
#     Description:  Used to convert atomic density to mass density ect.
#
########################################
__author__ = 'f4p'


from pyne.material import Material
import sys
sys.path.insert(0, r'~/projects/pythonTools/PyneTools')

from PyneTools import PyneModules


#==================   User input=====================
heu_atom= Material({'U234': 4.18E-4, 'U235': 4.50E-2, 92238 : 2.50E-3},
                   4.79E-2,
                   metadata={'materialNumber': 1,
                             'materialName':"wtptHEU"})




heu=PyneModules.AtomicDensityToMassDensity(heu_atom)
#PyneModules.ScaleMaterialWriter(heu)



PyneModules.MC2_3MaterialWriter(heu_atom)