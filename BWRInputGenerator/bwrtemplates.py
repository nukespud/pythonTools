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


# Maximum Burnup
Max_burnup=71



#  This is a Fuel assembly class for use with Brian's libaraiy.  The goal is to not to repeat to many lines of code
class Fuel_assembly:
    def __init__(self):
        self.File_name         =''
        self.Parameter         ='check'  #Parameter='addnux=2,weight'
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

    lwr=0
    # Name of the file
    FA.File_name='%s_%s_enrich_%s_void'%(FA.FILE_NAME,FA.enrichment,FA.void)
    #  Intializig the pointer lwr to the object BWR
    lwr = BWR(sequence='tdepl',model='basic',fname='%s.inp'%(FA.File_name), parms=FA.Parameter)
    # seting the jobinformation for LWR
    lwr.jobinfo(FA.JobInfo)

    # Setting the state of the problem.
    #   tfu=temparture of the fuel
    #   tmo=temperature of the moderator
    #   vf=void fraction
    lwr.state(tfu=FA.Temp_Fuel,tmo=FA.Temp_moderator,vf=FA.void)

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
    lwr.zirc2('clad', den=FA.Clad_den,type='clad')

    #  Zirc4 instead of Zirc 2  Cladding for the structure
    lwr.zirc4('can', den=FA.Wall_den, type='struct')

    #  He is the gap
    lwr.he('gap',den=FA.Gap_den, type='gap')

    #  The water is called mod
    lwr.h2o('mod',type='mod')

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
    if FA.Num_Water_Rods>0:
        # The strucutre water is called mod1
        lwr.h2o('water_rod')
        water_dims=[FA.Water_Rod_IR,FA.Water_Rod_OR]
        for i in range(FA.Num_Water_Rods):

            if i==0:
                lwr.wr('W1',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_1)
            if i==1:
                lwr.wr('W2',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_2)
            if i==2:
                lwr.wr('W3',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_3)
            if i==3:
                lwr.wr('W4',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_4)
            if i==4:
                lwr.wr('W5',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_5)
            if i==5:
                lwr.wr('W6',water_dims,['water_rod','can'],xyloc=FA.Water_Rod_Loc_6)


    lwr.burnups(max=Max_burnup)
    return lwr





def bwr_2_3_7x7(enrichment,void):
    # Class called fuel assembly

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
    FA.Density_Fuel= 10.32
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


    return lwr,FA










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
    FA.Density_Fuel=10.32
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
    FA.Gd2=3.0
    # Enrichmet of Gad 3
    #Gd3=3.0

    FA.Num_Water_Rods=1
    # Water rod cladding outside radius
    FA.Water_Rod_OR=3.4036/2
    # Water Rod Inner radius
    FA.Water_Rod_IR=3.2004/2 #Water_Rod_OR-Water_Rod_thick
    # Water rod 1 location
    FA.Water_Rod_Loc_1=[0,0]
    # Water rod 2 location

    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    1  1  1
                    1  2  1  0
                    1  1  1  0  0
                    1  2  1  1  1  2
                    1  1  2  1  2  1  1
                    1  1  1  1  1  1  1  1""")

    return lwr,FA



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
    FA.Density_Fuel=  10.32
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
    FA.Gd2=5.0
    # Enrichmet of Gad 3
    #Gd3=3.0


    # Water rod cladding outside radius
    # Number of water rods
    FA.Num_Water_Rods=2
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
                    1  1  2
                    1  2  1  1
                    1  1  1  0  0
                    1  1  1  0  0  1
                    1  2  1  1  1  1  2
                    1  1  2  2  1  2  1  1
                    1  1  1  1  1  1  1  1  1""")

    return lwr,FA








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
    FA.Gap_OR=   1.26744/2
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

    return lwr,FA





def bwr_4_6_8x8(enrichment,void):
    #  Creat an object called fuel assembly
    FA=Fuel_assembly()

    # Enrichmet of fuel
    FA.enrichment=enrichment
    # Void fraction of fuel
    FA.void=void
    # File name to be saved
    FA.FILE_NAME='bwr8x8_4_6'
    # Information abou the job
    FA.JobInfo='BWR 8x8 ANF-pressurized ARP generation Ref   '

    # Fuel rod data
    # Density of fuel in g/cc
    FA.Density_Fuel=10.32
    # Temperateru of Fuel in C
    FA.Temp_Fuel=840
    # Pelllet Outside radius in cm
    FA.Pellet_OR=1.057/2
    ##  Calculated Gap outside radius in cm
    FA.Gap_OR=   1.15736/2
    ## Cladding outside radius in cm
    FA.Clad_OR=1.22936/2


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



    # Gd rod information
    # Enrichment of Gad 2
    FA.Gd2=4.0
    # Enrichmet of Gad 3
    FA.Gd3=3.0

    #   # Water Rod Data
    #   #  def wr(self,pinnum,dims,mats,xyloc=[0.0,0.0]):
    FA.Water_Rod_thick=0.074
    # Water rod cladding outside radius
    FA.Water_Rod_OR=2.6187/2
    FA.Water_Rod_IR=FA.Water_Rod_OR-FA.Water_Rod_thick
    FA.Water_Rod_IR=2.4561/2


    #  Set information for fuel assembly
    lwr=Set_lwr(FA)

    #Name of the file
    lwr.lattice(""" 1
                    1  1
                    2  1  1
                    1  1  1  0
                    1  1  1  0  0
                    2  1  1  1  1  1
                    1  1  1  1  1  1  1
                    1  1  2  1  1  2  1  1""")
    return lwr,FA










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
    FA.Gap_OR=   0.967/2
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
    FA.Gd2=5.0
    # Enrichmet of Gad 3
    #Gd3=3.0

    # Plot flux
    FA.Fluxplots='yes'
    # Maximum Burnup
    FA.Max_burnup=71
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
    return lwr,FA




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
    FA.Density_Fuel=   10.32
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
    FA.Gd2=5.0
    # Enrichmet of Gad 3
    #Gd3=3.0

    # Plot flux
    FA.Fluxplots='yes'
    # Maximum Burnup
    FA.Max_burnup=71
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

    return lwr,FA



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
    FA.Density_Fuel=10.32
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
    #
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
    
    return lwr,FA 
    
    
    
    
    
    
    
    
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
    FA.Density_Fuel=  10.32
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

    return lwr,FA





