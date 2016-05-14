# BWR templates built from the basic template
from bwr import *


<<<<<<< local
=======
Parameter='addnux=2,weight'
# Plot flux     
Fluxplots='yes' 
# Maximum Burnup
Max_burnup=71   
>>>>>>> other

<<<<<<< local
#  Inital pramaeters for all the codes
Parameter='addnux=2,weight'
# Plot flux
Fluxplots='yes'
# Maximum Burnup
Max_burnup=71
=======
>>>>>>> other


<<<<<<< local
=======
def bwr_23_7x7(enrichment,void):
     # File name to be saved
    FILE_NAME='bwr7x7_2_3'
    # Information abou the job
    JobInfo='BWR 7x7 Ge2b ARP generation Ref   '
     
    # Fuel rod data
    # Density of fuel in g/cc
    Density_Fuel=9.73 
    # Temperateru of Fuel in C 
    Temp_Fuel=811
    # Pelllet Outside radius in cm
    Pellet_OR=1.237/2 
    ##  Calculated Gap outside radius in cm
    Gap_OR=   1.26744/2 
    #
    #
    Gap_den= 0.0001
    ## Cladding outside radius in cm
    Clad_OR=1.43/2 
    # Clad Density
    Clad_den=6.56
    
    
    
    
    # Assemblyh data
    # Moderator temperate (C) 
    Temp_moderator=558
    # Pin Pitch in cm
    Pinpitch=1.875
    #Latice pitch in cm
    Latpitch=15.24
    #
    apitch=Latpitch
    # Assembly channel inner dimension (cm)
    Waterchanel=12.9996
    # Assembly channel thickness
    Tchanel=0.2032
    # Radius of the corners
    Ricorner= 0.9652
    # Corner thickness
    Tcorner=0.2032
    #
    # Cladding walls
    Wall_den=Clad_den
    # Cladding wall temp
    Wall_temp=Temp_moderator
    
    
    # Gd rod information
    # Gad rod information
    # Number of Gd rings
    Gdrings=5
    # Gad grids per each pin
    Gridsperpin=5
    # Enrichment of Gad 2
    Gad_enrich2=4.0
    # Enrichmet of Gad 3
    Gad_enrich3=3.0
    
>>>>>>> other

<<<<<<< local
#  This is a Fuel assembly class for use with Brian's libaraiy.  The goal is to not to repeat to many lines of code
class Fuel_assembly:
    def __init__(self):
        self.File_name         =''
        self.Parameter         =''
        self.Temp_Fuel         =0.0
        self.Temp_moderator    =0.0
        self.void              =0.0
        self.Pinpitch          =0.0
        self.Latpitch          =0.0
        self.apitch            =0.0
        self.Waterchanel       =0.0
        self.Tchanel           =0.0
        self.Ricorner          =0.0
        self.Tcorner           =0.0
        #  Number of Gad ring
        self.Gdrings           =5
        # Grids per pin
        self.Gridsperpin       =5
        #
        self.Fluxplots         =0.0
        self.Clad_den          =0.0
        self.Wall_den          =0.0
        self.Wall_temp         =0.0
        self.Gap_den           =0.0
        self.Pellet_OR         =0.0
        self.Gap_OR            =0.0
        self.Clad_OR           =0.0
        self.Density_Fuel      =0.0
        self.enrichment        =0.0
        self.Gad_enrich2       =0.0
        self.Gad_enrich3       =0.0
        self.Max_burnup        =0.0
        self.Water_Rod_OR      =0.0
        self.Water_Rod_IR      =0.0
        self.Water_Rod_Loc_1   =0.0
        self.Water_Rod_Loc_2   =0.0
        self.Water_Rod_Loc_3   =0.0
        self.Water_Rod_Loc_4   =0.0
        self.Water_Rod_Loc_5   =0.0
        self.Water_Rod_Loc_6   =0.0
        self.Num_Water_Rods    =0





#  This runs Bryans script for creating BWR libraries.
def Set_lwr(FA):

=======
    
    #  True and False Statements 
    # If you want to exicute the scale script 
    EXECUTE=True
    #  This moves the output to the correct location for future analysis
    POST_PROCESS=False
    # If you want to generate an arplib txt file.  
    PRINT_ARPLIB=False
 
     
