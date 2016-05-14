# depletionblock.py

def makefueldicts(fuels):
  fueldict = {}
  gdfueldict = {}
  for fuel in fuels:
    if fuel[0].strip().find('gd') == -1:
      fueldict[fuel[0].strip()] = fuel[1:]
    else:
      gdfueldict[fuel[0].strip()] = fuel[1:]
  return fueldict, gdfueldict

def newmakefueldicts(fuels):
#  print fuels
#  print
  fueldict = {}
  gdfueldict = {}
  for fuel in fuels:
    if fuel[1] <= 1:
      fueldict[fuel[0].strip()] = fuel[2:]
    else:
      gdfueldict[fuel[0].strip()] = fuel[2:]
  return fueldict, gdfueldict

def depletionblocktext(pins,mats, onefuels,allfuels,gdrings):
  newonefuels = []
  newallfuels = []
  for key in pins:
    newonefuels.append(['$1f'+pins[key]['mats'][0], pins[key]['flrings']] + mats[pins[key]['mats'][0]]['1flnums'])
    newallfuels.append(['$f'+pins[key]['mats'][0], pins[key]['flrings']] + mats[pins[key]['mats'][0]]['flnums'])
  onefueldict, onegdfueldict = newmakefueldicts(newonefuels)
  allfueldict, allgdfueldict = newmakefueldicts(newallfuels)
  deplblock = 'read depletion '
  for key in allfueldict: deplblock += '\n  {0} '.format(key)
  deplblock += '\n flux '
  for key in allgdfueldict: deplblock += '\n  {0} '.format(key)
  deplblock += '  end \n'
  for key in onefueldict: deplblock += '    assign {0}  {1}  end \n'.format(key, key.replace('$1','$'))
  for key in allgdfueldict:
    numgdfuels = len(allgdfueldict[key])/gdrings
    for i in range(0,gdrings):
      deplblock += '    assign {0}'.format(onegdfueldict[key.replace('$','$1')][i])
      for j in range(i, len(allgdfueldict[key])+i, gdrings):
        deplblock += ' {0} '.format(allgdfueldict[key][j])
      deplblock += ' end \n'
  deplblock += 'end depletion '
  return deplblock
