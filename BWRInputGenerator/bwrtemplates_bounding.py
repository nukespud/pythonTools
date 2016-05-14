# BWR templates built from the basic template
#
#
#     Code:    bwrtemplates.py
#
#     Author:  Joshua Peterson, Brian Ade, and Jianwei Hu
#   
#     Date:     Sep. 11, 2012
#
#     Description:   Used to make BWR assemblies ARP libraries on the fly. 
#  
#
#    
######################################## 



from bwr import *



#  Inital pramaeters for all the codes






#  This is a Fuel assembly class for use with Brian's libaraiy.  The goal is to not to repeat to many lines of code
class Fuel_assembly:
    def __init__(self):
        self.File_name         =''
        self.Parameter         ='check'  
        #self.Parameter='addnux=2,weight'
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
        #  Number of Gad rings
        self.Gdrings           =5
        # Grids per pin
        self.Gridsperpin       =5
        #
        self.Fluxplots         ='yes'
        # Assuming clad den=6.56
        self.Clad_den          =6.56
        # Assuming clad den=6.56
        self.Wall_den          =self.Clad_den
        self.Wall_temp         =0.0
        #  Assuming Gap den =0.0001
        self.Gap_den           =0.0001
        self.Pellet_OR         =0.0
        self.Gap_OR            =0.0
        self.Clad_OR           =0.0
        self.Density_Fuel      =0.0
        self.enrichment        =0.0
        self.Gd2       =0.0
        self.Gd3       =0.0
        self.Max_burnup        =75
        self.Water_Rod_OR      =0.0
        self.Water_Rod_IR      =0.0
        self.Water_Rod_Loc     =[]
        self.Inert_Rod         =[]
        self.Inert_Rod_SS      =[]
        self.Inert_Rod_Loc     =[]
        self.Den_inert         =0.0
        self.powerdens         =22.38
        #  if SS_Clad is used instead of Zircaloy
        self.SS_Clad           =False