>>>>>>> other
    lwr=0
    # Name of the file
<<<<<<< local
    FA.File_name='%s_%s_enrich_%s_void'%(FA.FILE_NAME,FA.enrichment,FA.void)
=======
    File_name='%s_%s_enrich_%s_void'%(FILE_NAME,enrichment,void)
>>>>>>> other
    #  Intializig the pointer lwr to the object BWR
<<<<<<< local
    lwr = BWR(sequence='tdepl',model='basic',fname='%s.inp'%(FA.File_name), parms=FA.Parameter)
=======
    lwr = BWR(sequence='tdepl',model='basic',fname='%s.inp'%(File_name), parms=Parameter)
>>>>>>> other
    # seting the jobinformation for LWR
<<<<<<< local
    lwr.jobinfo(FA.JobInfo)

    # Setting the state of the problem.
=======
    lwr.jobinfo(JobInfo)
    
    # Setting the state of the problem.  
>>>>>>> other
    #   tfu=temparture of the fuel
    #   tmo=temperature of the moderator
    #   vf=void fraction
<<<<<<< local
    lwr.state(tfu=FA.Temp_Fuel,tmo=FA.Temp_moderator,vf=FA.void)

=======
    lwr.state(tfu=Temp_Fuel,tmo=Temp_moderator,vf=void)
    
>>>>>>> other
    # lwr.pitch(pinpitch=0.738*i2cm,latpitch=6.0*i2cm,offset=0.187*i2cm*0.5)
    #  pinpitch= Pin Pitch
    #  latpitch= Lattice Pitch
<<<<<<< local
    #  Offset=?
    lwr.pitch(pinpitch=FA.Pinpitch,latpitch=FA.Latpitch,offset=0.0)

=======
    #  Offset=? 
    lwr.pitch(pinpitch=Pinpitch,latpitch=Latpitch,offset=0.0)
    
>>>>>>> other
    # Apitch=?
<<<<<<< local
    # Wchan=?
=======
    # Wchan=? 
>>>>>>> other
    # TChan=?
    # RiCorner=?
    # Tcorner=?
<<<<<<< local
    lwr.channel(apitch=FA.apitch, wchan=FA.Waterchanel, tchan=FA.Tchanel, ricorner=FA.Ricorner, tcorner=FA.Tcorner)

=======
    lwr.channel(apitch=apitch, wchan=Waterchanel, tchan=Tchanel, ricorner=Ricorner, tcorner=Tcorner)
    
>>>>>>> other
    # GdRings= Number of Gad rings
    # Gridsperpin= Number of grids needed per pin
    # FluxPlots=?
<<<<<<< local
    lwr.options(gdrings=FA.Gdrings,gridsperpin=FA.Gridsperpin,fluxplots=FA.Fluxplots),

=======
    lwr.options(gdrings=Gdrings,gridsperpin=Gridsperpin,fluxplots=Fluxplots),    
    
>>>>>>> other
    #  Cladding (replace in generic model the word clad)
    # Temp is the temp of the self.tfu*0.2 + self.tmo*0.8
<<<<<<< local
    lwr.zirc2('clad', den=FA.Clad_den,type='clad')

=======
    lwr.zirc2('clad', den=Clad_den,type='clad')
    
>>>>>>> other
    #  Zirc4 instead of Zirc 2  Cladding for the structure
<<<<<<< local
    lwr.zirc4('can', den=FA.Wall_den, type='struct')

=======
    lwr.zirc4('can', den=Wall_den, type='struct')
    
>>>>>>> other
    #  He is the gap
<<<<<<< local
    lwr.he('gap',den=FA.Gap_den, type='gap')

=======
    lwr.he('gap',den=Gap_den, type='gap')
    
>>>>>>> other
    #  The water is called mod
    lwr.h2o('mod',type='mod')
<<<<<<< local

=======
    
>>>>>>> other
    # The strucutre water is called mod1
<<<<<<< local
    lwr.h2o('mod1')

=======
    lwr.h2o('mod1,tmp=Temp_moderator')
    
>>>>>>> other
    #  Pin dimiesions
    # Pell, Gap, Cladding
    # Cladding thickness 0.81 mm World Nuclear Report
