#!/usr/bin/env python
#
#
#     Code: scale_scrpt.py
#
#     Author:  Joshua Peterson
#
#     Date:
#     Description:  Python moduels for scale
########################################



#  Includes
#
#          scale_mat2_mcnp(Scale_file)
#          get_psoition_ft71(Scale_file,MIX)
#          get_flux_scale(SCALE_output,MAT)
#          get_CE_scale_flux(SCALE_output)

import sys
import os




#  Here is a class for cells
class Mat:  #This is the name of the class that will hold all of the mater information for scale
    '''  Represents any cell in input deck '''
    def __init__(self):
        self.sc        =''         # standard composition
        self.mx        ='0'    # mixture no.
        self.den       ='0.0'  #  atomic density
        self.roth      ='0.0'  #  theetical density
        self.nel       ='0'    # no. elements
        self.icp       ='0'    # 0/1 mixture/compound
        self.temp      ='0.0'  # deg kelvin
        self.zzzaaa    ='0'    #100.000 wt%
    #     sc  h-1              standard composition
    #     mx             2     mixture no.
    #     den   3.9714E-02     atomic density
    #     roth      1.0000     theoretical density
    #     nel            1     no. elements
    #     icp            0     0/1 mixture/compound
    #     temp       293.6     deg kelvin
     #                1001   100.000 wt%
    #     end                 #
    #      Run:   scale_mat2_mcnp.py [scale_file.out]
    ########################################


##  Here is a class for cells
class Fluxes:  #This is the name of the class that will hold all of the cells information
    '''  Represents any cell in input deck '''
    def __init__(self):
        self.result    =[]    # number of the material in the cell
        self.group     =[]
        self.flux      =[]
        self.error     =[]
        self.region    =[]

















def get_position_ft71(Scale_output,MIX):
    # MIX matrix of mixtures
    #!/usr/bin/env python
    #
    #       get_positions.py
    #
    #       Gets   positions in the ft71 input file
    #
    #
    #
    # ************************





    input_file = open(Scale_output, 'r')
    Results={}
    for line in input_file:
        if "Position  Time Step" in line:
            DATA=True
            while DATA:
                line=input_file.next()
                #print line
                temp=line.split()
                if int(temp[1])==1:
                    if len(temp)==13:
                        Results[int(temp[12])]=int(temp[0])
                    else:
                        DATA=False

    for i in MIX:
        print Results[i] , ", " ,

#  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++









#  *****************    SCALE MATERIAL TO MCNP **********************
def scale_mat2_mcnp(Scale_file,Mat_num,START_MAT):
    #Mat_num=range(1,10)   # Enter the desired material numbers
    #    START_MAT=100         # Enter the desired starting number
    # Scale.out file

    #
    #
    #     Code: scale_mat2_mcnp.py
    #
    #     Author:  Joshua Peterson
    #
    #     Date:  July 25 2011
    #
    #     Description:  This gets material information from scale and writes it in mcnp format
    #    Scale format should be like




    #################   Check for the write inport format
    input_file = open(Scale_file, 'r')

    ########################3    Get Mat prop from code   ######################3
    #    Scale format should be like
    # h-1         2     0     3.97136E-02     293.6     end
    # o-16        2     0     1.98568E-02     293.6     end
    # si          2     0     8.18321E-05     293.6     end
    # fe          2     0     7.20198E-05     293.6     end
    # cu          2     0     3.61680E-05     293.6     end

    test=1
    results={}
    counter=0
    for line in input_file:
        if 'problem composition description' in line:  # This is start of information
            input_file.next()
        while test==1:
                newline=input_file.next()
                temp=newline.split()
                #  Here is the iterative process to get all of the needed information
                try:
                    if temp[0]=='sc':
                        results[counter]=Mat()
                        #  SC
                        results[counter].sc=temp[1]
                        newline=input_file.next()
                        temp=newline.split()
                        # Mix
                        results[counter].mx=int(temp[1])
                        newline=input_file.next()
                        temp=newline.split()
                        #  den
                        results[counter].den=float(temp[1])
                        newline=input_file.next()
                        temp=newline.split()
                        # roth
                        results[counter].roth=float(temp[1])
                        newline=input_file.next()
                        temp=newline.split()
                        #  nel
                        results[counter].nel=int(temp[1])
                        newline=input_file.next()
                        temp=newline.split()
                        # icp
                        results[counter].icp=int(temp[1])
                        newline=input_file.next()
                        temp=newline.split()
                        #  temp
                        results[counter].nel=float(temp[1])
                        newline=input_file.next()
                        temp=newline.split()
                        # zzzaaa
                        results[counter].zzzaaa=int(temp[0])
                        counter=counter+1
                    if temp[0]=='****':
    #                      print temp
                         break

                except IndexError:
                    temp=1
    #                 print "This is blank line  Error"



    #  This is where I print out the results

    Total_den=[]
    sum
    #  Sum total density
    for num in Mat_num:
        sum=0.0
        for i in results:
            if results[i].mx==num:
                sum=sum+results[i].den
        Total_den.append(sum)


    #  Print results
    for num in Mat_num:
        print "c    Total density is %1.3e atoms/barn cm"%(Total_den[num])
        print "m%i"%(START_MAT+num)
    #     sum=0.0
        for i in results:
    #         print results[i].mx, '   ', num
            if results[i].mx==num:
                print "       ", results[i].zzzaaa, "     ", results[i].den
    #             sum=sum+results[i].den
        print "mt%i   lwtr" %(START_MAT+num)
        Total_den.append(sum)










