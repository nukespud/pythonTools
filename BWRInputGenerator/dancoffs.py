# dancoffs.py

def getdancofftext(fuelpinholes):
  dancofftext = 'read start \n'
  fuelpinholes = fuelpinholes.split('\n')
  for i in range(0,len(fuelpinholes)):
    if len(fuelpinholes[i]) != 0:
      dancofftext += '  dancoff hole {0} unit {1} region 1 \n'.format(i+1,fuelpinholes[i].split()[1])
  dancofftext += 'end start \n'
  return dancofftext

