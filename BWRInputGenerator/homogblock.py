# gethomogblock.py

def gethomogblock(homogid,mats,seq):
  homogmats = []
  for key in mats:
    if seq == 'tnewt':
      if '1flnums' in mats[key].keys(): homogmats += mats[key]['1flnums']
      else: homogmats += mats[key]['matnums']
    elif seq == 'tdepl':
      if 'flnums' in mats[key].keys(): homogmats += mats[key]['flnums']
      else: homogmats += mats[key]['matnums']
  homogmats.sort()
  homogblocktext = 'read homog \n'
  homogblocktext += '  {0}  hm{0} '.format(homogid)
  for i in range(0,len(homogmats)):
    if i != 0 and i%10 == 0: homogblocktext += ' {0} \n             '.format(homogmats[i])
    else: homogblocktext += ' {0} '.format(homogmats[i])
  homogblocktext += ' end\nend homog \n'
  return homogblocktext
