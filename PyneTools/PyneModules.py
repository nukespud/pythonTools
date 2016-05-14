

from pyne.material import Material
from pyne import nucname


def AtomicDensityToMassDensity(heu_atom):
    print "\n\n",heu_atom
    print "========heu_atom molecular mass ",heu_atom.molecular_mass()
    heu=Material()
    heu.from_atom_frac(heu_atom)
    print "\n\n",heu
    print "ERROR:  heu molecular mass is not correct heu.molecular_mass() = ", heu.molecular_mass()
    heu.metadata=heu_atom.metadata
    heu.metadata['density_g_per_cc']=heu.mass
    heu.normalize()
    return heu


#  Material:
#  mass = 11.265699488
#  density = -1.0
#  atoms per molecule = 0.0479
#  ---------------------------
#  U234   0.00868054127218
#  U235   0.938512847192
#  U238   0.0528066115354
#  ERROR:  heu molecular mass is not correct heu.molecular_mass() =  11.265699488
#  wtptHEU 1 11.265699488 3
#               92234  0.868054127218
#               92235  93.8512847192
#               92238  5.28066115354
#               1  300 end
def ScaleMaterialWriter(heu):
    print "{matName} {materialNum} {mass} {numIso}".format(matName=heu.metadata['materialName'],
                                    materialNum=heu.metadata['materialNumber'],
                                    mass=heu.metadata['density_g_per_cc'],
                                    numIso=len(heu))
    for iso in heu:
        print "             %s%s  %s"%(nucname.znum(iso),nucname.anum(iso), heu[iso]*100)
    print "             1  300 end"




#  \$material
#  i_externalspectrum(1)= 1      ! Spectrum file for composition: I_FUEL
#  t_composition(:, 1)=
#   U234_7    U234I     8.68054E-03   800.0
#   U235_7    U235I     9.38513E-01   800.0
#   U238_7    U238I     5.28066E-02   800.0
#  /
def MC2_3MaterialWriter(heu_atom):
    temperature=800.0
    print"\n\n"
    print"\$material"
    print"i_externalspectrum(1)= 1      ! Spectrum file for composition: I_FUEL"
    print "t_composition(:, 1)="
    for iso in heu_atom:
        # NA23_7    NA23I     8.04935E-03   740.5
        print " {iso}_7    {iso}I     {wt_pt:.5E}   {temp:.1f}".format(iso=nucname.name(iso), wt_pt=heu_atom[iso],temp=temperature)
    print "/"