#  ===================================================Get Flux Scale
def get_flux_scale(SCALE_output):
    ''' This gets flux of specific material number from scale as a funciton of depletion
       returns Time and the Flux for all of the mixture numbers
    '''


    input_file = open(SCALE_output, 'r')

    #--- Material powers for depletion pass no.   0 (MW/MITHM) ---
    #   Time =     0.00 days (   0.000 y), Burnup = 0.00     GWd/MTIHM, Transport k= 0.9909
    #
    #                Total    Fractional  Mixture     Mixture       Mixture
    #     Mixture    Power      Power      Power    Thermal Flux  Total Flux
    #      Number (MW/MTIHM)    (---)   (MW/MTIHM)  n/(cm^2*sec)  n/(cm^2*sec)
    #         1       3.596    0.00042     N/A       2.5786E+13    3.7153E+13
    #         2       9.006    0.00106     N/A       7.9161E+14    2.1804E+15
    #         3       3.729    0.00044     N/A       2.6502E+13    3.7990E+13
    #         4       4.084    0.00048     N/A       6.4625E+12    7.7361E+12
    #         5       2.095    0.00025     N/A       3.6407E+14    5.5646E+14

    Time=[]
    Flux={}
    Thermal_Flux={}
    First=True
    for line in input_file:
        if "Material powers for depletion pass no" in line:
            Read=True
            while(Read):
                line=input_file.next()
                temp=line.split()
                try:
                    if First:
                        Flux[int(temp[0])]=Fluxes()
                        Thermal_Flux[int(temp[0])]=Fluxes()
                    Thermal_Flux[int(temp[0])].result.append(float(temp[4]))
                    Flux[int(temp[0])].result.append(float(temp[5]))
                    #print temp
                except ValueError:
                    if "Time" in line:
                        Time.append(float(temp[2]))
                    #print "ValueError",temp
                except IndexError:
                    temp=0
                    #print "IndexError",temp
                if "Total Power is the Mixture Power per 1 metric ton of HM of the initial  " in line:
                    Read=False
                    First=False

    #Fluence={}
    #
    #for cells in Flux:
    #    Fluence[cells]=[]
    #    #print cells,
    #    #for i in [1,6]:
    #    for i in range(len(Flux[cells].result)):
    #        flux=Flux[cells].result[i]
    #        time_value=Time[i]
    #        Fluence[cells].append(flux*time_value)
    #    #    print value,
    #    #print


    return(Time,Thermal_Flux,Flux)
    print "Returning thermal Flux"
    #return(Time,Thermal_Flux)

    # for t in Time:
    #     output_file.write("%s  "%(t))
    # output_file.write(" \n")
    # for i in Mat_Num:
    #    for cells in Flux:
    #
    #      if int(i)==int(cells):
    #         output_file.write('%s '%(cells))
    #         for result in Flux[cells].result:
    #             output_file.write("%s  "%(result))
    #         output_file.write('\n')


#  ===================================================================