#  This runs Bryans script for creating BWR libraries.
def Set_lwr(FA):
    VOID=False
    lwr=0
    # Name of the file
    FA.File_name='%s_%s_enrich_%s_den'%(FA.FILE_NAME,FA.enrichment,FA.void)
    #  Intializig the pointer lwr to the object BWR
    lwr = BWR(sequence='tdepl',model='basic',fname='%s.inp'%(FA.File_name), parms=FA.Parameter)
    #lwr = BWR(sequence='mcd',model='basic',fname='%s.inp'%(FA.File_name))
    # seting the jobinformation for LWR
    lwr.jobinfo(FA.JobInfo)

    # Setting the state of the problem.
    #   tfu=temparture of the fuel
    #   tmo=temperature of the moderator
    #   vf=void fraction
    lwr.state(tfu=FA.Temp_Fuel,tmo=FA.Temp_moderator,vf=FA.void,powden=FA.powerdens)

    # lwr.pitch(pinpitch=0.738*i2cm,latpitch=6.0*i2cm,offset=0.187*i2cm*0.5)
    #  pinpitch= Pin Pitch
    #  latpitch= Lattice Pitch
    #  Offset=?
    lwr.pitch(pinpitch=FA.Pinpitch,latpitch=FA.Latpitch,offset=0.0)

    # Apitch=?
    # Wchan=?
    # TChan=?
    # RiCorner=?
    # Tcorner=?
    lwr.channel(apitch=FA.apitch, wchan=FA.Waterchanel, tchan=FA.Tchanel, ricorner=FA.Ricorner, tcorner=FA.Tcorner)

    # GdRings= Number of Gad rings
    # Gridsperpin= Number of grids needed per pin
    # FluxPlots=?
    lwr.options(gdrings=FA.Gdrings,gridsperpin=FA.Gridsperpin,fluxplots=FA.Fluxplots),

    

    #  Cladding (replace in generic model the word clad)
    # Temp is the temp of the self.tfu*0.2 + self.tmo*0.8
    if FA.SS_Clad:
        lwr.ss('clad', den=FA.Clad_den,type='clad')
    else:
        lwr.zirc2('clad', den=FA.Clad_den,type='clad')

    #  Zirc4 instead of Zirc 2  Cladding for the structure
    lwr.zirc4('can', den=FA.Wall_den, type='struct')

    #  He is the gap
    lwr.he('gap',den=FA.Gap_den, type='gap')

    #  The water is called mod
    if VOID:
        lwr.h2o('mod',type='mod')
    else:
        #print "Warning Warning void fraction is not on, only density"
        lwr.h2o_den('mod',type='mod',den=FA.void)

    # The strucutre water is called mod1
    lwr.h2o('mod1')

    #  Pin dimiesions
    # Pell, Gap, Cladding
    # Cladding thickness 0.81 mm World Nuclear Report
    pindims=[FA.Pellet_OR, FA.Gap_OR ,FA.Clad_OR]
    # F1 material def
    lwr.uo2('f1', den=FA.Density_Fuel, enr=FA.enrichment)
    lwr.fuelpin(1,  pindims,['f1','gap','clad'])

    if FA.Gd2>0:
        #  Gad material, with density, enrichment of fuel, and wt% of gd
        lwr.uo2gd('Gd2%s'%(FA.Gd2), den=FA.Density_Fuel, enr=FA.enrichment,gd=FA.Gd2)
        # Assigning pin 5 two be gad pin
        lwr.fuelpin(2,  pindims,['Gd2%s'%(FA.Gd2),'gap','clad'])

    if FA.Gd3>0:
        #  Gad material, with density, enrichment of fuel, and wt% of gd
        lwr.uo2gd('Gd3%s'%(FA.Gd3), den=FA.Density_Fuel, enr=FA.enrichment,gd=FA.Gd3)
        # Assigning pin 5 two be gad pin
        lwr.fuelpin(3,  pindims,['Gd3%s'%(FA.Gd3),'gap','clad'])

    # If using water Rods:
    # The strucutre water is called mod1
    lwr.h2o('water_rod')
    water_dims=[FA.Water_Rod_IR,FA.Water_Rod_OR]
    for i in range(len(FA.Water_Rod_Loc)):
        lwr.wr('W%s'%(i),water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc[i])
     # If using Inert Rods:
    inert_rod_dims=[FA.Clad_OR]
    for i in range(len(FA.Inert_Rod)):
        lwr.inert_rd('inert%s'%(i),den=FA.Den_inert,tmp=FA.Temp_moderator,per_ss=FA.Inert_Rod[i])
        lwr.pin('inert%s'%(i),inert_rod_dims,['inert%i'%(i)],xyloc=FA.Inert_Rod_Loc[i])

    for i in range(len(FA.Inert_Rod_SS)):
        lwr.inert_rd_ss('inert%s'%(i),den=FA.Den_inert,tmp=FA.Temp_moderator,per_ss=FA.Inert_Rod_SS[i])
        lwr.pin('inert%s'%(i),inert_rod_dims,['inert%i'%(i)],xyloc=FA.Inert_Rod_Loc[i])


 

    lwr.burnups(max=FA.Max_burnup)
    return lwr