<<<<<<< local
    pindims=[FA.Pellet_OR, FA.Gap_OR ,FA.Clad_OR]
=======
    pindims=[Pellet_OR, Gap_OR ,Clad_OR]
>>>>>>> other
    # F1 material def
<<<<<<< local
    lwr.uo2('f1', den=FA.Density_Fuel, enr=FA.enrichment)
=======
    lwr.uo2('f1', den=Density_Fuel, enr=enrichment)
>>>>>>> other
    lwr.fuelpin(1,  pindims,['f1','gap','clad'])
<<<<<<< local

    if FA.Gad_enrich2>0:
        #  Gad material, with density, enrichment of fuel, and wt% of gd
        lwr.uo2gd('Gad_enrich2%s'%(FA.Gad_enrich2), den=FA.Density_Fuel, enr=FA.enrichment,gd=FA.Gad_enrich2)
        # Assigning pin 5 two be gad pin
        lwr.fuelpin(2,  pindims,['Gad_enrich2%s'%(FA.Gad_enrich2),'gap','clad'])

    if FA.Gad_enrich3>0:
        #  Gad material, with density, enrichment of fuel, and wt% of gd
        lwr.uo2gd('Gad_enrich3%s'%(FA.Gad_enrich3), den=FA.Density_Fuel, enr=FA.enrichment,gd=FA.Gad_enrich3)
        # Assigning pin 5 two be gad pin
        lwr.fuelpin(3,  pindims,['Gad_enrich3%s'%(FA.Gad_enrich3),'gap','clad'])

    # If using water Rods:
    if FA.Num_Water_Rods>0:
        # The strucutre water is called mod1
        lwr.h2o('water_rod')
        water_dims=[FA.Water_Rod_IR,FA.Water_Rod_OR]
        for i in range(FA.Num_Water_Rods):

            if i==1:
                lwr.wr('W1',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_1)
            if i==2:
                lwr.wr('W2',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_2)
            if i==3:
                lwr.wr('W3',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_3)
            if i==4:
                lwr.wr('W4',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_4)
            if i==5:
                lwr.wr('W5',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_5)
            if i==6:
                lwr.wr('W6',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_6)


    lwr.burnups(max=Max_burnup)
=======
>>>>>>> other
    
    
<<<<<<< local
=======
    #  Gad material, with density, enrichment of fuel, and wt% of gd
    lwr.uo2gd('f2', den=Density_Fuel, enr=enrichment,gd=Gad_enrich2)
    # Assigning pin 5 two be gad pin
    lwr.fuelpin(2,  pindims,['f2','gap','clad'])
>>>>>>> other
    
