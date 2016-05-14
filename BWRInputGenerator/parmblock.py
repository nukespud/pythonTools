# newtparmblock.py

def getnewtparmblock(echo='yes',
                     drawit='yes',
                     solntype='b1',
                     combine='no',
                     prtflux='no',
                     cmfd=1,
                     xycmfd=4,
                     collapse='no',
                     epseigen=1e-5,
                     epsinner=1e-5,
                     epsouter=1e-5,
                     converg='mix',
                     timed='yes',
                     prtmxtab='no'):
  dictkeys = locals().keys()
  dict = locals()
  dictkeys.sort()
  newtparmblocktext = 'read parm \n'
  for key in dictkeys:
    newtparmblocktext += '  {0}={1} \n'.format(key,str(dict[key]))
  newtparmblocktext += 'end parm\n'
  return newtparmblocktext

def getkenoparmblock(gen=500,
                     npg=10000,
                     tba=100,
                     htm='no',
                     flx='yes',
                     fdn='yes',
                     run='yes'):
  dictkeys = locals().keys()
  dict = locals()
  dictkeys.sort()
  kenoparmblocktext = 'read parm \n'
  for key in dictkeys:
    kenoparmblocktext += '  {0}={1} \n'.format(key,str(dict[key]))
  kenoparmblocktext += 'end parm\n'
  return kenoparmblocktext

def getmcdparmblock(gen=100,
                     npg=100,
                     htm='no',
                     flx='yes',
                     fdn='yes',
                     run='yes'):
  dictkeys = locals().keys()
  dict = locals()
  dictkeys.sort()
  mcdparmblocktext = 'read parm \n'
  for key in dictkeys:
    mcdparmblocktext += '  {0}={1} \n'.format(key,str(dict[key]))
  mcdparmblocktext += 'end parm\n'
  return mcdparmblocktext
