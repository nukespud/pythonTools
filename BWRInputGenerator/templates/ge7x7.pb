=<sequence> <tparms>
<jobinfo>
<xslib>
' Brian J. Ade - updated 2/3/2010
' Data taken from:
'    [1] Core Design and Operating Data for Cycles 1 and 2
'        of Peach Bottom 2, N. H. Larson, Electric Power
'        Research Institute.
'    [2] B.J. Ade, FuelTemp.nb - Mathematica notebook for
'        fuel temperature estimates based on moderator
'        temperature.
'    [3] N.E. Todreas and M.S. Kazimi, Nuclear Systems I -
'        Thermal Hydraulic Fundamentals, Taylor and Francis
'        Group, New York, 1990.
'    [4] Y.A. Cengel and M.A. Boles, Thermodynamics -
'        An Engineering Approch, Steam Tables, McGraw Hill,
'        New York, 2006.
'------------------DEFINE ALIAS--------------------------
' Assembly Layout
'              11  12  13  14  15  16  17
'                  22  23  24  25  26  27
'                      33  34  35  36  37
'                          44  45  46  47
'                              55  56  57
'                                  66  67
'                                      77
<aliasblock>
<compblock>
<celldatablock>
<depletionblock>
<burndatablock>
<branchblock>


'------------DEFINE NEWT MODEL--------------------

read model
<jobinfo>
<newtparmblock>
<newtmats>

read geom

<fuelpins>

' Channel corners
' Channel corners placed in geometry by using a hole.
' Thickness:  0.2032 cm   from 0.080" in Table 1 of [1] - same as channel
' Radius:     0.9652 cm   from 0.380" in Table 1 of [1]
' Northeast Corner
  unit   80
    cylinder 5   0.9652   chord +x=0.0    chord +y=0.0
    cylinder 6   1.1684   chord +x=0.0    chord +y=0.0
    cuboid   7   1.2 0.0  1.2 0.0
    media <mod> 1 5
    media <can> 1 6 -5
    media <mod1> 1 7 -6
    boundary    7  2 2

' Global unit
' Channel
' Thickness:       0.2032 cm   from 0.080" in Table 1 of [1] - same as channel
' Assembly Pitch: 15.24 cm     from control blade pitch, Table 11, 12.0" [1]
' Rounded channel corners, partial pins with the corners, and control blades
'   are placed using holes.
global unit 100
  cuboid  1   6.70306 <pos> -6.70306 <pos>  6.70306 <mos> -6.70306 <mos>
  cuboid  2   6.90626 <pos> -6.90626 <pos>  6.90626 <mos> -6.90626 <mos>
  cuboid  10  4p7.62
  hole 80  origin x=  5.73786 <pos> y=  5.73786 <mos>
  hole 80  origin x= -5.73786 <pos> y=  5.73786 <mos>  rotate a1= 90
  hole 80  origin x= -5.73786 <pos> y= -5.73786 <mos>  rotate a1=180
  hole 80  origin x=  5.73786 <pos> y= -5.73786 <mos>  rotate a1=270
<fuelpinholes>
  media   <mod> 1 1
  media   <can> 1 2 -1
  media   <mod1> 1 10 -2
  boundary 10 <globalgrid>
end geom
' ---------ARRAYS--------
' --------BOUNDARY CONDITIONS--------
read bounds
   all=refl
end bounds

<collapseblock>
<homogblock>
<adfblock>

end model
end

