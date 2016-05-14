#!/usr/bin/env python
#
#
#     Code: IsoConverter
#
#     Author:  Joshua Peterson
#
#     Date:    September 15, 2015
#
#     Description:  Used to convert MC2-3 output cross sections into Fissipin input cross sections
#
########################################
__author__ = 'f4p'




# class Data:
#     ''' Represent Isotopic data'''
#     def __init__(self):
#         self.AAAZZZ=0
#         self.Na_me =''
#         self.Name  =''
#         self.mass  = 0.0
#         self.nuclide_type='0'

# def get_isotope():
#     """  This gets isotope information from data.txt found in /home/f4p/PYTHON_PATH/data.txt
#     It uses this informaiton for addition work
#     """
#     from os.path import expanduser
#     home = expanduser("~")
#     DATA_FILE=home+'/PYTHON_PATH/data.txt'
#     input_file=open(DATA_FILE,'r')
#
#     # GET meta data too
#     GET_META=False
#     Results={}
#     count=0
#     Start=False
#     for line in input_file:
#         if "Name" in line:
#             Start=True
#             line=input_file.next()
#         if Start:
#             temp=line.split()
#             if len(temp)==5:
#                 name=temp[1]
#                 Results[name]=Data()
#                 Results[name].AAAZZZ=int(temp[2])
#                 Results[name].Na_me=temp[0]
#                 Results[name].Name=temp[1]
#                 Results[name].mass=float(temp[3])
#                 Results[name].nuclide_type=float((temp[4]))


#    for res in range(len(Results)):
#        print Results[res].AAAZZZ ,Results[res].Na_me,Results[res].Name,Results[res].mass
    #print "Returning isotopic data informaiton"



INPUT_NAME = ["SFR_Driver_MC2.txt","SFR_Blanket_MC2.txt"]
count=0
for inputName in INPUT_NAME:
    count+=1
    print "' For the inputfile "+inputName
    # INPUT_NAME = "driver.microxs_bg"
    inputFile=open(inputName, 'r');
    # outputFile=open(inputName + ".out", 'w')
    # Iso_data=get_isotope()

    # U234_7
    #        energy(eV)     capture  scattering       total   transport     fission          nu         chi
    #    1  1.4191E+07  4.8940E-01  1.0449E+01  1.1549E+01  9.9232E+00  1.1961E-01  2.4734E+00  1.0000E+00
    inputFile=open(inputName, 'r');
    counter=0
    # for line in inputFile:
    #     if "7" in line and len(line.split())==1:
    #         counter+=1
    # inputFile.close

    inputFile=open(inputName, 'r');
    # outputFile.write("TOTNUC=    %s\n"%(counter))
    # outputFile.write("TOTSTATE=     1\n")
    # outputFile.write("BURNUP=    0.000e+00\n")
    for line in inputFile:
        atomic_mass=line.split()[2]
        iso=line.split()[0]
        iso=iso[:-1]
        iso=iso.split("_")[0]
        if iso[1].isdigit():
            print "%s-%s %s 0 %s  900 end"%(iso[0:1],iso[1:],count,atomic_mass)
        elif iso[2].isdigit():
            print "%s-%s %s 0 %s  900 end"%(iso[0:2],iso[2:],count,atomic_mass)
        # else:
        #  print "Error",iso,count,
        # if "7" in line and len(line.split())==1:
        #     if "_" in line:
        #         isotope=line.split("_")[0].strip()
        #     else:
        #         isotope=line.split()[0][:-1].strip()

            # outputFile.write("PARENT_NUCLIDE=  %s      0      "%(Iso_data[isotope.lower()].AAAZZZ))
            # inputFile.next()
            # line=inputFile.next()
            # temp=line.split()
            # capture_102=temp[2]
            # scatter=temp[3]
            # total=temp[4]
            # transport=temp[5]
            # if len(temp)>6:
                # fission_18=temp[6]
                # outputFile.write("2\n")
                # outputFile.write("    18      0 %.6e\n"%(float(fission_18)))
            # else:
               # outputFile.write( "1\n")

            # outputFile.write("   102      0 %.6e\n"%(float(capture_102)))
    # outputFile.write("\n")
    # outputFile.close()
    inputFile.close()
    print " \n"