def bwr_7x7(enrichment,void):
    # Class called fuel assembly

    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
     # File name to be saved
    FA.FILE_NAME='g4607g3b-b'
    # Information abou the job
    FA.JobInfo='BWR 7x7 Ge3B v2b ARP generation   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=  10.741
    # Temperateru of Fuel in C
    FA.Temp_Fuel=1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.21158/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.24206/2
    #
    #
    FA.Gap_den= 0.0001
    ## Cladding outside radius in cm
    FA.Clad_OR=1.43002/2
    # Clad Density
    FA.Clad_den=6.56

    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator= 560.7
    # Pin Pitch in cm
    FA.Pinpitch= 1.9447
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch=FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.40612
    # Assembly channel thickness
    FA.Tchanel=0.2032
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel
    #
    # Cladding walls
    FA.Wall_den=FA.Clad_den
    # Cladding wall temp
    FA.Wall_temp=FA.Temp_moderator


    # Gd rod information
    # Gad rod information
    # Number of Gd rings
    # Enrichment of Gad 2
    FA.Gd2=4.0
    # Enrichmet of Gad 3
    FA.Gd3=3.0


    #  Set information for fuel assembly
    lwr=Set_lwr(FA)



    #Name of the file
    lwr.lattice(""" 1
                    1  2
                    1  1  1
                    1  1  1  3
                    1  1  1  1  1
                    1  1  3  1  1  2
                    1  1  1  1  1  1  1""")
    lwr.cb(type='basic')

    return lwr,FA










def bwr_8x8(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void

    FA.FILE_NAME='g4608g4b-b'
    # Information abou the job
    FA.JobInfo='BWR 8x8 Ge9 ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.741
    # Temperateru of Fuel in C
    FA.Temp_Fuel=1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.05664/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.0795/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.25222/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=560.7
    # Pin Pitch in cm
    FA.Pinpitch=1.6256
    #Latice pitch in cm
    FA.Latpitch=15.24
    # Assemply pitch
    FA.apitch=FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.40612
    # Assembly channel thickness
    FA.Tchanel=0.2032
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner= FA.Tchanel



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gd2=3.0
    # Enrichmet of Gad 3
    #Gd3=3.0

    # Water rod cladding outside radius
    FA.Water_Rod_OR=1.25222/2
    # Water Rod Inner radius
    FA.Water_Rod_IR=1.0795/2 #Water_Rod_OR-Water_Rod_thick
    # Water rod 1 location
    FA.Water_Rod_Loc.append([-FA.Pinpitch/2,FA.Pinpitch/2])
    # Water rod 2 location

    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    2  1  1
                    1  1  1  0
                    1  1  1  1  1
                    1  1  1  1  1  2
                    1  1  1  1  1  1  1
                    1  1  2  1  1  1  1  1""")
    lwr.cb(type='basic')
    return lwr,FA



def bwr_9x9(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void

    # File name to be saved
    FA.FILE_NAME='g4609a-b'
    # Information abou the job
    FA.JobInfo='BWR 9x9 Ge11 9x9 with 7 rods replaced with WR ARP generation   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel= 10.741
    # Temperateru of Fuel in C
    FA.Temp_Fuel=1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=.88456/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=.92456/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.07696/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=560.7
    # Pin Pitch in cm
    FA.Pinpitch=1.45288
    #Latice pitch in cm
    FA.Latpitch=15.24
    # Assemply pitch
    FA.apitch=FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.33754
    # Assembly channel thickness
    FA.Tchanel=0.2032
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gd2=3.0
    # Enrichmet of Gad 3
    #Gd3=3.0


    # Water rod cladding outside radius
    # Number of water rods
    FA.Num_Water_Rods=0
    #FA.Water_Rod_OR=2.52/2
    # Water Rod Inner radius
    #FA.Water_Rod_IR=2.32/2 #Water_Rod_OR-Water_Rod_thick
    # Water rod 1 location
    #FA.Water_Rod_Loc_1=[-.892,-.892]
    # Water rod 2 location
    #FA.Water_Rod_Loc_2=[.892, .892]
    # End of user input

    FA.Inert_Rod_SS.append(.9999)
    FA.Inert_Rod_SS.append(.9999)
    #  Inert rod locaiton
    FA.Inert_Rod_Loc.append([0,0]  )
    FA.Inert_Rod_Loc.append([FA.Pinpitch,-FA.Pinpitch])

    FA.Den_inert=6.55  # Density of ZIRC2 g/cc
    
    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    1  1  2
                    1  1  1  1
                    1  1  1  1  0
                    1  2  1  1  1  0
                    1  1  1  1  1  1  1
                    1  1  2  1  1  2  1  1
                    1  1  1  1  1  1  1  1  1""")
    lwr.cb(type='basic')
    return lwr,FA









