# constructmodel.py

def constructmodel(f, matrepls='', **kwargs):
  '''aliasblock='', compblock='', celldatablock='', depletionblock='', burndatablock='', branchblock='', fuelpins='', fuelpinholes='', collapseblock='', homogblock='', adfblock='', '''
  newfile = []
  for line in f:
    for key in kwargs:
      if line.find('<' + key + '>') != -1:
        line = line.replace('<' + key + '>',kwargs[key])
    for mat in matrepls:
      thiskey, thisrepl = mat[0].split()[0].replace('$',''), mat[1].split()[0]
      if line.find('<' + thiskey + '>') != -1:
        line = line.replace('<' + thiskey + '>',thisrepl)
    newfile.append(line)
  return ''.join(newfile)