def get_CE_scale_flux(SCALE_output):
    # fluxes for this problem
    #            region   1
    #
    #  group   flux     percent
    #                  deviation
    #     1   1.727E-05    3.12
    # 1                                        toy model of hfir
    #
    #  fluxes for this problem
    #            region   1
    #
    input_file = open(SCALE_output, 'r')
    Zone=0
    Old_region=100
    Saved_flux={}
    for line in input_file:
        #  This is where the flux information is saved
        if "fluxes for this problem" in line or "Collapsed fluxes" in line:
            #  loop through lines
            Continue=True
            while(Continue):
                try:
                    line=input_file.next()
                    temp=line.split()
                    # Region is even and last one tells you if it is increasing or newer
                    if 'region' in line:
                        # Gets the last number of region and if it is greater then before then contiues
                        New_region=temp[len(temp)-1]
                        if int(New_region)<int(Old_region)+6:
                            Zone=Zone+1
                            Saved_flux[Zone]=Fluxes()
                        print Zone, Old_region,New_region
                        Old_region=New_region
                        #print Zone



                    if 'deviation' in line:

                        line=input_file.next()
                        temp=line.split()
                        temp.pop(0)
                        #print temp
                        for i in range(len(temp)):
                            if i%2==0:
                                Saved_flux[Zone].flux.append(temp[i])
                                Saved_flux[Zone].error.append(temp[i+1])

                        #print temp

                    #print line
                    if "frequency" in line:
                        Continue=False
                except StopIteration:
                    Continue=False


    print "Zone\tFlux\tError"
    for zone in Saved_flux:
        for i in range(len(Saved_flux[zone].flux)):
            Results=Saved_flux[zone].flux[i]
            Error=Saved_flux[zone].error[i]
            print "%s\t%s\t%s\t"%(zone, Results, Error)





            #class Fluxes:  #This is the
            #    '''  Represents any cell
            #    def __init__(self):
            #        self.result    =[]
            #        self.group     =[]
            #        self.flux=     =[]
            #        self.error=    =[]
            #        self.region    =[]



#
SCALE=1E12
def write_arp_data(ARP_DATA_FILE,cell_fluence):
    '''  ARP_DATA_FILE is the name of the Arp file that will be saved
         Cell_fluence is the array of fluences for the cell
    '''
    Arp_data_file=open(ARP_DATA_FILE,'w')


    #  Need to adjust for ORIGEN ARP
    new_cell_fluence=[]
    for res in cell_fluence:
        new_cell_fluence.append(res/SCALE)






    # Write input for ARP data library================
    Arp_data_file.write("!act-hfir\n")
    #  First two are number of seperate cross section sets for each varaible.  The third is the number of sets in the library
    Arp_data_file.write("1 1 %s                  \n"%(len(cell_fluence)))
    # Not used
    Arp_data_file.write("1                      \n")
    # 1 Means total flux
    Arp_data_file.write("1                      \n")
    #  Genearly only needs one libarary name
    Arp_data_file.write("'act-hfir-new.arplib'  \n")
    #  Fluence value reduced by 10E-24 to avoid numerical problems during interpolation.
    for result in new_cell_fluence:
        Arp_data_file.write("%.4E    \n"%(result))

    Arp_data_file.close()


def write_arp_inp(Output_file,ARP_DATA_FILE, Irradation_Period,Neutron_Flux,Mat_num):

    LENGTH=5

    Neutron_Flux_new=[]
    for flux in Neutron_Flux:
        Neutron_Flux_new.append(flux/SCALE)




    Output_file.write("=shell\n")
    Output_file.write("    cp $INPDIR/ARP_SAVED_DATA/%s_%s  arpdata.txt \n"%(ARP_DATA_FILE,Mat_num))
    Output_file.write("    cp $INPDIR/FT33_LIB/ft33f001.mix0%s   act-hfir-new.arplib \n"%(Mat_num))
    Output_file.write("end\n\n\n")
    Output_file.write("=arp \n")
    #1 Library Name
    Output_file.write(" act-hfir \n")
    #2 Reserved interpolation paramater (?Dummy value 1.0)
    Output_file.write(" 1.0 \n")
    # Number of cycles

    Output_file.write(" %s   \n"%(len(Irradation_Period)))
    #Fuel irradation period  (Irradation time for each cycle)
    count=0
    for irr in Irradation_Period:
        Output_file.write(" %s"%(irr))
        count=count+1
        if count%LENGTH==0:
            Output_file.write(" \n")
    if count%LENGTH!=0:
        Output_file.write("\n")
    #5 Neutron flux
    count=0
    for flux in Neutron_Flux_new:
        Output_file.write("  %.4E  "%(flux))
        count=count+1
        if count%LENGTH==0:
            Output_file.write(" \n")
    if count%LENGTH!=0:
        Output_file.write("\n")

    #6 Number of libraries for each cycle
    count=0
    for i in range(len(Neutron_Flux)):
        Output_file.write("  1  ")
        count=count+1
        if count%LENGTH==0:
            Output_file.write(" \n")
    if count%LENGTH!=0:
        Output_file.write("\n")

    #7  Flux type (0 thermal 1 total flux)
    Output_file.write(" 1 \n")
    #8 New Library name
    Output_file.write(" ft33f001 \n")
    Output_file.write("end   \n")




