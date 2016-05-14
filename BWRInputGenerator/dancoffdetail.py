# dancoffdetail.py
 
print "CPILE2 does not have numpy" 
#from numpy import polyfit

def newfromold(dict):
  newdict = {}
  for key in dict:
    newdict[key] = dict[key]
  return newdict

def getdfs(dfdict, rhomod):
  latlen = len(dfdict[dfdict.keys()[0]])
  thesedfs = []
  order = 2
  for i in range(0,latlen):
    df = 0 
    raw_input( "ERROR coeffs cant work because cpile does not have numpy")
    
    #coeffs = polyfit(dfdict.keys(), [dfdict[key][i] for key in dfdict.keys()],order)
    keytest = [dfdict[key][i] for key in dfdict.keys()]
    if keytest[0] != 0 and keytest[0] != 1:
      for j in range(0,order+1):
        df += coeffs[order-j]*rhomod**float(j)
    else:
      df = 0.0
    thesedfs.append(df)
  return thesedfs

def revlist(list):
  if len(list) == 0:
    print "revlist: list is empty"
    return
  elif len(list) == 1:
    return list
  else:
	reversedlist = [list[i] for i in range(len(list)-1,-1,-1)]
	return reversedlist

def indexdict(array):
  dict = {}
  for i in range(0,len(array)):
    if array[i] in dict:
      dict[array[i]].append(i)
    else:
      dict[array[i]] = [i]
  return dict


def normdfs(unnormeddfs, counts):
  normeddfs = [0 for i in range(0,len(unnormeddfs)) ]
  for i in range(0,len(unnormeddfs)):
    if len(counts[i]) != 0: normeddfs[i] = unnormeddfs[i]/float(len(counts[i]))
  return normeddfs

def whichbin(bins,df):
  for i in range(0,len(bins)):
    if bins[i] < df and df < bins[i+1]:
      return i
      break

def bindfs(bins,dfs):
  binindices = [[] for i in range(0,len(bins))]
  for i in range(0,len(dfs)):
    if dfs[i] != 0 and dfs[i] != 1:
      binindices[whichbin(bins,dfs[i])].append(i)
  return binindices

def avelist(list):
  total = 0
  for i in range(0,len(list)):
    total += list[i]
  total = total/float(len(list))
  return total

def dict2list(dict):
  list = []
  for key in dict:
    list.append([key,dict[key]])
  return list

def list2dict(list):
  dict = {}
  for i in range(0,len(list)):
    dict[list[i][0]] = list[i][1:]
  return dict


class dancoffdetailclass:
  def __init__(self, fuellat, dfdict, rhomod, fuelpins, mats):
    topkey = max(fuelpins.keys())

    newfuellat = [i for i in fuellat]

    newpinnums = max(fuellat)

    dfs = getdfs(dfdict, rhomod)

    for key in fuelpins:
      fuelpins[key]['dfs'] = [ dfs[index] for index in fuelpins[key]['listindicies']]
    detaillevel = 10
    pinstoadd = {}
    matstoadd = {}

    for key in fuelpins:
      bins = [i/float(detaillevel) for i in range(0,detaillevel + 1)]
      counts = [[] for i in range(0,detaillevel)]
      counter = 0
      pops = []
      binnedindices = bindfs(bins, fuelpins[key]['dfs'])
      for indices in binnedindices:
        if len(indices) != 0:
          if counter > 0:
            topkey += 1
            pinstoadd[topkey] = dict(fuelpins[key])
            pinstoadd[topkey]['df'] = avelist([fuelpins[key]['dfs'][index] for index in indices])
            pinstoadd[topkey]['dfs'] = [fuelpins[key]['dfs'][index] for index in indices]
            pinstoadd[topkey]['listindicies'] = [fuelpins[key]['listindicies'][index] for index in indices]
            pinstoadd[topkey]['latindices'] = [fuelpins[key]['latindices'][index] for index in indices]
            newmats = ['{0}d{1}'.format(fuelpins[key]['mats'][0],counter)] + fuelpins[key]['mats'][1:]
            pinstoadd[topkey]['mats'] = newmats
            matstoadd[newmats[0]] = dict(mats[fuelpins[key]['mats'][0]])
            matstoadd[newmats[0]]['mattext'] = mats[fuelpins[key]['mats'][0]]['mattext'].replace(fuelpins[key]['mats'][0] + ' ',newmats[0]+' ')
            for index in indices:
              newfuellat[fuelpins[key]['listindicies'][index]] = topkey
            pops += indices
            counter += 1
          elif counter == 0:
            fuelpins[key]['df'] = avelist([fuelpins[key]['dfs'][index] for index in indices])
            counter += 1
      if len(pops) !=0:
        pops.sort()
        for i in revlist(pops):
          fuelpins[key]['dfs'].pop(i)
          fuelpins[key]['listindicies'].pop(i)
          fuelpins[key]['latindices'].pop(i)
    for key in pinstoadd:
      fuelpins[key] = pinstoadd[key]
    for key in matstoadd:
      mats[key] = matstoadd[key]
#    print newfuellat
    self.fuellat = newfuellat
