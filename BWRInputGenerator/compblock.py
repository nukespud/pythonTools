# compblock.py

def listtodict(a):
  adict = {}
  for part in a:
    thiskey = part[0].replace(' ','')
    adict[thiskey] = part[1:]
  return adict


class compblockclass:
  "This is the composition block class"
  def __init__(self,mats,seq=None):
    if seq == 'tnewt' or seq == 'tdepl':
      self.compblocktext = 'read comp\n'
      keys = mats.keys()
      keys.sort()
      for key in keys :
        self.compblocktext += '  ' + mats[key]['mattext']
      self.compblocktext += 'end comp\n'
    else:
      self.compblocktext = 'read comp\n'
      keys = mats.keys()
      keys.sort()
      for key in keys:
        if mats[key]['type'] == 'fuel':
          for mixnum in mats[key]['1flnums']:
            self.compblocktext += '  ' + mats[key]['mattext'].replace('$1f'+key,str(mixnum))
        else:
          for mixnum in mats[key]['matnums']:
            self.compblocktext += '  ' + mats[key]['mattext'].replace('$'+key,str(mixnum))
      self.compblocktext += 'end comp\n'

