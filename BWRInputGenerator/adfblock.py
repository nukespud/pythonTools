# adfblock.py

def getadfblock(homogid,aspitch):
  adfblocktext = 'read adf\n'
  adfblocktext += ' 1 {0} n={1} s=-{1} e={1} w=-{1}\n'.format(homogid,aspitch/2)
  adfblocktext += 'end adf\n'
  return adfblocktext