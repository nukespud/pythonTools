# collapseblock.py

def getcollpaseblock(groupcollapse,tparms,xslib):
  collapseblock = 'read collapse \n'
  if groupcollapse == '2g':
    if tparms.find('weight') != -1:
      collapseblock += '  30r1 19r2 \n'
    else:
      if xslib.find('238') != -1:
        collapseblock += '  199r1 39r2 \n'
      elif xslib.find('44') != -1:
        collapseblock += '  25r1 19r2 \n'
  else:
    collapseblock += '  ' + groupcollapse + '\n'
  collapseblock += 'end collapse'
  return collapseblock