def bwr_4_6_10x10(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void




    # File name to be saved
    FA.FILE_NAME='g4610g14-b'
    # Information abou the job
    FA.JobInfo='BWR 10x10 ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.741
    # Temperateru of Fuel in C
    FA.Temp_Fuel= 1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=0.876/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   0.894/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.026/2


    # Assemblyh data
    # Moderator temperate (C)
    FA.Temp_moderator=560.7
    # Pin Pitch in cm
    FA.Pinpitch=1.295
    #Latice pitch in cm
    FA.Latpitch=15.24
    #
    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=13.15
    # Assembly channel thickness
    FA.Tchanel=0.2
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gd2=5.0
    # Enrichmet of Gad 3
    #Gd3=3.0

    # Plot flux
    FA.Fluxplots='yes'
    # Maximum Burnup



    # Water Rod Data
    # Water rod cladding outside radius
    FA.Water_Rod_IR=2.322/2
    # Water Rod Inner radius
    FA.Water_Rod_OR=2.522/2
    # Water rod 1 location
    FA.Water_Rod_Loc.append([FA.Pinpitch,FA.Pinpitch])
    # Water rod 2 location
    FA.Water_Rod_Loc.append([-FA.Pinpitch,-FA.Pinpitch])


     #  Set information for fuel assembly
    lwr=Set_lwr(FA)


    lwr.lattice(""" 1
                    1  2
                    1  1  1
                    1  2  1  1
                    1  1  1  1  1
                    1  2  1  0  0  1
                    1  1  1  0  0  1  1
                    1  1  2  1  1  1  1  1
                    1  2  1  1  2  1  2  1  2
                    1  1  1  1  1  1  1  1  1  1""")
    lwr.cb(type='basic')
    return lwr,FA



def bwr_xdr(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void



    # File name to be saved
    FA.FILE_NAME='xdr06g5-b'
    # Information abou the job
    FA.JobInfo='BWR 6x6 ARP generation Ref for XDR06G5 assembly type   '
     
    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel= 10.741
    # Temperateru of Fuel in C 
    FA.Temp_Fuel=1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.22428/2 
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.25095/2 
    ## Cladding outside radius in cm
    FA.Clad_OR=1.42875/2 
    # Assemblyh data
    # Moderator temperate (C) 
    FA.Temp_moderator=560.7
    # Pin Pitch in cm
    FA.Pinpitch=1.8034
    #Latice pitch in cm
    FA.Latpitch=12.922
    #
    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=10.922
    # Assembly channel thickness
    FA.Tchanel=0.2032   
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
    lwr.cb(type='basic',halfspan=FA.Waterchanel-FA.Tchanel-.1,npins=17)    
    return lwr,FA 
    
    
    
    
    
    
    
    
def bwr_xlc(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
    # File name to be saved
    FA.FILE_NAME='xlc10a-b'
    # Information abou the job
    FA.JobInfo='BWR 10x10 ARP generation Ref for HLC10a assembly type   '
     
    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=  10.741
    # Temperateru of Fuel in C 
    FA.Temp_Fuel=1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=.889/2 
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   .89916/2 
    ## Cladding outside radius in cm
    FA.Clad_OR=1.00076/2 
    
    
    # Assemblyh data
    # Moderator temperate (C) 
    FA.Temp_moderator= 560.7
    # Pin Pitch in cm
    FA.Pinpitch=1.41478
    #Latice pitch in cm
    FA.Latpitch=16.1798
    # Grids per each 

    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=14.25956
    # Assembly channel thickness
    FA.Tchanel=0.2032   
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel
    
    #  For inert rods need to specifiy fraction of materail, Location, and Densitiy
    #  Percent SS in Inert Rod
    FA.Inert_Rod_SS.append(.98)
    FA.Inert_Rod_SS.append(.98)
    FA.Inert_Rod_SS.append(.98)
    FA.Inert_Rod_SS.append(.994)
    #  Inert rod locaiton
    FA.Inert_Rod_Loc.append([FA.Pinpitch/2,FA.Pinpitch/2]  )
    FA.Inert_Rod_Loc.append([-FA.Pinpitch/2,-FA.Pinpitch/2])
    FA.Inert_Rod_Loc.append([FA.Pinpitch/2,-FA.Pinpitch/2] )
    FA.Inert_Rod_Loc.append([-FA.Pinpitch/2,FA.Pinpitch/2] )
    FA.Den_inert=8.03  # Density of SS g/cc
    FA.SS_Clad=True
    
    lwr=Set_lwr(FA)
    
    
    
    
           
            
    #Name of the file
    lwr.lattice("""1
                   1  1
                   1  1  1
                   1  1  1  1
                   1  1  1  1  0
                   1  1  1  1  0  0
                   1  1  1  1  1  1  1
                   1  1  1  1  1  1  1  1
                   1  1  1  1  1  1  1  1  1
                   1  1  1  1  1  1  1  1  1  1""")
    lwr.cb(type='basic',halfspan=FA.Waterchanel-.75,npins=23)
    return lwr,FA

 
 
 
def bwr_xbr(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void



    # File name to be saved
    FA.FILE_NAME='xbr09a-b'
    # Information abou the job
    FA.JobInfo='BWR 9x9 ARP generation for xbr09a assembly type   '
     
    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel= 10.741
    # Temperateru of Fuel in C 
    FA.Temp_Fuel=1200
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.21603/2 
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=1.25603/2 
    ## Cladding outside radius in cm
    FA.Clad_OR=1.42875/2 
    # Assemblyh data
    # Moderator temperate (C) 
    FA.Temp_moderator=560.7
    # Pin Pitch in cm
    #FA.Pinpitch=1.79352
    FA.Pinpitch=1.7713
    #Latice pitch in cm
    FA.Latpitch=18.1417
    #
    FA.apitch= FA.Latpitch
    # Assembly channel inner dimension (cm)
    FA.Waterchanel=16.1417
    # Assembly channel thickness
    FA.Tchanel=0.2032   
    # Radius of the corners
    FA.Ricorner= 0.9652
    # Corner thickness
    FA.Tcorner=FA.Tchanel
    #  For inert rods need to specifiy fraction of materail, Location, and Densitiy
    #  Percent SS in Inert Rod
    FA.Gd2=1.5
    
    FA.Inert_Rod_SS.append(.994)
    FA.Inert_Rod_SS.append(.994)
    FA.Inert_Rod_SS.append(.994)
    FA.Inert_Rod_SS.append(.994)
    #  Inert rod locaiton
    FA.Inert_Rod_Loc.append([FA.Pinpitch,FA.Pinpitch]  )
    FA.Inert_Rod_Loc.append([-FA.Pinpitch,-FA.Pinpitch])
    FA.Inert_Rod_Loc.append([FA.Pinpitch,-FA.Pinpitch] )
    FA.Inert_Rod_Loc.append([-FA.Pinpitch,FA.Pinpitch] )
    FA.Den_inert=6.55  # Density of ZIRC2 g/cc
    FA.SS_Clad=False    

    lwr=Set_lwr(FA)    
                                        
    #Name of the file
    lwr.lattice(""" 1
                    1  2
                    1  1  1
                    1  1  1  0
                    1  1  1  1  1
                    1  1  1  0  1  0
                    1  1  1  1  1  1  1
                    1  2  1  1  1  1  1  2
                    1  1  1  1  1  1  1  1  1""")
    lwr.cb(type='basic',halfspan=FA.Waterchanel-FA.Tchanel,npins=28)    
    return lwr,FA 