<<<<<<< local
def bwr_2_3_7x7(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
     # File name to be saved
    FA.FILE_NAME='bwr7x7_2_3'
    # Information abou the job
    FA.JobInfo='BWR 7x7 Ge2b ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=9.73
    # Temperateru of Fuel in C
    FA.Temp_Fuel=811
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.237/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.26744/2
    #
    #
    FA.Gap_den= 0.0001
    ## Cladding outside radius in cm
    FA.Clad_OR=1.43/2
    # Clad Density
    FA.Clad_den=6.56

    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=558
    # Pin Pitch in cm
    FA.Pinpitch=1.875
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch=FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=12.9996
    # Assembly channel thickness
    FA.Tchanel=0.2032
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=0.2032
    #
    # Cladding walls
    FA.Wall_den=FA.Clad_den
    # Cladding wall temp
    FA.Wall_temp=FA.Temp_moderator


    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=4.0
    # Enrichmet of Gad 3
    FA.Gad_enrich3=3.0


    #  Set information for fuel assembly
    lwr=Set_lwr(FA)



    lwr.lattice(""" 1
                    1  2
                    1  1  1
                    1  1  1  3
                    1  1  1  1  1
                    1  1  3  1  1  2
                    1  1  1  1  1  1  1""")


    return lwr,FA.File_name










def bwr_2_3_8x8(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void

    FA.FILE_NAME='bwr8x8_2_3'
    # Information abou the job
    FA.JobInfo='BWR 8x8 Ge9 ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=9.863
    # Temperateru of Fuel in C
    FA.Temp_Fuel=1128
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.057/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   1.064/2
    ## Cladding outside radius in cm
    Clad_OR=1.227/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=559.1
    # Pin Pitch in cm
    FA.Pinpitch=1.626
    #Latice pitch in cm
    FA.Latpitch=15.24
    # Assemply pitch
    FA.apitch=FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.0
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=0.2032



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=3.0
    # Enrichmet of Gad 3
    #Gad_enrich3=3.0

    FA.Num_Water_Rods=1
    # Water rod cladding outside radius
    FA.Water_Rod_OR=3.4036/2    # Gad rod information
    # Water Rod Inner radius
    FA.Water_Rod_IR=3.2004/2 #Water_Rod_OR-Water_Rod_thick
    # Water rod 1 location
    FA.Water_Rod_Loc_1=[0,0]
    # Water rod 2 location

    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

=======
    #  Gad material, with density, enrichment of fuel, and wt% of gd
    lwr.uo2gd('f3', den=Density_Fuel, enr=enrichment,gd=Gad_enrich3)
    # Assigning pin 5 two be gad pin
    lwr.fuelpin(3,  pindims,['f3','gap','clad'])
    
            
>>>>>>> other
    #Name of the file
    lwr.lattice(""" 1
<<<<<<< local
                    1  1
                    1  1  1
                    1  2  1  0
                    1  1  1  0  0
                    1  2  1  1  1  2
                    1  1  2  1  2  1  1
                    1  1  1  1  1  1  1  1""")

    return lwr,FA.File_name



def bwr_2_3_9x9(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void

    # File name to be saved
    FA.FILE_NAME='bwr9x9_2_3'
    # Information abou the job
    FA.JobInfo='BWR 9x9 Ge11 9x9 with 7 rods replaced with WR ARP generation   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel= 10.412
    # Temperateru of Fuel in C
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=0.955/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.0853/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.095/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=555.5
    # Pin Pitch in cm
    FA.Pinpitch=1.437
    #Latice pitch in cm
    FA.Latpitch=15.24
    # Assemply pitch
    FA.apitch=FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=12.93
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=0.2032



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=5.0
    # Enrichmet of Gad 3
    #Gad_enrich3=3.0


    # Water rod cladding outside radius
    # Number of water rods
    FA.Num_Wate_Rods=2
    FA.Water_Rod_OR=2.52/2
    # Water Rod Inner radius
    FA.Water_Rod_IR=2.32/2 #Water_Rod_OR-Water_Rod_thick
    # Water rod 1 location
    FA.Water_Rod_Loc_1=[-.892,-.892]
    # Water rod 2 location
    FA.Water_Rod_Loc_2=[.892, .892]
    # End of user input


    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    1  1  1
                    1  2  1  1
                    1  1  1  0  0
                    1  2  1  0  0  2
                    1  1  1  1  1  1  1
                    1  1  1  2  1  1  2  1
                    1  1  1  1  1  1  1  1  1""")

    return lwr,FA.File_name








def bwr_4_6_7x7(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void

    # File name to be saved
    FA.FILE_NAME='bwr7x7_4_6'
    # Information abou the job
    FA.JobInfo='BWR 7x7 Ge3b ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.32
    # Temperateru of Fuel in C
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.212/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   9.7344/2
    #
    #
    FA.Gap_den= 0.0001
    ## Cladding outside radius in cm
    FA.Clad_OR=1.43/2
    # Clad Density
    FA.Clad_den=6.56

    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=558
    # Pin Pitch in cm
    FA.Pinpitch=1.875
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch= FA.Latpitch
    # Assembly channel outder dimension (cm)
    FA.Waterchanel=13.5
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=0.2032

    # Cladding walls
    FA.Wall_den=6.56
    # Cladding wall temp
    FA.Wall_temp=FA.Temp_moderator

    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=4.0
    # Enrichmet of Gad 3
    FA.Gad_enrich3=3.0




    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    #Name of the  file
    lwr.lattice(""" 1
=======
>>>>>>> other
                    1  2
                    1  1  1
                    1  1  1  3
                    1  1  1  1  1
                    1  1  3  1  1  2
                    1  1  1  1  1  1  1""")
    lwr.burnups(max=Max_burnup)
<<<<<<< local
    return lwr,FA.File_name
=======
     
    return lwr,File_name
>>>>>>> other





<<<<<<< local
def bwr_4_6_8x8(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()
=======
>>>>>>> other

<<<<<<< local
    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
    # File name to be saved
    FA.FILE_NAME='bwr8x8_4_6'
    # Information abou the job
    FA.JobInfo='BWR 8x8 ANF-pressurized ARP generation Ref   '
=======
>>>>>>> other

<<<<<<< local
    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel= 10.32
    # Temperateru of Fuel in C
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.057/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=  9.7336/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.22936/2
=======
>>>>>>> other


<<<<<<< local
    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=552
    # Pin Pitch in cm
    FA.Pinpitch=1.62814
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.006
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=0.2032
=======
>>>>>>> other



<<<<<<< local
    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=4.0
    # Enrichmet of Gad 3
    FA.Gad_enrich3=3.0
=======
>>>>>>> other

<<<<<<< local
    #   # Water Rod Data
    FA.Water_Rod_thick=0.074
    # Water rod cladding outside radius
    FA.Water_Rod_OR=2.6187/2
    FA.Water_Rod_IR=FA.Water_Rod_OR-FA.Water_Rod_thick
    FA.Water_Rod_IR=2.4561/2
=======
>>>>>>> other

<<<<<<< local
=======
 
>>>>>>> other

<<<<<<< local
    #  Set information for fuel assembly
    lwr=Set_lwr(FA)
=======
>>>>>>> other

<<<<<<< local
    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    2  1  1
                    1  1  1  0
                    1  1  1  0  0
                    2  1  1  1  1  1
                    1  1  1  1  1  1  1
                    1  1  2  1  1  2  1  1""")
    lwr.burnups(max=Max_burnup)
    return lwr,FA.File_name
=======
>>>>>>> other



<<<<<<< local
=======
i2cm = 2.54
>>>>>>> other

<<<<<<< local
=======
hatch7x7 = BWR(sequence='tnewt',model='basic',fname='hatch7x7.inp', parms='check')
hatch7x7.jobinfo('Hatch C1-C3 Test Model')
hatch7x7.state(tfu=950,tmo=540,vf=0.40)
hatch7x7.pitch(pinpitch=0.738*i2cm,latpitch=6.0*i2cm,offset=0.187*i2cm*0.5)
hatch7x7.channel(apitch=6.0*i2cm, wchan=5.278*i2cm, tchan=0.08*i2cm, ricorner=0.38*i2cm, tcorner=0.08*i2cm)
hatch7x7.options(gdrings=5,gridsperpin=5,fluxplots='yes')
hatch7x7.dfs([[0.77293,''' 0.106
                           0.161  0.220
                           0.160  0.225  0.227
                           0.161  0.225  0.227  0.229
                           0.163  0.225  0.226  0.232  0.231
                           0.159  0.223  0.222  0.222  0.230  0.224
                           0.111  0.163  0.168  0.167  0.169  0.169  0.115 '''],
              [0.47441,''' 0.154
                           0.235  0.330
                           0.236  0.339  0.345
                           0.238  0.339  0.345  0.348
                           0.241  0.340  0.344  0.350  0.350
                           0.232  0.334  0.336  0.336  0.346  0.336
                           0.162  0.241  0.250  0.249  0.250  0.248  0.170 '''],
              [0.17589,''' 0.240
                           0.370  0.538
                           0.380  0.562  0.581
                           0.383  0.560  0.582  0.584
                           0.387  0.560  0.579  0.586  0.585
                           0.369  0.543  0.559  0.561  0.570  0.549
                           0.255  0.388  0.405  0.404  0.405  0.397  0.270 ''']])
>>>>>>> other


<<<<<<< local




def bwr_4_6_9x9(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
    # File name to be saved
    FA.FILE_NAME='bwr9x9_4_6'
    # Information abou the job
    FA.JobInfo='BWR 9x9 ANF-pressurized ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel= 10.32
    # Temperateru of Fuel in C
    FA.Temp_Fuel=900
    # Pelllet Outside radius in cm
    FA.Pellet_OR=0.95/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   10.1442
    ## Cladding outside radius in cm
    FA.Clad_OR=1.1/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=552
    # Pin Pitch in cm
    FA.Pinpitch=1.45288
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.006
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=0.2032



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=5.0
    # Enrichmet of Gad 3
    #Gad_enrich3=3.0

    # Plot flux
    FA.Fluxplots='yes'
    # Maximum Burnup
    FA.Max_burnup=71
      # Gad rod information
    # Number of Gd rings
    FA.Gdrings=5
    # Gad grids per each pin
    FA.Gridsperpin=5
  # Desired parameters
    FA.Parameter='addnux=2,weight'
    #Parameter='check'

    # Water Rod Data
    FA.Num_Water_Rods=5
    #  def wr(self,pinnum,dims,mats,xyloc=[0.0,0.0]):
    # NUMBER OF WATER rods

    # Water rod cladding thickness
    FA.Water_Rod_thick=0.08
    # Water rod cladding outside radius
    FA.Water_Rod_OR=1.445/2
    # Water Rod Inner radius
    FA.Water_Rod_IR=FA.Water_Rod_OR-FA.Water_Rod_thick
    # Water rod 1 location
    FA.Water_Rod_Loc_1=[0,0]
    # Water rod 2 location
    FA.Water_Rod_Loc_2=[FA.Pinpitch,0]
    # Water rod 2 location
    FA.Water_Rod_Loc_3=[0,-FA.Pinpitch]
    #
    FA.Water_Rod_Loc_4=[FA.Pinpitch*2,FA.Pinpitch]
    #
    FA.Water_Rod_Loc_5=[-FA.Pinpitch,-FA.Pinpitch*2]

    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    lwr.lattice(""" 1
                    1  2
                    1  1  2
                    1  1  1  1
                    1  1  1  1  0
                    1  1  1  1  0  1
                    1  1  1  0  1  1  1
                    1  2  1  1  1  1  2  1
                    1  1  1  1  1  1  1  1  1""")
    return lwr,FA.File_name




def bwr_4_6_10x10(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void




    # File name to be saved
    FA.FILE_NAME='bwr10x10_4_6'
    # Information abou the job
    FA.JobInfo='BWR 10x10 ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.144
    # Temperateru of Fuel in C
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=0.876/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   0.894/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.026/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=552
    # Pin Pitch in cm
    FA.Pinpitch=1.295
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.4176
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gad_enrich2=5.0
    # Enrichmet of Gad 3
    #Gad_enrich3=3.0

    # Plot flux
    FA.Fluxplots='yes'
    # Maximum Burnup
    FA.Max_burnup=71
      # Gad rod information
    # Number of Gd rings
    FA.Gdrings=5
    # Grids per each pin
    FA.Gridsperpin=5
  # Desired parameters
    FA.Parameter='addnux=2,weight'
    FA.Parameter='check'

    # Water Rod Data
    # Water Rod Data
    FA.Num_Water_Rods=2
    # Water rod cladding outside radius
    FA.Water_Rod_IR=1.161
    # Water Rod Inner radius
    FA.Water_Rod_OR=1.261
    # Water rod 1 location
    FA.Water_Rod_Loc_1=[FA.Pinpitch,FA.Pinpitch]
    # Water rod 2 location
    FA.Water_Rod_Loc_2=[-FA.Pinpitch,-FA.Pinpitch]


     #  Set information for fuel assembly
    lwr=Set_lwr(FA)


    lwr.lattice(""" 1
                    1  1
                    1  1  1
                    1  1  1  1
                    1  1  2  1  1
                    1  1  1  0  0  1
                    1  1  2  0  0  1  1
                    1  1  1  1  1  1  2  1
                    1  1  1  1  1  2  1  1  1
                    1  1  1  1  1  1  1  1  1  1""")

    return lwr,FA.File_name



def bwr_xdr06u_n(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void



    # File name to be saved
    FA.FILE_NAME='xdr06u-n'
    # Information abou the job
    FA.JobInfo='BWR 6x6 ARP generation Ref for XDR06U assembly type   '
     
    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.144
    # Temperateru of Fuel in C 
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.24/2 
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.26744/2 
    ## Cladding outside radius in cm
    FA.Clad_OR=1.43/2 
    # Assemblyh data
    # Moderator temperate (C) 
    FA.Temp_moderator=557.65
    # Pin Pitch in cm
    FA.Pinpitch=1.8796
    #Latice pitch in cm
    FA.Latpitch=13.6928
    #    # Grids per each     
    FA.Gridsperpin=5     

    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=11.4618
    # Assembly channel thickness
    FA.Tchanel=0.2   
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel
    

    lwr=Set_lwr(FA)    
                                        
    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    1  1  1
                    1  1  1  1
                    1  1  1  1  1
                    1  1  1  1  1  1""")
    
    return lwr,FA.File_name  
    
    
    
    
    
    
    
    
def bwr_xhb06g(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
    # File name to be saved
    FA.FILE_NAME='xhb06g'
    # Information abou the job
    FA.JobInfo='BWR 6x6 ARP generation Ref for XHB assembly type   '
     
    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.144
    # Temperateru of Fuel in C 
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.24/2 
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   1.26744/2 
    ## Cladding outside radius in cm
    FA.Clad_OR=1.43/2 
    
    
    # Assemblyh data
    # Moderator temperate (C) 
    FA.Temp_moderator=552
    # Pin Pitch in cm
    FA.Pinpitch=1.8769
    #Latice pitch in cm
    FA.Latpitch=13.6928
    # Grids per each 

    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel.4618
    # Assembly channel thickness
    FA.Tchanel=0.2   
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel
  
    lwr=Set_lwr(FA)       
            
    #Name of the file
    lwr.lattice(""" 1
                   1  1
                   1  1  1
                   1  1  1  1
           
    FA.Gridsperpin=5          1  1  1  1  1
                   1  1  1  1  1  1""")

    return lwr,FA.File_name  





=======
ge14 = BWR(sequence='tnewt',model='basic',fname='ge14.inp', parms='check')
ge14.jobinfo('GE14')
ge14.state(tfu=950,tmo=540,vf=0.40)
ge14.pitch(pinpitch=1.2954,latpitch=15.24)
ge14.options(gdrings=5,gridsperpin=4,fluxplots='yes')
ge14.channel(apitch=15.24, wchan=13.40612, tchan=0.1905, ricorner=0.87376, tcorner=0.3084, wcutout=0.6*13.40612)
ge14.dfs([[0.77293,''' 0.158
                       0.241  0.342
                       0.248  0.347  1.000
                       0.242  0.355  0.351  0.350
                       0.241  0.352  1.000  0.272  0.193
                       0.244  0.346  0.273  0.000  0.000  0.190
                       0.243  0.347  1.000  0.000  0.000  0.272  1.000
                       0.244  0.346  0.327  0.272  1.000  0.326  0.352  0.351
                       0.239  0.345  1.000  0.350  0.348  1.000  0.351  1.000  0.341
                       0.161  0.246  0.248  0.248  0.251  0.247  0.248  0.250  0.251  0.173''' ],
          [0.47441,''' 0.206
                       0.316  0.457
                       0.327  0.467  1.000
                       0.321  0.476  0.474  0.472
                       0.320  0.470  1.000  0.373  0.273
                       0.322  0.464  0.376  0.000  0.000  0.271
                       0.322  0.465  1.000  0.000  0.000  0.373  1.000
                       0.323  0.465  0.437  0.375  1.000  0.436  0.475  0.478
                       0.316  0.461  1.000  0.469  0.466  1.000  0.472  1.000  0.457
                       0.213  0.327  0.332  0.332  0.337  0.331  0.333  0.335  0.333  0.231''' ],
          [0.1774,'''  0.283
                       0.434  0.640
                       0.456  0.664  1.000
                       0.450  0.671  0.676  0.672
                       0.448  0.662  1.000  0.547  0.421
                       0.448  0.654  0.553  0.000  0.000  0.423
                       0.449  0.655  1.000  0.000  0.000  0.548  1.000
                       0.449  0.655  0.617  0.553  1.000  0.617  0.678  0.689
                       0.439  0.646  1.000  0.663  0.660  1.000  0.671  1.000  0.645
                       0.299  0.458  0.469  0.470  0.477  0.470  0.474  0.475  0.467  0.327''' ]])
>>>>>>> other
