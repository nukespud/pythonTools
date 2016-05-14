#!/usr/bin/env python
#
#
#     Code: MCNP_to_Heating_Decay.py 
#
#     Author:  Joshua Peterson
#   
#     Date:    Second week after Joshua Left
#
#     Description:                Creates tallies for MCNP, writes inputs to Couple and Origen, Reads tallies ... All in one.
#
########################################    

import sys
import os
import os.path 
# For sorting purposes
from operator import itemgetter
import operator



    
#  This is the class of tallies that will hold tally number and other information        
class Tallies:  
    def __init__(self):
        self.result=0.0
        self.error=0.0
        self.cell_num =[]      # Cell number
        self.tally_num= []      # Tally number
        self.tally_result=[]  #  Tally result
        self.tally_error=[]   #  Tally error 
        self.multiplier =0.0   # Tally multiplier
        # Energy min value
        self.energy_min=[]    
        # Energy max value
        self.energy_max=[]
        
        self.energy_tally=[]
        
        self.energy_error=[]
        
        self.energy_cell=[]
        # Number of particles per sec used in this tally
        self.nps=0
        #
        self.mult_cell=[]
        self.mult_multiply=[]  #for use with the fm card
        #  Material it is being multipled by
        self.mult_mat=[]
        #  Number it is being multipled for (reaction rate)
        self.mult_mtnum=[]
        # Result for multipling tallies
        self.mult_tally=[]
        #  Error of mulitipling tallies
        self.mult_error=[] 
        #  Multiplicion value usually one
        self.mult_value=[]
        #  Reaction rate value
        self.mult_reaction=[]
        # Micro cross section
        self.multi_micro=[]
        self.micro_error=[]
        
#  This is used for tailles with materal number tally cell number ext.   
class MAT:                                                                  
    def __init__(self):
        self.mtnum=[]
        self.tally=[]
        self.error=[]
        self.cell=[]
        self.multiply=[]
        self.flux=0.0
        self.micro={}



#  Here is a class for cells
class Cells:  #This is the name of the class that will hold all of the cells information
    '''  Represents any cell in input deck '''
    def __init__(self):
        self.mat    =''
        self.rhoatm =0.0
        self.rhogrm =0.0
        self.vol    =0.0
        self.mass   =0.0
        self.pieces =0
        self.nimp   =0.0
        self.new_vol=0.0
        self.new_vol_err=0.0



class Data:
    ''' Represent Isotopic data'''
    def __init__(self):
        self.AAAZZZ=0
        self.Na_me =''
        self.Name  =''
        self.mass  = 0.0
        self.nuclide_type='0'


class Material:
    ''' Material with associated densities'''
    def __init__(self):
        self.matnum=0
        self.iso=[]
        self.iso_wtpt=[]
        self.iso_atpt=[]
        self.iso_name=[]
        







#  Utliitizes from Brian
def tritoncputimes(toutputfile):
    outtext = """
      Useage:
    
      python dancoffpp.py tritoncputimes.py outfile 
    
      where:
        'outfile' : The name of the TRIOTN output file
    
      General Info: This utility searches a TRITON output file for the CPU time
                    required for each module in the sequnce.  It sorts the CPU 
                    time for each module and prints the results with a percentage
                    of the total time required.  
    
      example:
    
      $python tritoncputimes.py cputimes 
    
        Module         Time       
      newt-omp     978.89  minutes (54.7%)
      centrm       340.25  minutes (19.0%)
      bonami       167.62  minutes (9.4%)
      worker       117.73  minutes (6.6%)
      pmc          114.15  minutes (6.4%)
      couple        28.79  minutes (1.6%)
      origen        27.07  minutes (1.5%)
      wax           15.79  minutes (0.9%)
      crawdad        0.12  minutes (0.0%)
      malocs         0.09  minutes (0.0%)
      opus           0.09  minutes (0.0%)  
      TOTAL:      1784.53  minutes 
    """
    
    
    def converttime(value,unit,tounit='minutes'):
        convertoseconds ={'seconds':1.0, 'minutes':1.0/60.0, 'hours':1/3600.0}
        convertominutes ={'seconds':1/60.0, 'minutes':1.0, 'hours':60.0}
        convertohours ={'seconds':1/3600.0, 'minutes':1/60.0, 'hours':1.0}
        if tounit == 'seconds': 
            return value*convertoseconds[unit]
        elif tounit == 'minutes': 
            return value*convertominutes[unit]
        elif tounit == 'hours': 
            return value*convertohours[unit]
      


    os.system('grep "\. cpu time used" {0}> cputimes'.format(toutputfile))
    
    toutput = open('./cputimes').readlines()
    
    os.system('rm cputimes')
    
    cputimedict = {}
    totaltimes = []
    
    for line in toutput:
          module = line.split()[1]
          val = float(line.split()[10])
          unit = line.split()[11].replace('.','')
          if module in cputimedict.keys(): 
                cputimedict[module].append(converttime(val,unit))
          else:
                cputimedict[module] = [converttime(val,unit)]
          
    for key in cputimedict.keys(): totaltimes.append([key, sum(cputimedict[key])])
    
    totaltimes = sorted(totaltimes, key=lambda tup: tup[1],reverse=True)
    grandtotal =  sum([pair[1] for pair in totaltimes])
    
    print
    print '  {0:^10} {1:^17}'.format('Module','Time')
    for pair in totaltimes: print '  {0:<10} {1:8.2f}  minutes ({2:>.1%})'.format(pair[0], pair[1],pair[1]/grandtotal)
    print '  {0:<10} {1:8.2f}  minutes '.format('TOTAL:', grandtotal)
    print











#   ****************             Data from mcnp output *******************
def mcnp_mass(MCNP_Output):
    '''  This gets data out of mcnp output
    
    '''
    try:
         output_file_old=open(MCNP_Output,'r')
    except IndexError:
        print "ERROR 1:  The command should read ]$ get_data_mcnp_output output file"

    
    results={}                                   
    for line in output_file_old:
        if 'cell  mat    density' in line:  # This is start of information
            loop=True
            output_file_old.next()
            while(loop):

    #           print line
    #           print input_file2
                newline=output_file_old.next()
                temp=newline.split()
                try:
                    results[int(temp[1])]=Cells()
                    results[int(temp[1])].mat    =temp[2]
                    results[int(temp[1])].rhoatm =float(temp[3])
                    results[int(temp[1])].rhogrm =float(temp[4])
                    results[int(temp[1])].vol    =float(temp[5])
                    results[int(temp[1])].mass   =float(temp[6])
                    results[int(temp[1])].pieces =int(temp[7])
                    results[int(temp[1])].nimp   =float(temp[8])
                except IndexError:
                    "Warning index error", temp
                    break
    output_file_old.close()
    print "results has attriubtes of .mat, .rhoatm, .rhogrm, .vol, .mass, .pieces, .nimp"
    return results
    
    
    
    
    
    
    



#   ****************             Write volume to mcnp *******************
def write_vol_2_mcnp(Input_file,Error_file,Result_file):
    # ******************************************
    # **********************  Enter data here
    # Input_file:  File adding to volume
    # Error_file: File that has the zeros showing no volumes this is an output
    # Result is the output after runing the volume solver
    
    
    PRINT_CELL_VOL=False
    LENGTH_CELL=5  # Length of the " cell" for getting cell data
    N=5
    
    # #####################    End of entering data ############
    #  First input should be name of file parsing
    try:
        input_file = open(Input_file, 'r')
        output_file=open(Result_file,'r')
    except IndexError:
        print "ERROR 1:  The command should read ]$ write_volume_2_mcnp.py [input.i] [error.out] [result.out]"
        sys.exit()
    new_file_name="%s.new_vol.i"%(Input_file)
    new_file=open(new_file_name,'w')
    
    
    
    results=mcnp_mass(Error_file)
    
    
    
    
    Max_error=0
    Max_cell=0
    # This gets the tally information from the output file by search for 1tally
    #    ************************************
    Skip_lines=5;    
    Multple_value=False
    Energy_bin,Total_flux,Multiply_tally=get_tally(Result_file,Multple_value,False)
    print "The len of the tallies are", len(Energy_bin), len(Total_flux), len(Multiply_tally)
    for i in Total_flux:
        print i
        results[i].new_vol=Total_flux[i].result
    
    print "These are the cells to have the volume replaced"
    print "Cell number,  new_volume[cm],   Relative error,   Absolute error[cm],  "
    
    #  Add volume card to every cell in the system
    for line in input_file:
        cell_num=line[0:5]  #This gets the first five lines of input which is cell number, surface, or material
    
        try:
            cell_num=int(cell_num)
            i=True  # This is for the while loop
            while i:
              if "imp:n=1" in line:
                   i=False
                   if results[cell_num].vol==0:
    
                       print "%i , %6.3E, %6.3E , %6.3E" %(cell_num,results[cell_num].new_vol, results[cell_num].new_vol_err,  results[cell_num].new_vol_err*results[cell_num].new_vol)
                       line=line.replace("imp:n=1", "imp:n=1 \n          vol=%.5E" %(results[cell_num].new_vol))
                       if Max_error<results[cell_num].new_vol_err:
                                Max_error=results[cell_num].new_vol_err
                                Max_cell=cell_num
                   else:
                       print "%i , %6.3E, %6.3E , %6.3E" %(cell_num,results[cell_num].new_vol, results[cell_num].vol,  (results[cell_num].vol-results[cell_num].new_vol)/results[cell_num].vol)
                   new_file.write(line)     
              else:
                   if "VOL" in line:
                       print "Removing volume"
                   else:
                       new_file.write(line)
                   line=input_file.next()
    
        except ValueError:
            new_file.write(line)
        except StopIteration:
            print "Process complete"
           
    print "Max_error for problem is ",Max_error, Max_cell
    input_file.close()
    output_file.close()







 #   ****************            get_cell surface num *******************
# This gets cell number and surface numbers from MCNP input
def get_cell_surface_num(File_name):
    try:
       input_file = open(File_name, 'r')
    except IndexError:
       print "ERROR 101:  The command should read ]$ get write_mcnp_tally.py [input.i] [mcnp.output] "
       sys.exit()    
   ##########    GEt cell data from output
    MCNP_cell={}
    surface_num=[]
    MCNP_mat={}
    Location=0  # Location based on blank lines
    Title=True  # Just to skip the title                                 
    for line in input_file:
        temp=line.split()
        if Title:
            print "Skipping the first three lines of the input incasee there is a message and title card"                 
            line=input_file.next()
            line=input_file.next()
            line=input_file.next()
            Title=False
         
        if not line.strip():
            Location=Location+1
            
        if Location==0:
            if 'c' not in line[0:5] and  line[0:5].strip() and 'C' not in line[0:5] :
                num=int(temp[0])
                material=int(temp[1])
                if material!=0:
                    rho=float(temp[2])
                else:
                    rho=0
                MCNP_cell[num]=Cells()
                MCNP_cell[num].mat=(material)
                if rho>0:
                    MCNP_cell[num].rhoatm=rho
                else:
                    MCNP_cell[num].rhogrm=-rho            
        if Location==1:
            if 'c' not in line[0:5] and  line[0:5].strip() and 'C' not in line[0:5] :
                surface_num.append(int(temp[0]))
        if Location==2:
            # Allows only the first line that has m and numbers and a space or two
            ok="m0123456789 "
            if('m' in line[0:5] and all(c in ok for c in line[0:5])):
                # Get mat number without the m
                mat_num=int((line[0:5].split('m'))[1])
                MCNP_mat[mat_num]=Material()
                MAT=True
                # Location of next material
                loc=1
                while(MAT):
                    #print mat_num
                    temp=line.split()
                    if 'm' in temp[0] and loc==0:
                        #print line
                        #print "exiting this material"
                        MAT=False
                    elif 'c' in line[0:5]:
                        #print line
                        #print "exiting this material"
                        MAT=False 
                    elif len(temp)==1:
                        loc=0
                        line=input_file.next()
                        temp=line.split
                    elif '$' in temp[loc]:
                        MAT=False                        
                    else:
                        #print temp
                        MCNP_mat[mat_num].iso.append(int(temp[loc].split('.')[0]))
                        if float(temp[loc+1])>0.0:
                            MCNP_mat[mat_num].iso_atpt.append(float(temp[loc+1]))
                        else:
                            MCNP_mat[mat_num].iso_wtpt.append(float(temp[loc+1]))
                        if len(temp)==loc+2:
                            loc=0
                            line=input_file.next()
                            temp=line.split()
                        
                        
                        else:
                            loc=loc+2
                        #raw_input('')
                        
   
    print ('Format has changed cells is now MCNP_cell object which has properites .mat .rhoatm .rhogrm')
    return(MCNP_cell,surface_num,MCNP_mat)











#   ****************            get_structure cell numbers *******************
# This gets cell number as they are listed in the input deck
def get_structure_cell(File_name):
    try:
       input_file = open(File_name, 'r')
    except IndexError:
       print "ERROR 101:  The command should read ]$ get write_mcnp_tally.py [input.i] [mcnp.output] "
       sys.exit()    
   ##########    GEt cell data from output
    MCNP_cell=[]
    Location=0  # Location based on blank lines
    Title=True  # Just to skip the title                                 
    
    for line in input_file:
        temp=line.split()
        if Title:
            print "Skipping the first three lines of the input incasee there is a message and title card"                 
            line=input_file.next()
            line=input_file.next()
            line=input_file.next()
            Title=False
         
        if not line.strip():
            Location=Location+1
            
        if Location==0:
            if 'c' not in line[0:5] and  line[0:5].strip() and 'C' not in line[0:5] :
                num=int(temp[0])
                MCNP_cell.append(num)
                       
    return(MCNP_cell)





































#   ****************             STOCHASTIC VOLUME *******************
def stoch_vol(File_name):
    
    #  **For stochastic volume have the VOID card in the problem
    #  **Set all nonzero imprtances to one and all positive weight windoes to zero
    #  **Use planar source with wource wheigth equal to the surface are to flood the geometry with particles
    #      inward-directed, biased cosine source on a spherical surface with weight equal to pi*r^2.153
    #  ** Use cell flux tally to tabulate volumes and the surface flux tally (F2) to tabulate areas.  The cell flux
    #        is inversly proportional to the cell volume 
    # 
    #TODO:  Need to place (1 so 500) at beginning of surphace card
    #TODO :  Need to have old imp:n=0 become 1 with a -1 added  and new void be  Last_cell_num 0  1   imp:n=0 
    #          IE:   9999 0  4018:199:-299   -1   imp:n=1
    #                 9998 0  1  imp:n=0  
    #TODO:   Need to replace kcode with the following     
    #               SDEF  SUR=1  NRM=-1  DIR=D1  WGT=3.14E6
    #               SB1   =-21  2
    #               NPS=1E10
    #
    
    
    
    print "2-190 Stochastic Volume and Area Calcuation"
    print "(1) Void out all material with VOID card  "
    print "(2) Set all nonzero importances to one and wieght windows to zero"
    print "(3) Use inward directed, biased cosine source on a spherical surface with weight equal to pi *r^2.153"
    print "(4) Use f4 to tabulate volume.  The cell is inversely proportional to cell volume."
    
    TEMP_FILE='Temp.txt'
    #  This how how many lines fortran reads for mcnp
    Start_tally=104
    Format_colum=4
    # Making sure format is okay
    try:
       input_file = open(File_name, 'r')
    except IndexError:
       print "ERROR 101:  The command should read ]$ get write_mcnp_tally.py [input.i] [mcnp.output] "
       sys.exit()

    output_name="%s.vol.inp"%(File_name)
    os.system('rm %s'%(output_name))
    output_file=open(output_name,'w')
   
   
    #  This gets the cell numbers and associated materials.
    cell_num,surface_num,material=get_cell_surface_num(File_name)        
        
    print ("\n WARNING:  All vol= cards need to be removed for this code to work properly")
    for line in input_file:
        if "kcode"  in line or "sdef" in line:
            output_file.write("VOID \n")
            output_file.write("sdef sur=1 nrm =-1 dir=d1 wgt=3.14159265359E6 \n") 
            print "Removing this line:  ",line,
            print "Replacing it with inward directed, biased cosine source on a spherical surface page 3-68 Example 3 "
            print(" \n NOTE:Surface 1 needs to be  1 so 1000")
            print(" \n NOTE: You also need to make imp:n=0 become the surface source 1 and everything else important.  ")
            raw_input(" \n NOTE: You also need to delete the tally for the void region")
            
            output_file.write("nps 4E10 \n")
            output_file.write("SB1 -21 2 \n")
            output_file.write("C %s"%(line))
        elif "vol=" in line:
            print "\n ERROR: ERROR:  Need to remove all vol= from code for this to work properly. Please retry after ready"
            sys.exit()
        elif "imp:n=1" in line:
            line=line.replace("imp:n=1", "imp:n=1 \n          vol=%.5E" %(1.0))
            output_file.write(line)
        else:    
            output_file.write(line)
    
    Reaction_rate=0;Material=0;Energy_tally=0
    Tally_type=["Flux"]
    Start=2
    output_file.close()
    new_cell=[]    
    for cell in cell_num:
        new_cell.append(cell)
    write_tally(Material, Energy_tally,new_cell,Reaction_rate, Tally_type,Start,output_name)  
    os.system('rm %s'%(output_name))
    







def averageOpus(averageFile,unit,File_name,scaleResult):
    #  averageFile is the name of the files to combine
    #  Unit is the unit combineing ie grams, watt, curies associated with the file
    #  File names  is the name of the file that the results should be saved to
    
    #  Open file to write to
    outputFile=open(File_name,'w')
    Result={}
    for CellNumber in averageFile:
        fileName='%s_%s.plt'%(CellNumber,unit)
        input_file=open(fileName,'r')
        
        # Save the isotope and result in a library for future use
        Result[CellNumber]={}
        Start=True
        for line in input_file:
            if Start:
                for i in range(6):
                    if i==1:
                        temp=line.split()
                        unitName='%s_%s'%(temp[0],temp[1])
                    if i==4:
                        temp=line.split()
                        TimeSteps=temp[0]
                        NumberIsotopes=temp[1]
                        line=input_file.next()
                    elif i==5:
                        Time=line.split()
                    else:
                        line=input_file.next()
                        
                Start=False
            else:
                temp=line.split()
                Result[CellNumber][temp[0]]=[]
                for i in (range(1,len(temp))):
                    Result[CellNumber][temp[0]].append(float(temp[i]))
    count=0
    for cell in Result:
        if count==0:
            CombinedResults=Result[cell]
            count=count+1
        else:
            for iso in Result[cell]:
                for value in range(len(Result[cell][iso])):
                    try:
                        CombinedResults[iso][value]=CombinedResults[iso][value]+Result[cell][iso][value]
                    #  This is if the isotopes are not found in either location.  
                    #  @TODO  improve this so that it will add all isotopes together and not leave some out
                    except KeyError:
                        if value==0:
                            print "NOTE: the following iso %s is not being used because it was not found in all files "%(iso)            
        for res in Result[cell]:
          input_file.close()
    
    print "  END of individual now averaging the values"
    

    
        
    
    #Change the dictionary into an array so I can sort high to low
    SortedResults=[]
    counter=0
    for iso in CombinedResults:
        #  Removes anything that decays away completely  
        if CombinedResults[iso][len(CombinedResults[iso])-1] !=0:
            #  Sort the value to be high to low
            SortedResults.append(iso)
            SortedResults[counter]=[]
            SortedResults[counter].append(iso)
            for value in CombinedResults[iso]:
                #  This is where I take the average and scale
                SortedResults[counter].append(value/len(averageFile)*scaleResult)
            
            counter=counter+1
    
    
    # Sort the array by cellnumber   
    printResults=sorted(SortedResults,key=lambda SortedResults: SortedResults[len(SortedResults)-1],reverse=True)       
    #  Print results
    #  Write out the unit_information and unit
    outputFile.write("%s  "%(unitName))
    for time in Time:
        outputFile.write("%s   "%(time))
    outputFile.write('\n')
    
    # Write out the values    
    for i in range(len(printResults)):
        for value in printResults[i]:
            outputFile.write("%s   "%(value))
            #print value,
        outputFile.write("\n")
    # Closing outputfile
    outputFile.close()


















 
def Opus_2_excell_last(output_file,cycle_number,ISO,counter,Desired_Cells):
    #output_file:  Name of the pointer to the opened file
    #  cycle_number:  Used to track multple cycles
    #  ISO desired isotopes
    #  counter:  counter so it doesn't repeat itself.  
    File_names=os.listdir('.')
    #print File_names
    

    
    
    
    Material_location=7
    #  Place time information on top
    FIRST=True
    Results={}
    for files in File_names:
        temp=files.split('_')

        if temp[0] in Desired_Cells:

            if ".plt" in files:
                input_file=open(files,'r')
                for line in input_file:
                    #  Get the information from the first four lines 
                    #  depletion material no. 612, opus case 1                                         
                    #    time (years)                                                                  
                    #  grams                                                                           
                    #  nuclide
                    #       7    41
                    for i in range(5):
                        if i==0:
                            material=line.split()[Material_location]
                            material=material.split(",")[0]
                            Results[material]={}
                            for iso in ISO:
                                Results[material][iso]=0
                                
                            
                        if i==4:
                            number_iso=int(line.split()[1])
                            number_days=int(line.split()[0])
                        
                        line=input_file.next()
                    if FIRST:
                        #  Print the time only once assuming same for all
                        print "For_time_in_days",line.split()[len(line.split())-1]
                        FIRST=False
                    for i in range(number_iso):
                        line=input_file.next()
                        
                       
                        for iso in ISO:
                            #  Only prints when the iso is in the line
                            if line.split()[0] == iso:
                                last_result=line.split()[len(line.split())-1]
                                #print "%s %s %s"%(material,iso,last_result)
                                Results[material][iso]=last_result
    
    
    #  Trying to sort the values
    sortedResults=sorted(Results.iteritems(),key=operator.itemgetter(1))
    
    if counter==0:
        output_file.write( "cycle_number   cells ")
        for iso in ISO:
            output_file.write("%s   "%(iso))
        output_file.write("\n")
    
    printResults=[]
    counter=0
    
    #Change the dictionary into an array for printablity
    for mat in Results:
        #print mat,
        first=True
        for iso in ISO:
            if Results[mat][iso]>0:
                if first:
                    #print mat, 
                    printResults.append(counter)
                    printResults[counter]=[]
                    printResults[counter].append(mat)
                    counter=counter+1
                    
                first=False
                printResults[counter-1].append(Results[mat][iso])
                #print Results[mat][iso],
            last_value=Results[mat][iso]
        #  Print new line only if it is a nonzero value
       
    
    # Sort the array by cellnumber   
    printResults=sorted(printResults,key=lambda printResults: printResults[0])       
    #  Print results
    for i in range(len(printResults)):
        output_file.write('%s   '%(cycle_number))
        for j in range(len(printResults[i])):
            output_file.write("%s   "%(printResults[i][j]))
        output_file.write("\n")
           
           
           
           
           
           
           
           
           
           
           
 
 
    
    
   
#  ================================ Plot Opus data ===========
def plot_opus(Total_Opus,Tolerence,ISO):
    ''' This takes a total array of opus information and plots it in excell readable format
    '''
    FILE_NAME='Opus_for_excell.inp' 
    #  Total_OPus =    Opus info from get_opus
    #  Tolerence = Tolerence of the cell
    #  ISO=List of iso desired to plot 
    #This is used if the ifo is greater then H-1
    if ISO[0]==0:
        PLOT_ISO=False
    else:
        PLOT_ISO=True
    
    
    os.system('rm %s'%(FILE_NAME))
    output_file=open(FILE_NAME,'w')    
    Isotopics={}
    #  This gets a library of all isotopics without repetting any
    output_file.write('Isotope\t')
    for cell in Total_Opus:
        output_file.write('%s\t'%(cell))
        for iso in Total_Opus[cell]:
            if Total_Opus[cell][iso]>Tolerence:
                Isotopics[iso]=0        
    output_file.write('\n')
      
    #This prints out the results for every isotopic in the desired list
    if PLOT_ISO:
        for iso in Isotopics:
            if iso in ISO:
                output_file.write("%s\t"%(iso))
                for cell in Total_Opus:
                    Cell=True
                    for new_iso in Total_Opus[cell]:
                        if new_iso==iso:
                            result=Total_Opus[cell][new_iso]
                            output_file.write("%s\t"%(result))
                            Cell=False
                    if Cell:
                        output_file.write("0.0\t")
                        
                        
                output_file.write('\n')
        print "Saved results in %s"%(FILE_NAME)          
    
    
    else:
        for iso in Isotopics:
            output_file.write("%s\t"%(iso))
            for cell in Total_Opus:
                Cell=True
                for new_iso in Total_Opus[cell]:
                    if new_iso==iso:
                        result=Total_Opus[cell][new_iso]
                        output_file.write("%s\t"%(result))
                        Cell=False
                if Cell:
                    output_file.write("0.0\t")
                    
                    
            output_file.write('\n')
        print "Saved results in %s"%(FILE_NAME)    


                    
    
   
 

 

#  ================================ Get Opus data ===========
def get_opus(Input_File,Day):                           
    """ This takes opus plt files and prints out one day information

    
    Input_File = name of the input file
    Day = day that material is wanted
    #  June 16,2012:  Made changes for OPUS-2_SQLITE which only has one line to read in.
    #"""
    
    
    input_file=open(Input_File,'r')
    # Save the isotope and result in a library for future use
    Result={}
    Start=True
    Found_day=False
    for line in input_file:
        if Start:
            for i in range(5):
                #print "%s"%(line)
                line=input_file.next()
            Start=False
            temp=line.split()
            for tmp in range(len(temp)):
                if Day=='First':
                    Found_day=True
                    Day_loc=1
                elif Day=='Last':
                    Found_day=True
                    #  This is the last location
                    Day_loc=len(temp)
                elif float(temp[tmp])==Day:
                    Found_day=True
                    # Location on array of Day
                    Day_loc=tmp+1
            if not Found_day:
                print "ERROR Day was not found",Day
                sys.exit()
            line=input_file.next()
            
        temp=line.split()
        #print Day_loc, len(temp)
        #print float(temp[Day_loc]),Day_loc
        try:
            Result[temp[0]]=float(temp[Day_loc])
        except IndexError:
            print "There is an indexx error which means there may be negative or not enough spacing between one answer and another"
    #for i in Result:
    #    print "%s\t%s"%(i, Result[i])
    #print "Returning opus data"
    input_file.close()
    # Result as a function of isotope
    return Result     
    

#  ================================ Get Opus data ===========
def get_all_opus(Input_File):                           
    """ This takes opus plt files and prints out one day information

    
    Input_File = name of the input file
    Day = day that material is wanted
    #  June 16,2012:  Made changes for OPUS-2_SQLITE which only has one line to read in.
    #"""
    
    
    input_file=open(Input_File,'r')
    # Save the isotope and result in a library for future use
    Result={}


     
    Material_location=7
    #  Place time information on top
    FIRST=True
     

    for line in input_file:
        #  Get the information from the first four lines 
        #  depletion material no. 612, opus case 1                                         
        #    time (years)                                                                  
        #  grams                                                                           
        #  nuclide
        #       7    41
        for i in range(5):
            if i==0:
                material=line.split()[Material_location]
                material=material.split(",")[0]
    
            if i==4:
                number_iso=int(line.split()[1])
                number_days=int(line.split()[0])
            
            line=input_file.next()
        if FIRST:
            #  Print the time only once assuming same for all
            print "time days",line,
            FIRST=False
        for i in range(number_iso):
            line=input_file.next()
            print material+line, 



#  ================================ Get Isotope data ===========
def get_isotope():
    """  This gets isotope information from data.txt found in /home/f4p/PYTHON_PATH/data.txt
    It uses this informaiton for addition work
    """
    from os.path import expanduser
    home = expanduser("~")
    DATA_FILE=home+'/PYTHON_PATH/data.txt'
    input_file=open(DATA_FILE,'r')
    
    # GET meta data too
    GET_META=False
    Results=[]
    count=0
    Start=False
    for line in input_file:
        if "Name" in line:
            Start=True
            line=input_file.next()
        if Start:
            temp=line.split()
            if len(temp)==5:
                Results.append(Data())
                Results[count].AAAZZZ=int(temp[2])
                Results[count].Na_me=temp[0]
                Results[count].Name=temp[1]
                Results[count].mass=float(temp[3])
                Results[count].nuclide_type=float((temp[4]))
                count=count+1

#    for res in range(len(Results)):
#        print Results[res].AAAZZZ ,Results[res].Na_me,Results[res].Name,Results[res].mass 
    #print "Returning isotopic data informaiton"
    input_file.close()
    return Results
    


#  ================================ Get Isotope data ===========
def origen_mat(Isotopes):
    """  This gets origen mat number (1 2 3) based on the isotopes that were provided
    """
    
    DATA_FILE='/home/f4p/PYTHON_PATH/origen_mat.txt'
    input_file=open(DATA_FILE,'r')
    
    # GET meta data too
    Mat=[]
    Iso={}
    for line in input_file:
        temp=line.split()
        Isotope=int(temp[0])/10
        Material=int(temp[1])
        Iso[Isotope]=Material

    for iso1 in Isotopes:
        Found=False 
        for iso2 in Iso:
            #print iso1, iso2
            if int(iso1)==int(iso2):
                Mat.append(Iso[int(iso1)])
                Found=True
        if not Found:
            print "Warning could not find iso %s setting equalto 3"%(iso1)
            Mat.append(3)
            print iso1
            #raw_input('Enter to contine')
    return Mat






# ================================ Opus to SCALE ===========================
def Opus_2_scale(Opus_data,Material_num,Tolerance,output_file):
    '''  This takes opus plot data and converst it to scale data
      Opus data == Opus data from get_opus
      material_num == number you want the material file to be written to
      Tolerance is the tollerence of the saved materials
    '''     

    

    # Get iso data
    Iso_data=get_isotope()
    
    #  This creates material information for SCALE
    material={}
    Total=0    
    for iso in Opus_data:
        # Only get data above tolereance
        if Opus_data[iso]>Tolerance:
            Found=False
            for res in range(len(Iso_data)):
                if iso==Iso_data[res].Name:
                    #  Save mass as a function of the isotope name
                    #material[Iso_data[res].Na_me]=Opus_data[iso]
                    material[Iso_data[res].AAAZZZ]=Opus_data[iso]
                    Found=True
            if iso=='total':
                #Obtaines the total information
                print "The Total should be %s" %Opus_data[iso]
                Total=Opus_data[iso]
                Found=True 
                # If it can not find the isotope it might be a metastable if it has an m in it
            if not Found:
                print "ERROR the following was not found %s %s"%(iso, Opus_data[iso])
                if "m" in iso:
                    print "It must be a metastable"
                else:
                    sys.exit()
    
        
    # Summing the material information
    total=0
    # Adds the total with the tollerence information
    for iso in material:
        total=total+material[iso]
    
    #  Compares the total with the tollerence.  
    print "The total sum is", total   
    if Total-total>.5:
        print "Error:Error tollerence is to high your are missing %s grams of mass"%(Total-total) 
        sys.exit()
    
    #Normaizing material to one
    #for iso in material:
    #    material[iso]=material[iso]/total
        #print iso, material[iso]
    # Sort the vales from largest to smallest

    #for iso in material:
        #print "%6s          %5i 0  %.5E   293.600   end"%(iso, Material_num,material[iso])
    
    # Normalize to 100%
    for iso in material:
        material[iso]=material[iso]/total*100
   
    Sorted_mat= sorted(material.items(), key=itemgetter(1),reverse=True)
    output_file.write( "wtpt%s    %s    roth=%.4E  \n"%(Material_num,Material_num,Total))
    for iso in Sorted_mat:
        output_file.write( "   %8s     %.4E\n"%(iso[0],iso[1]))    
    output_file.write( "                293.600   END\n")    
    
    return(Sorted_mat)
    










 



#  ========================= Opus to MCNP ==============
def opus_2_mcnp(Opus_data,Tolerance):
    '''  This takes opus plot data and converst it to mcnp material data
      Opus data == Opus data from get_opus
      material_num == number you want the material file to be written to
    '''     

    #Tolerance for how many materials to include into mcnp input file
    #  This is the list of actinides that can be ignored
    ACTINIDES=[92234, 92235, 92236,92237,92238,93236,93237,93238,93239,94238,94239,94240,94241,94242,95241,95242,95243,96243,96244,96245,96246]    
    #Save material file
    MISSING_ISOTOPES=['hf175','hf181', 'c14','hf182' ,'sr91', 'y93','zr97', 'i133','cr51','fe55','ni63','ta183','tm171','yb171','tb158','yb170','tm170', 'mn54','tm169','tm168','yb168','tb157','sr92','y92','nb97','ru101','pd109','pd112','sb127','sb128','sb129','te127','te128','i132','i134','ba139','la141','la142','pr145','np240','kr88','te134','cs138','nd149','pm150']



    # Get iso data
    Iso_data=get_isotope()
    #for i in Opus_data:
    #    print "%s\t%s"%(i, Opus_data[i])
    #for res in range(len(Iso_data)):
    #    print Iso_data[res].AAAZZZ ,Iso_data[res].Na_me,Iso_data[res].Name,Iso_data[res].mass
    #  This creates material information for mcnp
    material={}
    Total=0    
    for iso in Opus_data:
        #print iso.type()
        # Only get data above tolereance
        if Opus_data[iso]>Tolerance:
            if iso not in MISSING_ISOTOPES :
                Found=False
                for res in range(len(Iso_data)):
                    if iso==Iso_data[res].Name:
                        material[Iso_data[res].AAAZZZ]=Opus_data[iso]
                        Found=True
                if iso=='total':
                    print "The Total should be %s" %Opus_data[iso]
                    Total=Opus_data[iso]
                    Found=True
                if not Found:
                    print "ERROR the following was not found %s %s"%(iso, Opus_data[iso])
                    if "m" in iso:
                        print "It must be a metastable"
                    else:
                        sys.exit()
            else:
                print "the following isotope is not in MCNP: ",iso
                
        
    # Summing the material information
    total=0
    countFP=0
    countActinide=0
    for iso in material:
        #print iso
        total=total+material[iso]
        if iso not in ACTINIDES:
            countFP=countFP+1
        else:
            countActinide=countActinide+1
    #print countFP, countActinide
    #  Get the amount of mass that is missing
    missing=Total-total
    
    
    print "The total sum is", total   
 
    #  Tollerence .1% to prevent further error
    if abs(missing)/Total>.001:
        print "Error:Error tollerence is to high your are missing %s grams of mass"%(Total-total) 
        sys.exit()
    #Normaizing material to one

    #  Here normalizing the fission products to one while keeping the actinides the same.  Its the fission products that are missing. 
    #  normalization
    if missing>0.000 and countActinide>0:   #  This is to privent having negative material and duing correction on non fissionable materials like hf
        for iso in material:
            if iso not in ACTINIDES:
                #print iso ," ", material[iso],"  ",
                material[iso]=material[iso]+missing/countFP
                #print material[iso]
                
        # Normalize to one        
    for iso in material:
        material[iso]=material[iso]/Total
        
        

    # Sort the vales from largest to smallest
    Sorted_mat= sorted(material.items(), key=itemgetter(1),reverse=True)

    
    return(Sorted_mat)
    


        
   
   
   
    


def stdcmp_2_mcnp(STDCMP_NAME,MCNP_FILE):
    '''This takes STDCMP file information and converts it to mcnp material data
       This will also plot the information for each time step
    '''
    
    STDCMP_File=open(STDCMP_NAME,'r')
    MCNP_Output=open(MCNP_FILE,'w')
    
    Mixture={}
    Total=0
    #  This creates an array of material objects
    #  objects include .matnum, .iso, .iso_wtpt, .iso_atpt
    for line in STDCMP_File:
        temp=line.split()
        if 'days' in line:
            for i in range(len(temp)):
                if "mixture" == temp[i]:
                    mixture=int(temp[i+1])
                elif 't=' == temp[i]:
                    time=temp[i+1]
                    time_unit=temp[i+2]
            Mixture[mixture]=Material()
        else:
            iso_name=temp[0]
            iso_atpt=temp[3]
            Mixture[mixture].iso_name.append(iso_name)
            Mixture[mixture].iso_atpt.append(float(iso_atpt))
    
    #  Debug option
    print mixture, time, time_unit #, #Mixture      
    
    # This gets iso data for converting letters to numbers and also atomic mass to density
    # Iso_data is a class with .AAAZZZ, .Na_me, .Name, .mass, .nuclide_type
    Iso_data=get_isotope()         
    


    Total=0
 
    for mix in Mixture:
        for iso in Mixture[mix].iso_name:
            Found=False   
            #  This goes through every isotope and looks for the name
            for res in range(len(Iso_data)):
                #print iso,Iso_data[res].Na_me
                if iso==Iso_data[res].Na_me:
                    #print mix, Iso_data[res].AAAZZZ 
                    Mixture[mix].iso.append(Iso_data[res].AAAZZZ)
                    #Saves the Wtpt for the same location
                    Wtpt=Mixture[mix].iso_atpt[len(Mixture[mix].iso)-1] / .60233 * Iso_data[res].mass
                    Mixture[mix].iso_wtpt.append(Wtpt)
 
                    Found=True
            if not Found:
                print "ERROR the following was not found %s "%(iso)
                if "m" in iso:
                    print "It must be a metastable"
                else:
                    sys.exit()
    
    #  This is a list of items not in MCNP or of tolerence is to low
    Missing=[72175,72181,6014,72182,4007,98253,99253]
    TOLERENCE=1E-7
    #  This prints out the material
    for mix in Mixture:
        Density=0
        MCNP_Output.write( "c    For mixture  %s   \n"%(mix))
        MCNP_Output.write( "m%s  \n"%(mix))
        Sorted=[]
        # Creates a double array for simplificaiton when sorting the information
        for i in range(len(Mixture[mix].iso)):
            
            if Mixture[mix].iso[i] not in Missing:
                if Mixture[mix].iso_wtpt[i]>TOLERENCE:
                    Sorted.append([Mixture[mix].iso[i],Mixture[mix].iso_wtpt[i]])
        
        Sorted=sorted(Sorted,key=itemgetter(1),reverse=True)
        for i in range(len(Sorted)):
            Density=Density+Sorted[i][1]
            MCNP_Output.write( "        %6i.70c   %.4E \n"%(Sorted[i][0],-Sorted[i][1]))     
        MCNP_Output.write( "c Density is %.4E  \n"%(Density))        
    print "\n\n ***Writing mcnp output file",MCNP_Output
    
    
    #  Closes the MCNP material file
    MCNP_Output.close()
    return Mixture 
    # Mixture.iso, iso_wtpt, iso_atp        
       
         

def write_csasmg(output_file,crossSection,isotopes,density, fractionIsotopes,temperature,buckledHeight, outsideRadius):
    #output_file  file to be saved at  
    #crossSection = 'v7-238'
    #  isotopes  = isotopes used in the problem
    #  fractionIsotopes = fraction of isotopes in problem
    #  density of the material in the problem
    #  temperature of the problem
    #  BuckledHeight  length of a finite cyclinder
    #  outsideRadius:  Outside radius of the zone  
    
                                                                    
    output_file.write("=csas-mg parm=(centrm,adnu=4)                                \n")
    output_file.write(" csasmg generated from m2s.write                             \n")
    output_file.write("%s                                                       \n" %(crossSection))
    output_file.write("read composition                                             \n")
    output_file.write("'                                                            \n")
    output_file.write("' Material generated with write_casamg in m2s.py write_csasmg      \n")
    output_file.write("wtptfuel 1  %s  %s  "%(density, len(isotopes)))
    for i in range(len(isotopes)):
        #"u-236 1 den=10.40  .0000428 500 end                         
        output_file.write("  %s  %s                            \n"%(isotopes[i],fractionIsotopes[i]))
    output_file.write(" 1.0  %s   END "%(temperature))  
    output_file.write("end composition                                              \n")
    output_file.write("read celldata                                                \n")
    output_file.write("multiregion buckledcyl left_bdy=reflected right_bdy=vacuum   \n")
    output_file.write("    origin=0.0 dy=%s end                                  \n"%(buckledHeight))
    output_file.write("    1 %s end zone                                         \n"%(outsideRadius))
    output_file.write("end celldata                                                 \n")
    output_file.write("end                                                          \n")





# ==================================WRITE COUPLE====================================================
def write_couple_csas(Energy_tally,Multiply_tally,cell_num,WEIGHT_GROUP,FISSION,output_file,UPDATE_CROSS,DESIRED_MATERIAL,REACTION,START_NUM,CSAS_REGION):

          
    FORMAT_ROW=4
    
    if WEIGHT_GROUP==49:
        CROSS=77
    elif WEIGHT_GROUP==200:
        CROSS=78
    elif WEIGHT_GROUP==44:
        CROSS=79
    elif WEIGHT_GROUP==238:
        CROSS=80  


    
    if len(FISSION)>1:
        NFISW=len(FISSION)
    else:
        NFISW=0
    
    print FISSION,len(FISSION),NFISW
    #raw_input()
        
    output_file.write('=couple \n\n')
    

    output_file.write('0$$ a3 {JD} a4 {ND} a5{LD} a6 {MD} e \n'.format(JD=CROSS, ND=21,LD=4, MD=33))
    # 0$$ array
    # a3. JD  AMPX neutron  =77, 49-group 78, 200-group 79, 44-group 80, 238-group                                                                                                                                                                                                                                                                                                                                                      
    # a4. ND  Input ORIGEN binary library {if LBIN = 0} (21).                                                                                                                                                                                                                                                                                                                                                                           
    # a6. MD  Output ORIGEN binary library (33).                                                                                                                                                                                                                                                                                                                                                                                        
    # e   : always needed                                                                                                                                                                                                                                                                                                                                                                                                                
    #  DEBUG JOSH PETERSON    
    
    
    
    
    
    output_file.write('1$$ a3 {LBUP} a4 {JADD} a5 {JEDT} a10 {IDENT} a11 {NEWID} a12 {IDREF} a13 {NZONE}\n     \
     a15 {NFISW} a16 {NUMA} a17 {NORM} a18 {NWGT} e t \n'.format
        (LBUP=UPDATE_CROSS, JADD=1, JEDT=0, IDENT=0, NEWID=9022, IDREF=0, NZONE=CSAS_REGION, NFISW=NFISW, NUMA=8, NORM=0, NWGT=WEIGHT_GROUP))
    # output_file.write('0$$ a3 {JD} a4 {ND} a6 {MD} e \n'.format(JD=80, ND=21, MD=33))    
    # 1$$  Array  Control Constants [19 entries].                                                                                                                                                                                                                                                                                                                                                                                       
    # a3.  LBUP  1/0  Update from user input cross sections (Data Block 8) / no user update (0).                                                                                                                                                                                                                                                                                                                                       
    # a4.  JADD  1/0  Add/do not add new transitions to the library (1).                                                                                                                                                                                                                                                                                                                                                               
    # a5.  JEDT  1/0  Edit input library only/normal library generation case (0).                                                                                                                                                                                                                                                                                                                                                      
    # a10  IDENT  ID number of weighted AMPX library (0).                                                                                                                                                                                                                                                                                                                                                                               
    # a11  NEWID  Updated library ID number (0).                                                                                                                                                                                                                                                                                                                                                                                        
    # a12. IDREF  Nuclide ID number of the isotope in AMPX library on unit LD that contains the neutron flux weighting spectrum to be used to collapse multigroup cross sections. If 0, code uses flux from first isotope in weighted AMPX library, which is usually the zone flux                                                                                                                                    
    # a13  NZONE  The zone of the nuclides with which to add/update the library. Used for library                                                                                                                                                                                                                                                                                                                     
    # a15  NFISW  Number of fissile nuclides 1, all 30 fissionable N nuclides defined in 7$ array                                                                                                                                                                                                                                                                                                                                      
    # a16  NUMA  Number of title lines from teh start of the input library prologue to be retained in the ouput library porlouge                                                                                                                                                                                                                                                                                                         
    # a17 NORM  Cross section normalization -1/0/N  thermal flux/ total flux/ cross section N/                                                                                                                                                                                                                                                                                                                                           
    # a18 NWGT  For defining source of weighting flux spectrum data (0)  1, generate weighting spectrum using 2* array parameters  0, obtain flux from AMPX library on unit LD, nuclide IDREF N, user-defined N group weight spectrum input in 9* array NOTE: must be consitstant with 0$ a3.                                                                                                                                          
    # e    always needed                                                                                                                                                                                                                                                                                                                                                                                                                 
    # t    always needed  Data Block 1 terminator.  



    output_file.write('\'   ********  Start of Block 2   flux spectrum  fission yield  ************                %  \n')                                                                       
    print len(FISSION)
    if NFISW!=0:
        #  7$$ Nuclide ID numbers for nuclides with fission yields [1$-a15]. 
        count=0
        output_file.write('7$$   ')
        for fiss in FISSION:
            count=count+1
            output_file.write('%i  '%(fiss))
            if count%7==0:                   
                output_file.write('\n       ')
        output_file.write('\n\n') 
     
    

                
    #  9** Array  User input weighting function [$1-a18].
    #  Get the needed weighting function
    if WEIGHT_GROUP>0:
        Energy=[]
    
        output_file.write('\n9**   ')
    
        for tal in range(len(Energy_tally[cell_num].energy_tally)):
            Energy.append(Energy_tally[cell_num].energy_tally[tal])
        count=0
        for flux in reversed(Energy):
            count=count+1
            output_file.write('%7E   '%(flux))
            #print i, flux
            if count%FORMAT_ROW==FORMAT_ROW-1:
                output_file.write('\n      ')
        output_file.write(' e     t \n')
    
    
    #  @TODO  Need to update cross section also
    START_MAT=[]
    END_MAT=[]
    if UPDATE_CROSS:
        
 
        # This creates a cross section file for couple
        Cross_section=[]
        # Multiply_tally has the objects .mult_cell, .mult_mat, .mult_value, .mult_reaction, ,multi_micro=[] "
        for tally_num in Multiply_tally:
            for i in range(len(Multiply_tally[tally_num].mult_cell)):
                Multi_cell_num=Multiply_tally[tally_num].mult_cell[i]
                if Multi_cell_num==cell_num:
                   Cross_section.append(Multiply_tally[tally_num].multi_micro[i])
                   Material=DESIRED_MATERIAL[Multiply_tally[tally_num].mult_mat[i]-START_NUM]
                   Reaction=Multiply_tally[tally_num].mult_reaction[i]
                   #print DESIRED_MATERIAL[Multiply_tally[tally_num].mult_mat[i]-START_NUM]
                   # If fission then the first one is negative and the daughter is positive
                   if Reaction==18:
                       START_MAT.append("-%i0"%(Material))
                   else:
                       START_MAT.append("%i0"%(Material))
                   
                   if Reaction==102:
                       END_MAT.append("%i0"%(Material+1)) 
                   elif Reaction==18:
                       END_MAT.append("%i0"%(Material))                   
                   else:
                        print "ERROR: ERROR:  NOT INFORMAITON FOR CROSS SECTION:  EXITING"
                        sys.exit()      
        
        #  Removal all results that have zero for the cross section
        pop=[]
        for i in range(len(Cross_section)):
            if Cross_section[i]==0:
                print "Removeing croos section for %s to reaction %s because it was zero"%(START_MAT[i] ,END_MAT[i])
                pop.append(i)
        #print pop, len(Cross_section),Cross_section
        for i in range(len(pop)-1,-1,-1):
            #print pop[i],i
            Cross_section.pop(pop[i])
            START_MAT.pop(pop[i])
            END_MAT.pop(pop[i])
        #print Cross_section
        
        
        output_file.write(' \n\' ********* Start of Data Block 6 number of reaction rates NOTE:  required if 1$-a3 = 1} ****  \n')
    
        # '  NOTE:  required if 1$-a3 or LBUP = 1}. 
    
        # LBU  Total number of nuclide reaction cross sections to be entered (0).                                                                                      
        DESIRED_MATERIAL
        output_file.write('15$$ {LBU} T \n'.format(LBU=len(START_MAT)))
        output_file.write( '\'   **************   Data Block 8  Reaction rate    *************       % \n')
        output_file.write('71$$ ')
        for mat in range(len(START_MAT)):
            output_file.write(" %s "%(START_MAT[mat]))
            if mat%FORMAT_ROW-1==0:
                output_file.write("\n      ")

        output_file.write('\n72$$ ')
        for mat in range(len(END_MAT)):
            output_file.write(" %s "%(END_MAT[mat]))
            if mat%FORMAT_ROW-1==0:
                output_file.write("\n      ")                    

        output_file.write('\n73**  ')
        for mat in range(len(Cross_section)):
            output_file.write(" %s "%(Cross_section[mat]))
            if mat%FORMAT_ROW-1==0:
                output_file.write("\n      ")                    

        output_file.write('\nT\n')
    output_file.write('done \n')
    output_file.write('end \n')
    






# ==================================WRITE OPUS==================================================== 
def write_opus(MINPOSITION, MAXPOSITION,unit,output_file,opus_counter,cell_num,LIBUNIT):
    #  Writing opus to print out hte results in the format I want  
    # MIN
    # MAX
    # UNIT
    # OUTPUT_FILE
    # OPUS_COUNTER
    #CELL_NUM
    #LIBUNIT
    if unit=='GSPECTRUM'or unit=='NSPECTRUM':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=%s \n'%(unit))
        output_file.write('UNITS=PARTICLES \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n\n')
        output_file.write('=shell \n')
        output_file.write('  cp _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')         
    
    
    else:
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('NRANK=500 \n')
        
        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]    
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n\n')
        output_file.write('=shell \n')
        output_file.write('  cp _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n') 
    opus_counter=opus_counter+1
    return(opus_counter)
    

# ==================================WRITE OPUS==================================================== 
def write_opus_ft71(MINPOSITION, MAXPOSITION,unit,output_file,opus_counter,cell_num,LIBUNIT,SAVED_RESULTS):
    #  Writing opus to print out hte results in the format I want  
    # MIN
    # MAX
    # UNIT
    # OUTPUT_FILE
    # OPUS_COUNTER
    #CELL_NUM
    #LIBUNIT
    if unit=='GSPECTRUM'or unit=='NSPECTRUM':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=%s \n'%(unit))
        output_file.write('UNITS=PARTICLES \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n\n')
        output_file.write('=shell \n')
        output_file.write('  cp _plot*000%i %s/%s_%s.plt \n'%(opus_counter,SAVED_RESULTS,cell_num,unit))
        output_file.write('end \n')         
    
    
    else:
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('NRANK=500 \n')
        
        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]    
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n\n')
        output_file.write('=shell \n')
        output_file.write('  cp _plot*000%i %s/%s_%s.plt \n'%(opus_counter,SAVED_RESULTS,cell_num,unit))
        output_file.write('end \n') 
    opus_counter=opus_counter+1
    return(opus_counter)    

  
  
  

# ============================================== WRITES ARP INFORMATION
def write_arp(output_file,lib_name,initenr,num_cycle,irr_time,average_pow,num_lib,mod_den):
   '''
   This code create an arp input deck similar to that of the windows GUI ORIGEN-ARP
   
   
   **Input descrption:**
   
   
      * output_file:  The file that the arp library will be writen too    
      * lib_name:  The name of the library the will be used for the arp run     
      * initenr:  The initial enrichment of the fuel      
      * num_cycle: The number of cycles, a set of interpolated corss section is created for each cycle   
      * irr_time:  The irradation time for each cycle in days         
      * average_pow: The fission power (MW/MTIHM) for each cycle: One per cycle    
      * num_lib:  Number of libraries per each cycle     
      * mod_den:  Moderator density g/cm3               
   '''                                                              
   # A check
   if len(irr_time) !=num_cycle or len(average_pow) !=num_cycle  or len(num_lib)!=num_cycle:
       print "ERROR 780: Number of cycles not equal to irradation times",len(irr_time),len(average_pow),len(num_lib),num_cycle
       sys.exit()
   
   #if num_cycle>1:
   #    print "ERROR,ERROR, number of cycles greater then one so you must create ORIGENS input deck to reflect that change ARP infor to only have one number of cycles"
   #    print "Need additonal work before this is supported"
   #    sys.exit()
   # Witing opus library:  See page D1.3.5 in Scale manual for better understanding
   output_file.write("=arp     \n")
   output_file.write("%s  \n"%(lib_name))
   output_file.write("%.4E      \n"%(initenr))
   output_file.write("%i        \n"%(num_cycle))
   for time in irr_time:
       output_file.write("%.4E \n"%(time))
   for pow in average_pow:
       output_file.write("%.4E       \n"%(pow))
   for lib in num_lib:
       output_file.write("%i        \n"%(lib))
   output_file.write("%.4E   \n"%(mod_den))
   output_file.write("ft33f001 \n")
   output_file.write("end      \n")
       




# ==================================WRITE ORIGIN====================================================
def write_origen_short(USE_FT33,DECAY_STEPS,IRRADIATE,FORMAT_ROW,TITLE,UNITS,IRRADIATION, \
              DECAY,FINAL_DECAY,MIX_NUM,output_file,Isotopes,Frac,Mat,FISSION,FLUX,Power_instead_Flux):
    '''  #
    Code: write_origin_short.py
    
    Author:  Joshua Peterson
       
    Date:    Writes origen but uses the least amount of memory possible and only saves the end of irradation and end of calcuation on the ft71f001 file
    
 
    
    **Description of input:** 
    
       * USE_FT33= if you want to use an existing ft33 file
       * DECAY_STEPS number of decay steps
       * IRRADIATE  number of irradation steps
       * FORMAT_ROW number of rows per collum
       * TITLE    title used in the title card
       * UNITS    units you want to use
       * IRRADIATION days of irradation history
       * DECAY     days of decay history
       * FINAL_DECAY  final breakdown of decay history **NOTE**  This can be either as an array or a int/float use int/float if you dont care how it is broken up you just have a final time of decay.
       * MIX_NUM      (Mixture number used to copy over the ft33f001.mixNUM file.  If you use the word **'UNUSED'** Then it will assume the ft33f001 is allready generated in the temp directory.
       * output_file  output file to be writen
       * Isotopes     isotopes that used
       * Frac         fraction of the isotopes
       * Mat          type of isotope 1 for activation prodcuts 2 actinde 3 fission products 
       * FISSION      which fission products you want to include for irradation
       * NFISW       number of fission products you are including
       * FLUX        flux vector for each irradation 
       * Power_instead_Flux **This is a new one**. True means use Power False means use Flux 
    '''

    # Number of isotopes used
    FACTOR=1.351
    NUM_ISO=len(Isotopes)   
    NFISW=len(FISSION) # Number of fission enteries above 




    #  Moving the ft33f001 file to the correct location
    if USE_FT33:
        if MIX_NUM=='UNUSED':
            temp=1
           #print "Assuming ft33f001 is allready generated"
        else:
           output_file.write('=shell \n')
           output_file.write('cp $INPDIR/ft33f001.%s ft33f001 \n'%(MIX_NUM))
           output_file.write('end\n')
                                                                                                                                      
    #  INITALIZING INFORMATIOn
    time=[]
    decay_time=[]
    decay_time.append(0)
    count=0
    for irr in range(len(IRRADIATION)):
        # time is the time for irradation
        time.append(count)
        #  Here is a counter to keep it sequental
        count=IRRADIATION[irr]+count
        #  Here is a sequential for decay information
        decay_time.append(count)
        #  This addes decay plus the irradation to keep information straight
        count=DECAY[irr]+count
    
    
    output_file.write('=origens \n')
    output_file.write('0$$ a4 33 a11 71 e t \n') 
    TIME=0
    #  It increments over irradation.  
    #  NOTE:  the length of irradation needs to be the same as Decay
    if len(IRRADIATION) !=len(DECAY) or len(IRRADIATION) !=len(FLUX):
        print "ERROR ERROR Len of irradation needs to be length of decay and flux", len(IRRADIATION), len(DECAY),len(FLUX)
        print ("Len irr %s decay%s flux %s"%(len(IRRADIATION), len(DECAY), len(FLUX)))
        sys.exit()
    for irr in range(len(IRRADIATION)):  
           output_file.write('%s \n' %(TITLE))
           #  NOTE in second loop A16 is not there
           if irr==0:
                output_file.write('3$$ 33 a3 %i a4 0 a16 2 a33 0 e t \n'%(1))  
           else:
                #  IF USE_FT33 is true then incrementally use the ft33f001 file from Trition
                if USE_FT33:
                    output_file.write('3$$ 33 a3 %i a4 0 a16 2 a33 0 e t \n'%(irr))  
                else:
                    output_file.write('3$$ 33 a3 %i a4 0 a16 2 a33 0 e t \n'%(1))  
           output_file.write('35$$ 0 t \n')
           #  For irr=0 the number of isotopes are written here.  After that isotopes are not inputed
           if Power_instead_Flux:
              if irr==0:
                   output_file.write('56$$ %s %s a3 0 a6 1 a10 0 a13 %s a15 3 a18 0 e \n'%(IRRADIATE,IRRADIATE,NUM_ISO))  #a3 is for flux being read in
              else:
                  output_file.write('56$$ %s %s a3 0 a6 1 a10 1 a15 3 a18 0 e \n'%(IRRADIATE,IRRADIATE))# a10 1 a13 not there 
           else:
               if irr==0:
                    output_file.write('56$$ %s %s a3 1 a6 1 a10 0 a13 %s a15 3 a18 0 e \n'%(IRRADIATE,IRRADIATE,NUM_ISO))  #a3 is for flux being read in
               else:
                   output_file.write('56$$ %s %s a3 1 a6 1 a10 1 a15 3 a18 0 e \n'%(IRRADIATE,IRRADIATE))# a10 1 a13 not there 
           #This is where the initall time from the previous run is used.  So the output is nice looking
           output_file.write('57** %10.6f a3 1e-05  e \n'%(TIME))#time[i]))  #used to get better results
           output_file.write('95$$ 1 t \n')
           #  Input stuff into the comment line
           output_file.write('Cycle %i %s \n' %(irr+1,TITLE))

           # Writing out average power instead of flux
           if Power_instead_Flux:
               #  Writeing the flux out which is a function of burnup
               output_file.write('Power used for this cycle is %.3E MW \n'%(FLUX[irr]))
               output_file.write('58** ')

           else:
               output_file.write('Flux used for this cycle is %.3E n/cm2/s \n'%(FLUX[irr]))
               #  Writeing the flux out which is a function of burnup
               output_file.write('59** ')
           for tm in range(IRRADIATE):
               output_file.write(' %.3E '%(FLUX[irr]))
               if tm%FORMAT_ROW==FORMAT_ROW-1:
                   output_file.write('\n     ')
           #  Writing out the irradation time.  This is made to allow a range of irradation time
           output_file.write('\n60**  ')
           Count_time=TIME 
           #  breaks up to number of irradationation steps
           for t in range(IRRADIATE):
               #Count_time=Count_time+IRRADIATION[irr]/float(IRRADIATE)
               # Small steps  
               New_Count_time=Count_time+(IRRADIATION[irr]/FACTOR**(float(IRRADIATE)))*FACTOR**(t+1)
               output_file.write(' %10.6E'%(New_Count_time))
               # adds a return caracter to prevent for going pased speficied limit
               if t%FORMAT_ROW==FORMAT_ROW-1:
                    output_file.write('\n       ')

           output_file.write( ' \n')
           #  This is where the Time is set to the very last previous time step
           TIME=New_Count_time
           #output_file.write('66$$ a1 0 a5 0 a9 0 e \n')
           if irr==0:
                #  For the first step outputs the material inforamtion specified above
                #output_file.write(ISOTOPES) #ISOTOPE
                #output_file.write(FRACTION) # Fraction
                #output_file.write(MATERIAL) # Material
                output_file.write('\n73$$  ')
                for i in Isotopes:
                    output_file.write('\t%s0'%(i))
                    if Isotopes.index(i)%FORMAT_ROW==FORMAT_ROW-1:
                        output_file.write('\n      ')
                    #ISOTOPES='73$$ 721740 721760   \n 721770 721780 721790 721800 \n' 
                output_file.write('\n74**  ')
                count_Frac=0
                for i in Frac:
                    output_file.write('\t%.5E'%(i))
                    if count_Frac%FORMAT_ROW==FORMAT_ROW-1:
                        output_file.write('\n      ')
                    count_Frac=count_Frac+1
                
                    #FRACTION='74** .16E-2 5.26E-2  18.60E-2 \n 27.28E-2  13.92E-2 35.08E-2  \n'
                output_file.write('\n75$$  ')
                count_Mat=0
                for i in Mat:
                    output_file.write('\t%s '%(i))
                    if count_Mat%FORMAT_ROW==FORMAT_ROW-1:
                        output_file.write('\n      ')
                    count_Mat=count_Mat+1
                    #MATERIAL='75$$ 1 1 1 1 1 1 \n'
        
        
        
        
                
                
                
           output_file.write('t \n')
           #  For saving the irradation information
           # IRRADIATE
           #for step in range(IRRADIATE): 
           #    output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
           #  Decaying now
           if irr==len(IRRADIATION)-1:
               # Saving the last ft71f001 file 
               output_file.write('56$$  0 0 a10 %i e t \n'%(IRRADIATE))

           
           
           output_file.write('54$$ a8 1 a11 0  e \n')
           output_file.write('56$$ a2 %s a6 1 a10 10 a15 3 a17 1 e \n'%(DECAY_STEPS))
           #  This writes the next time incrementally
           output_file.write('57** %10.6f a3 1e-05 e \n'%(TIME))     
           output_file.write('95$$ 0 t \n')
           output_file.write('Decay %i %s for flux %s \n' %(irr+1,TITLE,FLUX[irr]))
           output_file.write('Decay for experiment \n')
           output_file.write('60**  ')
           Count_time=TIME
           #  Doing a intremental step to specified decay with the number of steps being DECAY steps
           for t in range(DECAY_STEPS):
               #  if it is the last decay step
               if irr ==len(IRRADIATION)-1:
                   #  This is if the user just specifies the final decay or how the decay is broken up
                   if type(FINAL_DECAY)==int or type(FINAL_DECAY)==float:
                       #break it up evenly 
                       # break it up logrithmitacllly
                       New_Count_time=Count_time+FINAL_DECAY**((t+1)/float(DECAY_STEPS))
                       #print New_Count_time
                   else:
                  
                       print "Warning Warning FINAL_DECAY IS NOT INCREMENTAL BUT EXPLICIT"
                       raw('Enter to continue')
                       New_Count_time=Count_time+FINAL_DECAY[t]
                       print "Final decay step", New_Count_time,FINAL_DECAY[t]
               else:
                   #break it up evenly 
                   #Count_time=Count_time+DECAY[irr]/float(DECAY_STEPS)
                   # break it up logrithmitacllly
                   New_Count_time=Count_time+(DECAY[irr]/FACTOR**(float(DECAY_STEPS)))*FACTOR**(t+1)
                     
               output_file.write(' %10.6E'%(New_Count_time))
               if t%FORMAT_ROW==FORMAT_ROW-1:
                    output_file.write('\n       ')
           output_file.write( ' \n')
           #  Saving the last inputedtime step
           TIME=New_Count_time
           output_file.write('61** f0.05 \n')
           #output_file.write('65$$ \n')
           #output_file.write('\'Gram-Atoms   Grams   Curies   Watts-All   Watts-Gamma \n')
           #output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')
           #output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')
           #output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')

           #   Saving information to the ft71f001 card
           #output_file.write(' 81$$ a1 2 a3 24 e  \n ')
           #output_file.write(' 82$$   ')
           #for step in range(DECAY_STEPS):
          #     output_file.write(' 2 ')
          #     if step%FORMAT_ROW==FORMAT_ROW-1:
          #        output_file.write('\n         ')
          # output_file.write(' e\n')
           
           
           
           # output_file.write('83**                                                                  \n')
           # output_file.write('1.0000000e+07 8.0000000e+06 6.5000000e+06 5.0000000e+06 4.0000000e+06 \n')
           # output_file.write('3.0000000e+06 2.5000000e+06 2.0000000e+06 1.6600000e+06 1.3300000e+06 \n')
           # output_file.write('1.0000000e+06 8.0000000e+05 6.0000000e+05 4.0000000e+05 3.0000000e+05 \n')
           # output_file.write('2.0000000e+05 1.0000000e+05 5.0000000e+04 1.0000000e+04 e             \n')
           # output_file.write('84**                                                                  \n')
           # output_file.write('2.0000000e+07 8.1873000e+06 6.4340000e+06 4.8000000e+06               \n')
           # output_file.write('3.0000000e+06 2.4790000e+06 2.3540000e+06 1.8500000e+06 1.4000000e+06 \n')
           # output_file.write('9.0000000e+05 4.0000000e+05 1.0000000e+05 2.5000000e+04 1.7000000e+04 \n')
           # output_file.write('3.0000000e+03 5.5000000e+02 1.0000000e+02 3.0000000e+01 1.0000000e+01 \n')
           # output_file.write('8.1000000e+00 6.0000000e+00 4.7500000e+00 3.0000000e+00 1.7700000e+00 \n')
           # output_file.write('1.0000000e+00 6.2500000e-01 4.0000000e-01 3.7500000e-01 e             \n')                                                                            
                                                                                                    
           
           
           
           
           
           output_file.write('t \n')

           #for step in range(DECAY_STEPS):
           #    output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
           #  For the last decay step need to add this card to say stop.  
           if irr==len(IRRADIATION)-1:
               # Saving the last ft71f001 file 
               output_file.write('56$$  0 0 a10 %i e t \n'%(DECAY_STEPS))
               output_file.write('56$$ f0 t \n')
               output_file.write('end \n')
           else:
               #  This is the input file for the next step      
               output_file.write('56$$ 0 1 a6 3 a10 %i a17 1 e t \n'%(DECAY_STEPS))
               output_file.write('60** 0 t \n')
    
        
        
    















# ==================================WRITE ORIGIN====================================================
def write_origen(USE_FT33,DECAY_STEPS,IRRADIATE,FORMAT_ROW,TITLE,UNITS,IRRADIATION, \
              DECAY,FINAL_DECAY,MIX_NUM,output_file,Isotopes,Frac,Mat,FISSION,FLUX,Power_instead_Flux):
    '''  #
    Code: write_origin.py
    
    Author:  Joshua Peterson
       
    Date:  Day after Birthday Nov 17 2011
    
    Description:  Writes origen input decks from MCNP data.
    
    Mod:   Nov 18 2011.  Cleaned up code and added better comments

    What I do here is I use a previously generated ft33f001 file and flux data either obtained from scale or mcnp
    as a function of burnup and then I do irrdations and decays based on the history of the reactor for a specified location
    and specified material.  
    
    Currently only the VXF4 and VXF12 postion.  
    
    I need to input parameters such as material, flux, location, decay history, irradaiton history, units plotted
    and then just run it.  
    
    Need to have the correct ft33f001 file with the correct extension to start the file.
    
    **Description of input:** 
    
       * USE_FT33= if you want to use an existing ft33 file
       * DECAY_STEPS number of decay steps
       * IRRADIATE  number of irradation steps
       * FORMAT_ROW number of rows per collum
       * TITLE    title used in the title card
       * UNITS    units you want to use
       * IRRADIATION days of irradation history
       * DECAY     days of decay history
       * FINAL_DECAY  final breakdown of decay history **NOTE**  This can be either as an array or a int/float use int/float if you dont care how it is broken up you just have a final time of decay.
       * MIX_NUM      (Mixture number used to copy over the ft33f001.mixNUM file.  If you use the word **'UNUSED'** Then it will assume the ft33f001 is allready generated in the temp directory.
       * output_file  output file to be writen
       * Isotopes     isotopes that used
       * Frac         fraction of the isotopes
       * Mat          type of isotope 1 for activation prodcuts 2 actinde 3 fission products 
       * FISSION      which fission products you want to include for irradation
       * NFISW       number of fission products you are including
       * FLUX        flux vector for each irradation 
       * Power_instead_Flux **This is a new one**. True means use Power False means use Flux 
    '''

    # Number of isotopes used
    FACTOR=1.151
    NUM_ISO=len(Isotopes)   
    NFISW=len(FISSION) # Number of fission enteries above 




    #  Moving the ft33f001 file to the correct location
    if USE_FT33:
        if MIX_NUM=='UNUSED':
            temp=1
           #print "Assuming ft33f001 is allready generated"
        else:
           output_file.write('=shell \n')
           output_file.write('cp $INPDIR/ft33f001.%s ft33f001 \n'%(MIX_NUM))
           output_file.write('end\n')
                                                                                                                                      
    #  INITALIZING INFORMATIOn
    time=[]
    decay_time=[]
    decay_time.append(0)
    count=0
    for irr in range(len(IRRADIATION)):
        # time is the time for irradation
        time.append(count)
        #  Here is a counter to keep it sequental
        count=IRRADIATION[irr]+count
        #  Here is a sequential for decay information
        decay_time.append(count)
        #  This addes decay plus the irradation to keep information straight
        count=DECAY[irr]+count
    
    
    output_file.write('=origens \n')
    output_file.write('0$$ a4 33 a11 71 e t \n') 
    TIME=0
    #  It increments over irradation.  
    #  NOTE:  the length of irradation needs to be the same as Decay
    if len(IRRADIATION) !=len(DECAY) or len(IRRADIATION) !=len(FLUX):
        print "ERROR ERROR Len of irradation needs to be length of decay and flux", len(IRRADIATION), len(DECAY),len(FLUX)
        print ("Len irr %s decay%s flux %s"%(len(IRRADIATION), len(DECAY), len(FLUX)))
        sys.exit()
    for irr in range(len(IRRADIATION)):  
           output_file.write('%s \n' %(TITLE))
           #  NOTE in second loop A16 is not there
           if irr==0:
                output_file.write('3$$ 33 a3 %i a4 27 a16 2 a33 18 e t \n'%(1))  
           else:
                #  IF USE_FT33 is true then incrementally use the ft33f001 file from Trition
                if USE_FT33:
                    output_file.write('3$$ 33 a3 %i a4 27 a16 2 a33 18 e t \n'%(irr))  
                else:
                    output_file.write('3$$ 33 a3 %i a4 27 a16 2 a33 18 e t \n'%(1))  
           output_file.write('35$$ 0 t \n')
           #  For irr=0 the number of isotopes are written here.  After that isotopes are not inputed
           if Power_instead_Flux:
              if irr==0:
                   output_file.write('56$$ %s %s a3 0 a6 1 a10 0 a13 %s a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE,NUM_ISO))  #a3 is for flux being read in
              else:
                  output_file.write('56$$ %s %s a3 0 a6 1 a10 1 a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE))# a10 1 a13 not there 
           else:
               if irr==0:
                    output_file.write('56$$ %s %s a3 1 a6 1 a10 0 a13 %s a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE,NUM_ISO))  #a3 is for flux being read in
               else:
                   output_file.write('56$$ %s %s a3 1 a6 1 a10 1 a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE))# a10 1 a13 not there 
           #This is where the initall time from the previous run is used.  So the output is nice looking
           output_file.write('57** %10.6E a3 1e-05  e \n'%(TIME))#time[i]))  #used to get better results
           output_file.write('95$$ 1 t \n')
           #  Input stuff into the comment line
           output_file.write('Cycle %i %s \n' %(irr+1,TITLE))

           # Writing out average power instead of flux
           if Power_instead_Flux:
               #  Writeing the flux out which is a function of burnup
               output_file.write('Power used for this cycle is %.3E MW \n'%(FLUX[irr]))
               output_file.write('58** ')

           else:
               output_file.write('Flux used for this cycle is %.3E n/cm2/s \n'%(FLUX[irr]))
               #  Writeing the flux out which is a function of burnup
               output_file.write('59** ')
           for tm in range(IRRADIATE):
               output_file.write(' %.3E '%(FLUX[irr]))
               if tm%FORMAT_ROW==FORMAT_ROW-1:
                   output_file.write('\n     ')
           #  Writing out the irradation time.  This is made to allow a range of irradation time
           output_file.write('\n60**  ')
           Count_time=TIME 
           #  breaks up to number of irradationation steps
           for t in range(IRRADIATE):
               #Count_time=Count_time+IRRADIATION[irr]/float(IRRADIATE)
               # Small steps  
               New_Count_time=Count_time+(IRRADIATION[irr]/FACTOR**(float(IRRADIATE)))*FACTOR**(t+1)
               output_file.write(' %10.6E'%(New_Count_time))
               # adds a return caracter to prevent for going pased speficied limit
               if t%FORMAT_ROW==FORMAT_ROW-1:
                    output_file.write('\n       ')

           output_file.write( ' \n')
           #  This is where the Time is set to the very last previous time step
           TIME=New_Count_time
           output_file.write('66$$ a1 2 a5 2 a9 2 e \n')
           if irr==0:
                #  For the first step outputs the material inforamtion specified above
                #output_file.write(ISOTOPES) #ISOTOPE
                #output_file.write(FRACTION) # Fraction
                #output_file.write(MATERIAL) # Material
                output_file.write('\n73$$  ')
                for i in Isotopes:
                    output_file.write('\t%s0'%(i))
                    if Isotopes.index(i)%FORMAT_ROW==FORMAT_ROW-1:
                        output_file.write('\n      ')
                    #ISOTOPES='73$$ 721740 721760   \n 721770 721780 721790 721800 \n' 
                output_file.write('\n74**  ')
                count_Frac=0
                for i in Frac:
                    output_file.write('\t%.5E'%(i))
                    if count_Frac%FORMAT_ROW==FORMAT_ROW-1:
                        output_file.write('\n      ')
                    count_Frac=count_Frac+1
                
                    #FRACTION='74** .16E-2 5.26E-2  18.60E-2 \n 27.28E-2  13.92E-2 35.08E-2  \n'
                output_file.write('\n75$$  ')
                count_Mat=0
                for i in Mat:
                    output_file.write('\t%s '%(i))
                    if count_Mat%FORMAT_ROW==FORMAT_ROW-1:
                        output_file.write('\n      ')
                    count_Mat=count_Mat+1
                    #MATERIAL='75$$ 1 1 1 1 1 1 \n'
        
        
        
        
                
                
                
           output_file.write('t \n')
           #  For saving the irradation information
           # IRRADIATE
           for step in range(IRRADIATE): 
               output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
           #  Decaying now
           output_file.write('54$$ a8 1 a11 0  e \n')
           output_file.write('56$$ a2 %s a6 1 a10 10 a15 3 a17 2 e \n'%(DECAY_STEPS))
           #  This writes the next time incrementally
           output_file.write('57** %10.6E a3 1e-05 e \n'%(TIME))     
           output_file.write('95$$ 0 t \n')
           output_file.write('Decay %i %s for flux %s \n' %(irr+1,TITLE,FLUX[irr]))
           output_file.write('Decay for experiment \n')
           output_file.write('60**  ')
           Count_time=TIME
           #  Doing a intremental step to specified decay with the number of steps being DECAY steps
           for t in range(DECAY_STEPS):
               #  if it is the last decay step
               if irr ==len(IRRADIATION)-1:
                   #  This is if the user just specifies the final decay or how the decay is broken up
                   if type(FINAL_DECAY)==int or type(FINAL_DECAY)==float:
                       #break it up evenly 
                       # break it up logrithmitacllly
                       New_Count_time=Count_time+(FINAL_DECAY/FACTOR**(float(DECAY_STEPS)))*FACTOR**(t+1)
                   else:
                       New_Count_time=Count_time+FINAL_DECAY[t]
                       print "Warning Warning FINAL_DECAY IS NOT INCREMENTAL BUT EXPLICIT"
                       #raw('Enter to continue')
                       print "Final decay step", Count_time,FINAL_DECAY[t]
               else:
                   #break it up evenly 
                   #Count_time=Count_time+DECAY[irr]/float(DECAY_STEPS)
                   # break it up logrithmitacllly
                   New_Count_time=Count_time+(DECAY[irr]/FACTOR**(float(DECAY_STEPS)))*FACTOR**(t+1)
                     
               output_file.write(' %10.6E'%(New_Count_time))
               if t%FORMAT_ROW==FORMAT_ROW-1:
                    output_file.write('\n       ')
           output_file.write( ' \n')
           #  Saving the last inputedtime step
           TIME=New_Count_time
           output_file.write('61** f0.05 \n')
           output_file.write('65$$ \n')
           output_file.write('\'Gram-Atoms   Grams   Curies   Watts-All   Watts-Gamma \n')
           output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')
           output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')
           output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')

           #   Saving information to the ft71f001 card
           output_file.write(' 81$$ a1 2 a3 24 e  \n ')
           output_file.write(' 82$$   ')
           for step in range(DECAY_STEPS):
               output_file.write(' 2 ')
               if step%FORMAT_ROW==FORMAT_ROW-1:
                  output_file.write('\n         ')
           output_file.write(' e\n')
           
           
           
           output_file.write('83**                                                                  \n')
           output_file.write('1.0000000e+07 8.0000000e+06 6.5000000e+06 5.0000000e+06 4.0000000e+06 \n')
           output_file.write('3.0000000e+06 2.5000000e+06 2.0000000e+06 1.6600000e+06 1.3300000e+06 \n')
           output_file.write('1.0000000e+06 8.0000000e+05 6.0000000e+05 4.0000000e+05 3.0000000e+05 \n')
           output_file.write('2.0000000e+05 1.0000000e+05 5.0000000e+04 1.0000000e+04 e             \n')
           output_file.write('84**                                                                  \n')
           output_file.write('2.0000000e+07 8.1873000e+06 6.4340000e+06 4.8000000e+06               \n')
           output_file.write('3.0000000e+06 2.4790000e+06 2.3540000e+06 1.8500000e+06 1.4000000e+06 \n')
           output_file.write('9.0000000e+05 4.0000000e+05 1.0000000e+05 2.5000000e+04 1.7000000e+04 \n')
           output_file.write('3.0000000e+03 5.5000000e+02 1.0000000e+02 3.0000000e+01 1.0000000e+01 \n')
           output_file.write('8.1000000e+00 6.0000000e+00 4.7500000e+00 3.0000000e+00 1.7700000e+00 \n')
           output_file.write('1.0000000e+00 6.2500000e-01 4.0000000e-01 3.7500000e-01 e             \n')                                                                            
                                                                                                    
           
           
           
           
           
           output_file.write('t \n')

           for step in range(DECAY_STEPS):
               output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
           #  For the last decay step need to add this card to say stop.  
           if irr==len(IRRADIATION)-1:
               output_file.write('56$$ f0 t \n')
               output_file.write('end \n')
           else:
               #  This is the input file for the next step      
               output_file.write('56$$ 0 1 a6 3 a10 %i a17 2 e t \n'%(DECAY_STEPS))
               output_file.write('60** 0 t \n')
    
        
        
    

  
  
  
  
  
# ==================================WRITE ORIGIN====================================================
def write_decay(Isotopes,Frac,DECAY_TIME, DECAY_STEPS,output_file):
    #
    #
    #     Code: write_decay.py
    #
    #     Author:  Joshua Peterson
    #   
    #     Date:  April 30, 2012
    #
    #     Description:  Writes decay information for ORIGENS  
    #
    ########################################
    ''' 
    @TODO
    Isotope= Isotopes to be used in the problem
    Frac is the fraction assicated with the Isotopes
    Mat is the material type assocated with the Isotopes
    Decay_time.  Total length of time for decay.
    
    DECAY_STEPS:  Number of decay steps per decay run  
    
    
         
    '''

    #  Assigns what type of material it is based on the isotopic information
    Mat=origen_mat(Isotopes)        
            

    FORMAT_ROW=5

    
    # Gets the total mass (g) from an output in the deplation card
    Total_mass=0
    for mass in Frac:
        Total_mass=Total_mass+mass
        
    # Checks that the lenghts are all the same
    if len(Isotopes)  != len(Frac) and len(Frac) != len(ISOTOPE_TYPE) :
        print "ERROR ERROR len isotope %s mass %s and Type %s not equal"%(len(Isotopes), len(Frac) ,len(Mat))
        sys.exit()
    else:
        LEN_ISOTOPE=len(Isotopes)
        
        


                                                                                   
    output_file.write("'This SCALE input file was generated by Joshua Peterson \n")
    output_file.write("=origens \n")
    # ************ DATA BLOCK 1************
    output_file.write("0$$ a11 71 e t  \n")
    # ************DATA BLOCK 2 ************
    output_file.write("Single Decay Only Case \n")  
    output_file.write("3$$ a1 21 a2 1 a3 1  a4 27 a16 2 a33 18 e t                                     \n")
    #************DATA BLOCK 4  ************
    output_file.write("35$$ 0 t                                                              \n")
    # ************DATA BLOCK 5************
    #  a11-0 applies to UO2 mediam for a,n reactionrs and a, n spectra
    output_file.write("54$$ a8 1 a11 0  e                                                    \n")
    
    output_file.write("56$$ a2 %i a6 1 a10 0 a13 %i a15 3 a17 2 e \n"%(DECAY_STEPS,LEN_ISOTOPE))
    #  a3 What concerntation to cut material from printing out
    output_file.write("57** a1 0 a3 1e-05 e                                                     \n")
    output_file.write("95$$ 1 t                                                              \n")
    output_file.write("Only depletion case                                                   \n")
    output_file.write("Total density %.5E g/cc                                                 \n"%(Total_mass))
    #  This prints out the time interval
    output_file.write('60**  ')
    #  Doing a intremental step to specified decay with the number of steps being DECAY steps
    Count_time=0
    for t in range(DECAY_STEPS):
        #  if it is the last decay step
        #break it up evenly (Need to change eventually) 
        Count_time=Count_time+DECAY_TIME/float(DECAY_STEPS)  
        output_file.write(' %10.6f'%(Count_time))
        if t%FORMAT_ROW==FORMAT_ROW-1:
             output_file.write('\n       ')
    output_file.write( ' \n')
    #  Cutoff from output
    output_file.write("61** f0.05\n")
    # Prints out information in output 
    output_file.write("65$$\n")
    output_file.write("'Gram-Atoms   Grams   Curies   Watts-All   Watts-Gamma \n")
    output_file.write(" 3z   1   0   0   3z   3z   3z   6z  \n")
    output_file.write(" 3z   1   0   0   3z   3z   3z   6z \n")
    output_file.write(" 3z   1   0   0   3z   3z   3z   6z   \n")
    # Gamma source option a3 bremsstrahlung for UO2 matrix
    output_file.write("81$$ a1 2  a3 26 a4 1 a7 200 e  \n")
    #  Time step saving information for each decay step
    output_file.write('82$$   ')
    for step in range(DECAY_STEPS):
        output_file.write(' 2 ')
        if step%FORMAT_ROW==FORMAT_ROW-1:
           output_file.write('\n       ')
    output_file.write(' e\n')
    output_file.write('83** \n')
    output_file.write('1.0000000e+07 8.0000000e+06 6.5000000e+06 5.0000000e+06 4.0000000e+06 \n')
    output_file.write('3.0000000e+06 2.5000000e+06 2.0000000e+06 1.6600000e+06 1.3300000e+06 \n')
    output_file.write('1.0000000e+06 8.0000000e+05 6.0000000e+05 4.0000000e+05 3.0000000e+05 \n')
    output_file.write('2.0000000e+05 1.0000000e+05 5.0000000e+04 1.0000000e+04 e             \n')
    output_file.write('84**  \n')
    output_file.write('2.0000000e+07 8.1873000e+06 6.4340000e+06 4.8000000e+06               \n')
    output_file.write('3.0000000e+06 2.4790000e+06 2.3540000e+06 1.8500000e+06 1.4000000e+06 \n')
    output_file.write('9.0000000e+05 4.0000000e+05 1.0000000e+05 2.5000000e+04 1.7000000e+04 \n')
    output_file.write('3.0000000e+03 5.5000000e+02 1.0000000e+02 3.0000000e+01 1.0000000e+01 \n')
    output_file.write('8.1000000e+00 6.0000000e+00 4.7500000e+00 3.0000000e+00 1.7700000e+00 \n')
    output_file.write('1.0000000e+00 6.2500000e-01 4.0000000e-01 3.7500000e-01 e             \n')
    
    
    #  Output the material information
    output_file.write('73$$  ')
    for i in Isotopes:
        output_file.write('\t%s0'%(i))
        if Isotopes.index(i)%FORMAT_ROW==FORMAT_ROW-1:
            output_file.write('\n      ')
        #ISOTOPES='73$$ 721740 721760   \n 721770 721780 721790 721800 \n' 
    output_file.write('\n74**  ')
    count_Frac=0
    for i in Frac:
        output_file.write('\t%.5E'%(i))
        if count_Frac%FORMAT_ROW==FORMAT_ROW-1:
            output_file.write('\n      ')
        count_Frac=count_Frac+1
    
        #FRACTION='74** .16E-2 5.26E-2  18.60E-2 \n 27.28E-2  13.92E-2 35.08E-2  \n'
    output_file.write('\n75$$  ')
    count_Mat=0
    for i in Mat:
        output_file.write('\t%s '%(i))
        if count_Mat%FORMAT_ROW==FORMAT_ROW-1:
            output_file.write('\n      ')
        count_Mat=count_Mat+1
        #MATERIAL='75$$ 1 1 1 1 1 1 \n'

    output_file.write('t \n')
    #************  DATABLOCK 5 *******************  
    for step in range(DECAY_STEPS):
        output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
        #  For the last decay step need to add this card to say stop.  
    output_file.write('56$$ f0 t \n')
    output_file.write('end \n')
    
 


# ==================================WRITE ORIGIN====================================================
def decay_ft71(DECAY_TIME, DECAY_STEPS,INDEX_NUMBER,output_file):
    #
    #
    #     Code: decay_ft71.py
    #
    #     Author:  Joshua Peterson
    #   
    #     Date: December 20, 2012
    #
    #     Description:  Writes decay information for ORIGENS  
    #
    ########################################
    ''' 
    @TODO
    Isotope= Isotopes to be used in the problem
    Frac is the fraction assicated with the Isotopes
    Mat is the material type assocated with the Isotopes
    Decay_time.  Total length of time for decay.
    
    DECAY_STEPS:  Number of decay steps per decay run  
    
    
         
    '''

           

    FORMAT_ROW=5
    output_file.write("'This SCALE input file was generated by Joshua Peterson \n")
    output_file.write("=origens                                               \n")
    output_file.write("0$$ a11 71 e t                                         \n")
    output_file.write("Single Decay Case                                      \n")
    #output_file.write("3$$ a1 21 a2 1 a3 1  a4 27 a16 2 a33 18 e t                                     \n")    
    output_file.write("3$$ a1 21 1 1 0 a16 2 a33 0 e t                           \n")
    output_file.write("35$$ 0 t                                               \n")
    output_file.write("54$$ a8 1 a11 0  e                                     \n")   
    output_file.write("56$$ a2 %i a10 0 a13 -%s a15 3 a17 4 e \n"%(DECAY_STEPS,INDEX_NUMBER))   
    output_file.write("57** 0 a3 1e-05 e                                      \n")   
    output_file.write("95$$ 0 t                                               \n")   
    output_file.write("Case 1                                                 \n")   
    output_file.write("Only depletion case                                    \n")      
    output_file.write('60**  ')
    #  Doing a intremental step to specified decay with the number of steps being DECAY steps
    Count_time=0
    # If hte user specifies the steps for decay time then write it out expecility otherwise do it impliclty
    if type(DECAY_TIME)!=int:
         counter=0
         for time in DECAY_TIME:
             output_file.write(' %.4E'%(time))
             counter=counter+1
             if counter%FORMAT_ROW==FORMAT_ROW-1:
                  output_file.write('\n       ')            
    
    else:    
        for t in range(DECAY_STEPS):
            #  if it is the last decay step
            #break it up evenly (Need to change eventually) 
            Count_time=Count_time+DECAY_TIME/float(DECAY_STEPS)  
            output_file.write(' %.4E'%(Count_time))
            if t%FORMAT_ROW==FORMAT_ROW-1:
                 output_file.write('\n       ')
    output_file.write( ' \n')
    output_file.write("61** f0.05                                             \n")      
    output_file.write("65$$                                                   \n")      
    output_file.write("'Gram-Atoms   Grams   Curies   Watts-All   Watts-Gamma \n")      
    output_file.write(" 3z   1   0   0   3z   3z   3z   6z                    \n")      
    output_file.write(" 3z   1   0   0   3z   3z   3z   6z                    \n")      
    output_file.write(" 3z   1   0   0   3z   3z   3z   6z                    \n")      
    output_file.write("t                                                      \n")      
    #************  DATABLOCK 5 *******************  
    for step in range(DECAY_STEPS):
        output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
        #  For the last decay step need to add this card to say stop.
    output_file.write("56$$ f0 t                                              \n")   
    output_file.write("end                                                    \n")   






# ==================================WRITE COUPLE====================================================
def write_couple(Energy_tally,Multiply_tally,cell_num,WEIGHT_GROUP,FISSION,output_file,UPDATE_CROSS,DESIRED_MATERIAL,REACTION,START_NUM):

          
    FORMAT_ROW=4
    
    if WEIGHT_GROUP==49:
        CROSS=77
    elif WEIGHT_GROUP==200:
        CROSS=78
    elif WEIGHT_GROUP==44:
        CROSS=79
    elif WEIGHT_GROUP==238:
        CROSS=80  


    
    if len(FISSION)>1:
        NFISW=len(FISSION)
    else:
        NFISW=0
    
    print FISSION,len(FISSION),NFISW
    #raw_input()
        
    output_file.write('=couple \n\n')
    

    output_file.write('0$$ a3 {JD} a4 {ND} a6 {MD} e \n'.format(JD=CROSS, ND=21, MD=33))
    # 0$$ array
    # a3. JD  AMPX neutron  =77, 49-group 78, 200-group 79, 44-group 80, 238-group                                                                                                                                                                                                                                                                                                                                                      
    # a4. ND  Input ORIGEN binary library {if LBIN = 0} (21).                                                                                                                                                                                                                                                                                                                                                                           
    # a6. MD  Output ORIGEN binary library (33).                                                                                                                                                                                                                                                                                                                                                                                        
    # e   : always needed                                                                                                                                                                                                                                                                                                                                                                                                                
    #  DEBUG JOSH PETERSON    
    
    
    
    
    
    output_file.write('1$$ a3 {LBUP} a4 {JADD} a5 {JEDT} a10 {IDENT} a11 {NEWID} a12 {IDREF} a13 {NZONE}\n     \
     a15 {NFISW} a16 {NUMA} a17 {NORM} a18 {NWGT} e t \n'.format
        (LBUP=UPDATE_CROSS, JADD=1, JEDT=0, IDENT=0, NEWID=9022, IDREF=0, NZONE=0, NFISW=NFISW, NUMA=8, NORM=0, NWGT=WEIGHT_GROUP))
    # output_file.write('0$$ a3 {JD} a4 {ND} a6 {MD} e \n'.format(JD=80, ND=21, MD=33))    
    # 1$$  Array  Control Constants [19 entries].                                                                                                                                                                                                                                                                                                                                                                                       
    # a3.  LBUP  1/0  Update from user input cross sections (Data Block 8) / no user update (0).                                                                                                                                                                                                                                                                                                                                       
    # a4.  JADD  1/0  Add/do not add new transitions to the library (1).                                                                                                                                                                                                                                                                                                                                                               
    # a5.  JEDT  1/0  Edit input library only/normal library generation case (0).                                                                                                                                                                                                                                                                                                                                                      
    # a10  IDENT  ID number of weighted AMPX library (0).                                                                                                                                                                                                                                                                                                                                                                               
    # a11  NEWID  Updated library ID number (0).                                                                                                                                                                                                                                                                                                                                                                                        
    # a12. IDREF  Nuclide ID number of the isotope in AMPX library on unit LD that contains the neutron flux weighting spectrum to be used to collapse multigroup cross sections. If 0, code uses flux from first isotope in weighted AMPX library, which is usually the zone flux                                                                                                                                    
    # a13  NZONE  The zone of the nuclides with which to add/update the library. Used for library                                                                                                                                                                                                                                                                                                                     
    # a15  NFISW  Number of fissile nuclides 1, all 30 fissionable N nuclides defined in 7$ array                                                                                                                                                                                                                                                                                                                                      
    # a16  NUMA  Number of title lines from teh start of the input library prologue to be retained in the ouput library porlouge                                                                                                                                                                                                                                                                                                         
    # a17 NORM  Cross section normalization -1/0/N  thermal flux/ total flux/ cross section N/                                                                                                                                                                                                                                                                                                                                           
    # a18 NWGT  For defining source of weighting flux spectrum data (0)  1, generate weighting spectrum using 2* array parameters  0, obtain flux from AMPX library on unit LD, nuclide IDREF N, user-defined N group weight spectrum input in 9* array NOTE: must be consitstant with 0$ a3.                                                                                                                                          
    # e    always needed                                                                                                                                                                                                                                                                                                                                                                                                                 
    # t    always needed  Data Block 1 terminator.  



    output_file.write('\'   ********  Start of Block 2   flux spectrum  fission yield  ************                %  \n')                                                                       
    print len(FISSION)
    if NFISW!=0:
        #  7$$ Nuclide ID numbers for nuclides with fission yields [1$-a15]. 
        count=0
        output_file.write('7$$   ')
        for fiss in FISSION:
            count=count+1
            output_file.write('%i  '%(fiss))
            if count%7==0:                   
                output_file.write('\n       ')
        output_file.write('\n\n') 
     
    

                
    #  9** Array  User input weighting function [$1-a18].
    #  Get the needed weighting function
    if WEIGHT_GROUP>0:
        Energy=[]
    
        output_file.write('\n9**   ')
    
        for tal in range(len(Energy_tally[cell_num].energy_tally)):
            Energy.append(Energy_tally[cell_num].energy_tally[tal])
        count=0
        for flux in reversed(Energy):
            count=count+1
            output_file.write('%7E   '%(flux))
            #print i, flux
            if count%FORMAT_ROW==FORMAT_ROW-1:
                output_file.write('\n      ')
        output_file.write(' e     t \n')
    
    
    #  @TODO  Need to update cross section also
    START_MAT=[]
    END_MAT=[]
    if UPDATE_CROSS:
        
 
        # This creates a cross section file for couple
        Cross_section=[]
        # Multiply_tally has the objects .mult_cell, .mult_mat, .mult_value, .mult_reaction, ,multi_micro=[] "
        for tally_num in Multiply_tally:
            for i in range(len(Multiply_tally[tally_num].mult_cell)):
                Multi_cell_num=Multiply_tally[tally_num].mult_cell[i]
                if Multi_cell_num==cell_num:
                   Cross_section.append(Multiply_tally[tally_num].multi_micro[i])
                   Material=DESIRED_MATERIAL[Multiply_tally[tally_num].mult_mat[i]-START_NUM]
                   Reaction=Multiply_tally[tally_num].mult_reaction[i]
                   #print DESIRED_MATERIAL[Multiply_tally[tally_num].mult_mat[i]-START_NUM]
                   # If fission then the first one is negative and the daughter is positive
                   if Reaction==18:
                       START_MAT.append("-%i0"%(Material))
                   else:
                       START_MAT.append("%i0"%(Material))
                   
                   if Reaction==102:
                       END_MAT.append("%i0"%(Material+1)) 
                   elif Reaction==18:
                       END_MAT.append("%i0"%(Material))                   
                   else:
                        print "ERROR: ERROR:  NOT INFORMAITON FOR CROSS SECTION:  EXITING"
                        sys.exit()      
        
        #  Removal all results that have zero for the cross section
        pop=[]
        for i in range(len(Cross_section)):
            if Cross_section[i]==0:
                print "Removeing croos section for %s to reaction %s because it was zero"%(START_MAT[i] ,END_MAT[i])
                pop.append(i)
        #print pop, len(Cross_section),Cross_section
        for i in range(len(pop)-1,-1,-1):
            #print pop[i],i
            Cross_section.pop(pop[i])
            START_MAT.pop(pop[i])
            END_MAT.pop(pop[i])
        #print Cross_section
        
        
        output_file.write(' \n\' ********* Start of Data Block 6 number of reaction rates NOTE:  required if 1$-a3 = 1} ****  \n')
    
        # '  NOTE:  required if 1$-a3 or LBUP = 1}. 
    
        # LBU  Total number of nuclide reaction cross sections to be entered (0).                                                                                      
        DESIRED_MATERIAL
        output_file.write('15$$ {LBU} T \n'.format(LBU=len(START_MAT)))
        output_file.write( '\'   **************   Data Block 8  Reaction rate    *************       % \n')
        output_file.write('71$$ ')
        for mat in range(len(START_MAT)):
            output_file.write(" %s "%(START_MAT[mat]))
            if mat%FORMAT_ROW-1==0:
                output_file.write("\n      ")

        output_file.write('\n72$$ ')
        for mat in range(len(END_MAT)):
            output_file.write(" %s "%(END_MAT[mat]))
            if mat%FORMAT_ROW-1==0:
                output_file.write("\n      ")                    

        output_file.write('\n73**  ')
        for mat in range(len(Cross_section)):
            output_file.write(" %s "%(Cross_section[mat]))
            if mat%FORMAT_ROW-1==0:
                output_file.write("\n      ")                    

        output_file.write('\nT\n')
    output_file.write('done \n')
    output_file.write('end \n')
    
    
        
        
        
        
 # ==================================WRITE COUPLE====================================================
def write_couple_no_cross(Energy,cell_num,WEIGHT_GROUP,FISSION,output_file):
    # like write couple but does not support cross section 
    
    

    
      
    FORMAT_ROW=4
    
    if WEIGHT_GROUP==49:
        CROSS=77
    elif WEIGHT_GROUP==200:
        CROSS=78
    elif WEIGHT_GROUP==44:
        CROSS=79
    elif WEIGHT_GROUP==238:
        CROSS=80  


    
    if len(FISSION)>1:
        NFISW=len(FISSION)
    else:
        NFISW=0
    
    print FISSION,len(FISSION),NFISW
    #raw_input()
        
    output_file.write('=couple \n\n')
    

    output_file.write('0$$ a3 {JD} a4 {ND} a6 {MD} e \n'.format(JD=CROSS, ND=21, MD=33))
    # 0$$ array
    # a3. JD  AMPX neutron  =77, 49-group 78, 200-group 79, 44-group 80, 238-group                                                                                                                                                                                                                                                                                                                                                      
    # a4. ND  Input ORIGEN binary library {if LBIN = 0} (21).                                                                                                                                                                                                                                                                                                                                                                           
    # a6. MD  Output ORIGEN binary library (33).                                                                                                                                                                                                                                                                                                                                                                                        
    # e   : always needed                                                                                                                                                                                                                                                                                                                                                                                                                
    #  DEBUG JOSH PETERSON    
    
    
    
    
    
    output_file.write('1$$ a3 {LBUP} a4 {JADD} a5 {JEDT} a10 {IDENT} a11 {NEWID} a12 {IDREF} a13 {NZONE}\n     \
     a15 {NFISW} a16 {NUMA} a17 {NORM} a18 {NWGT} e t \n'.format
        (LBUP=0, JADD=1, JEDT=0, IDENT=0, NEWID=9022, IDREF=0, NZONE=0, NFISW=NFISW, NUMA=8, NORM=0, NWGT=WEIGHT_GROUP))
    # output_file.write('0$$ a3 {JD} a4 {ND} a6 {MD} e \n'.format(JD=80, ND=21, MD=33))    
    # 1$$  Array  Control Constants [19 entries].                                                                                                                                                                                                                                                                                                                                                                                       
    # a3.  LBUP  1/0  Update from user input cross sections (Data Block 8) / no user update (0).                                                                                                                                                                                                                                                                                                                                       
    # a4.  JADD  1/0  Add/do not add new transitions to the library (1).                                                                                                                                                                                                                                                                                                                                                               
    # a5.  JEDT  1/0  Edit input library only/normal library generation case (0).                                                                                                                                                                                                                                                                                                                                                      
    # a10  IDENT  ID number of weighted AMPX library (0).                                                                                                                                                                                                                                                                                                                                                                               
    # a11  NEWID  Updated library ID number (0).                                                                                                                                                                                                                                                                                                                                                                                        
    # a12. IDREF  Nuclide ID number of the isotope in AMPX library on unit LD that contains the neutron flux weighting spectrum to be used to collapse multigroup cross sections. If 0, code uses flux from first isotope in weighted AMPX library, which is usually the zone flux                                                                                                                                    
    # a13  NZONE  The zone of the nuclides with which to add/update the library. Used for library                                                                                                                                                                                                                                                                                                                     
    # a15  NFISW  Number of fissile nuclides 1, all 30 fissionable N nuclides defined in 7$ array                                                                                                                                                                                                                                                                                                                                      
    # a16  NUMA  Number of title lines from teh start of the input library prologue to be retained in the ouput library porlouge                                                                                                                                                                                                                                                                                                         
    # a17 NORM  Cross section normalization -1/0/N  thermal flux/ total flux/ cross section N/                                                                                                                                                                                                                                                                                                                                           
    # a18 NWGT  For defining source of weighting flux spectrum data (0)  1, generate weighting spectrum using 2* array parameters  0, obtain flux from AMPX library on unit LD, nuclide IDREF N, user-defined N group weight spectrum input in 9* array NOTE: must be consitstant with 0$ a3.                                                                                                                                          
    # e    always needed                                                                                                                                                                                                                                                                                                                                                                                                                 
    # t    always needed  Data Block 1 terminator.  



    output_file.write('\'   ********  Start of Block 2   flux spectrum  fission yield  ************                %  \n')                                                                       
    print len(FISSION)
    if NFISW!=0:
        #  7$$ Nuclide ID numbers for nuclides with fission yields [1$-a15]. 
        count=0
        output_file.write('7$$   ')
        for fiss in FISSION:
            count=count+1
            output_file.write('%i  '%(fiss))
            if count%7==0:                   
                output_file.write('\n       ')
        output_file.write('\n\n') 
     
    

                
    #  9** Array  User input weighting function [$1-a18].
    #  Get the needed weighting function
    if WEIGHT_GROUP>0:
    
        output_file.write('\n9**   ')
        count=0
        print "Energy",Energy
        for flux in Energy:
            count=count+1
            output_file.write('%7E   '%(flux))
            #print i, flux
            if count%FORMAT_ROW==FORMAT_ROW-1:
                output_file.write('\n      ')
        output_file.write(' e     t \n')
    
    #  @TODO  Need to update cross section also
    START_MAT=[]
    END_MAT=[]


    output_file.write('done \n')
    output_file.write('end \n')
        
    
       
    
    
    
    
    
    
    




















# ==================================GET TALLY====================================================
def get_tally(Result_file,Multple_value,RETURN_HEAT):
    '''#!/usr/bin/env python
    #  Results file is the file where the results were saved to i.e mcnp output file
    #  The Multiple_value file is if to use the Multiple scalled oppripriate or not.
    #
    #
    #
    #     Code: get_tally.py 
    #
    #     Author:  Joshua Peterson
    #   
    #     Date:  Second week at work at ORNL
    #
    #     Description:  This gets data from MCNP tallies and parses to screen or processes ect.
    #     
    #     Date:  Week after Josh left made it an object of libraries for easier use
    ########################################
   ''' 
    
    
    
    
    
   
    
    #################   Check for the write inport format
    try:
        input_file = open(Result_file, 'r')
    except IndexError:
        print "ERROR 1:  The command should read ]$ get_tally.py [output.o] "
        sys.exit()
        
    PRINT_MULTIPLY=True
    #print "WARNING WARNING FOR TIME THE VXF-12 UNFORMAT IS SET TO TRUE SHOULD CHANGE THIS"
    #VFX_12=raw_input('Running fo VXF_12(Unformated) True(1) or False (2):  ') 
    VFX_12='1'
    #VFX_12='1' 
    if VFX_12=='1': #Starts two cycles latter  
        UNFORMATED_OUTPUT=True  #For UO2 of VXF12
    else    :    #VXF_4 
        UNFORMATED_OUTPUT=False  #This is used if the output is different current VXF4 is fasle and VXF12 is True
    
    #  Energy tally that will be used to create tally objects                            
    Energy_tally={}
    #  Flux tally used to create tally objects
    Flux_tally={}
    # Multiply tally used to create tally objects
    Multiply_tally={}
    
     
    Neutron_per_fission=2.43
    KEFF=1.0
    for line in input_file: 
        #  Gets nu from inpt
        if "the average number of neutrons produced per fission" in line:
            temp=line.split()
            Neutron_per_fission=float(temp[10])
            print "Nu is equal to ", Neutron_per_fission
        if "= final keff =" in line: 
            #  Split line a seperate by space
            temp=line.split()
            #  There is keff) so seperating the ) from the keff value
            temp=temp[len(temp)-1].split(')')
            # saving KEFF for results
            KEFF=float(temp[0])
        #  This is where it looks for tally information
        #  Fluctuation chart is at the end and has not tally information
        if "1tally" in line and "fluctuation charts" not in line:
            #  This is a way to continue to loop through the results until the end of the tally is found
            Tally=True
            #  Creates strings objects from the line
            temp=line.split()
            #  Saving the tally number
            tally_num=int(temp[1])
            if UNFORMATED_OUTPUT:
                Flux_tally[tally_num]=Tallies()  #  Define object tally
            if "nps" in line:
                NPS=True
                # Saving the NPS number;  Never use it though
                NPS_value=temp[4]
            else:
                NPS=False
            # This statment Assign lib is used so that a new array of Tallies can be created without overwriting other information
            #  There is probably a cleaner way of doing this but I do not know
            ASSIGN_LIB=True 
            while(Tally):
                line=input_file.next()
                temp=line.split()
                # This is for unformated output which is a little tricker to get data for
                if UNFORMATED_OUTPUT:
                    if "cell" in line and len(temp)==2:
                        Cell=int(temp[1])
                        line=input_file.next()
                        temp=line.split()
                        #cell  8901
                        #                1.14575E+04 0.0098
                        #
                        #cell  8902
                        #                8.33106E+02 0.0424
                        #
                        #cell  8903
                        #                4.55796E+01 0.0984 
                        if len(temp)==2 and "cell" not in line:
                            Flux_tally[tally_num].cell_num.append(Cell)
                            Flux_tally[tally_num].tally_result.append(float(temp[0]))
                            Flux_tally[tally_num].tally_error.append(float(temp[1]))



                    #  This gets the energy information from these tallies
                    if "energy" in line and len(temp)==1:  #  This is for a different format result
                        #********  THIS IS WHAT THE UNFORMATED OUTPUT LOOKS LIKE FOR ENERGY TALLIES
                        #
                        #            1tally   4        nps =   480107591
                        #                                     Tally for cell number 13653
                        #           tally type 4    track length estimate of particle flux.      units   1/cm**2
                        #           tally for  neutrons
                        # number of histories used for normalizing tallies =    460100000.00
                        # 
                        #           volumes
                        #                   cell:     13653
                        #                         2.88811E+01
                        # 
                        #  cell  410                                                                                                             
                        #       energy
                        #     6.2500E-07   2.35923E-04 0.0013
                        #     1.0000E-01   1.47748E-04 0.0016
                        #     2.0000E+01   1.30104E-04 0.0016
                        #       total      5.13775E-04 0.0009
                        #  
                        #  cell  411                                                                                                             
                        #       energy
                        #     6.2500E-07   2.36017E-04 0.0012
                        #                 
                        line=input_file.next()
                        # This stops when total is in line
                        while ('total' not in line):
                            temp=line.split()
                            if ASSIGN_LIB:
                                Energy_tally[tally_num]=Tallies()  #  Define object tally
    
                                if NPS:
                                    Energy_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)    
                                ASSIGN_LIB=False
                            temp=line.split()
                            Energy_tally[tally_num].energy_min.append(float(temp[0]))
                            Energy_tally[tally_num].energy_max.append(float(temp[0]))
                            Energy_tally[tally_num].energy_cell.append(Cell) #No cell number here
                            Energy_tally[tally_num].energy_tally.append(float(temp[1]))
                            Energy_tally[tally_num].energy_error.append(float(temp[2]))
                            #  Continues to loop until gets to total
                            line=input_file.next()
                        temp=line.split()
                        #  This gets the flux information from the total in an energy tally
                        #  
                        
                        if (NPS):
                           Flux_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)
                        Flux_tally[tally_num].cell_num.append((Cell))
                        Flux_tally[tally_num].tally_result.append(float(temp[1]))
                        Flux_tally[tally_num].tally_error.append(float(temp[2]))
                        #
                        #Tally=False
                        #print "End of reading input here"
                    if "multiplier bin" in line:
                        #  This is what a unformated multipler problem looks like
                        #  *****************************************                
                        #   1tally 434        nps =    35007740
                        #+                                    Heating rate for neutrons results are [MEV/g_sp]                          
                        #           tally type 4    track length estimate of particle flux.                        
                        #           tally for  neutrons 
                        # number of histories used for normalizing tallies =     30000000.00
                        #  cell  3000 
                        #    ....  .... ...                                                                                                            
                        #  multiplier bin:   1.00000E+00 2001         -2                                                                         
                        #                  4.42755E-06 0.0006
                        #  
                        #  cell  3000                                                                                                            
                        #  multiplier bin:   1.00000E+00 2002         -2                                                                         
                        #                  2.09502E-02 0.0012
                        #  
                        #  cell  3000                                                                                                            
                        #  multiplier bin:   1.00000E+00 2003         -2                                                                         
                        #                  1.33492E-03 0.0032
                        #                                    
    
                        # This stops when it reaches the end of the line ... ha ha
                        EXIT=False
                        while ('================='  not in line and EXIT==False):
                            #  Tally->Cell->Mat->Reaction rates
                            temp=line.split()
                            #  This is if this is the first itteration.  
                            if ASSIGN_LIB:
                                Multiply_tally[tally_num]=Tallies()  #  Define object tally
                                if NPS:
                                    Multiply_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)    
                                ASSIGN_LIB=False
                            
                            temp=line.split()
                            #  This is used if the multiplier is also split by energy.  
                            #if 'energy' in temp:
                            #    
                            #    print "WARNING Need to fix this"
                            #    line=input_file.next()
                            #else: 
                            #print temp
                            Multiplier=float(temp[2])
                            Material_num=int(temp[3])
                            Reaction_rate=int(temp[4])
                            #  Assigning values
                            Multiply_tally[tally_num].mult_cell.append(int(Cell))
                            Multiply_tally[tally_num].mult_mat.append(int(Material_num))
                            Multiply_tally[tally_num].mult_value.append(float(Multiplier))
                            Multiply_tally[tally_num].mult_reaction.append(int(Reaction_rate))
                            #  Getting information on the next line
                            line=input_file.next()
                            temp=line.split()
                            #  This is used if the multiplier is also split by energy.  
                            if 'energy' in temp:
                                
                                print "WARNING Need to fix this but exiting for now.  \nCross section is broken into Energy bins \nget rid of the E0 in input"
                                #line=input_file.next()
                                PRINT_MULTIPLY=False
                                # Need to exit this section
                                EXIT=True
                            else:    
                                Result=temp[0]
                                Error=temp[1]
                                Multiply_tally[tally_num].mult_tally.append(float(Result))
                                Multiply_tally[tally_num].mult_error.append(float(Error))

                                #  Continues to loop until gets to the end
                                line=input_file.next()
                                #  There is a space that is ignored
                                line=input_file.next()
                                #  Splits for hte cell information
                                temp=line.split()
                                # Saves the cell information
                                #print temp
                                '  Exit if this is found at the end of the line'
                                if 'there are no nonzero' in line:
                                       #Leave this inner loop
                                       EXIT= True
                                       # Leave the outer loop
                                       Tally=False
                                if len(temp)==2:
                                    Cell=int(temp[1]) 
                                # finaly next line
                                line=input_file.next()
                                #print line
    


                    if "==============================" in line:    
                        Tally=False 
                    if "there are no nonzero tallies in the" in line:
                        Tally=False
                    if "run terminated when" in line:
                        Tally=False
                        print "run terminated"               
                #  Formated ouptput section
                
                
                
                
                
                
                
                
                
                
                
                
                
                #  Formated section ============================================================================
                else:
                    #  Restarting flux tally
            
                    
                    #1tally   4        nps =     1000665
                    #+                                    Tally for cell number 13653                                               
                    #           tally type 4    track length estimate of particle flux.      units   1/cm**2   
                    #           tally for  neutrons 
                    # number of histories used for normalizing tallies =       950000.00
                    #
                    #           volumes 
                    #                   cell:     13653                                                                                 
                    #                         2.76791E+01
                    # 
                    # energy bin:   0.          to  3.00000E-09                                                                             
                    #        cell
                    #      13653      9.60191E-09 0.4154
                    #print line            
                    if "energy bin" in line:
                        if ASSIGN_LIB:
                            Energy_tally[tally_num]=Tallies()  #  Define object tally
                            if NPS:
                                Energy_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)    
                            ASSIGN_LIB=False
                        temp_old=temp
                        temp=line.split()
                        if "total" not in line:   # energy bin:  total
                            Energy_tally[tally_num].energy_min.append(float(temp[2]))
                            Energy_tally[tally_num].energy_max.append(float(temp[4]))
                            line=input_file.next()
                            line=input_file.next()
                            temp_old=temp
                            temp=line.split()
                            # print "Energy", tally_num,float(temp[1])
                            if temp[0]=='a':
                                print "Warning:  This is a sum of tallies and not just one"
                                Energy_tally[tally_num].energy_cell.append((temp[0]))
                            else:
                                Energy_tally[tally_num].energy_cell.append(int(temp[0]))
                            Energy_tally[tally_num].energy_tally.append(float(temp[1]))
                            Energy_tally[tally_num].energy_error.append(float(temp[2]))
                            
                        else:
                           line=input_file.next()
                           line=input_file.next()
                           temp_old=temp
                           temp=line.split() 
                           Flux_tally[tally_num]=Tallies()  #  Define object tally
                           Cell=int(temp[0])
                           if (NPS):
                               Flux_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)
                           Flux_tally[tally_num].cell_num.append((Cell))
                           Flux_tally[tally_num].tally_result.append(float(temp[1]))
                           Flux_tally[tally_num].tally_error.append(float(temp[2]))
      
                    #      1tally 614        nps =     1000665
                    #      +                                     Tally for cell number 13654                                              
                    #                 tally type 4    track length estimate of particle flux.                        
                    #                 tally for  neutrons 
                    #       number of histories used for normalizing tallies =       950000.00
                    #      
                    #                 volumes 
                    #                         cell:     13654                                                                                 
                    #                               1.14878E+01
                    #       
                    #       multiplier bin:   1.00000E+00 8000         16                                                                         
                    #              cell
                    #            13654      0.00000E+00 0.0000
                    #           
                    elif "multiplier" in line:
                        #  This one is a littler tricker then the other tallies.
                        #  I have object Tallies for every tally but then within each tally I have multiple
                        #  materials assocaited for the same cell
                        #  So I created another object called Mat () to help organize everything
                        if ASSIGN_LIB:
                            Multiply_tally[tally_num]=Tallies()  #  Define object tally
                            Multiply_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)
                            Multiply_tally[tally_num].mult_mat={}  #  Library of materials for tally number
                            ASSIGN_LIB=False
                            Mat_old=1 
                        temp_old=temp
                        temp=line.split()
                       
                        Mat_num=temp[3]
                        if Mat_num != Mat_old:   # This starts a new object for a new material in the same cell   
                            Multiply_tally[tally_num].mult_mat[Mat_num] = MAT()
                        Mat_old=Mat_num
                        Multiply_tally[tally_num].mult_mat[Mat_num].multiply.append(temp[2])
                        Multiply_tally[tally_num].mult_mat[Mat_num].mtnum.append(int(temp[4]))
                        line=input_file.next()
                        temp=line.split()
                        if temp[0]=='energy':
                            print 'This is an energy depenedent multi[plier bin need more work'
                        else:
                            line=input_file.next()
                            temp_old=temp
                            temp=line.split()
                            Multiply_tally[tally_num].mult_mat[Mat_num].cell.append(float(temp[0]))
                            Multiply_tally[tally_num].mult_mat[Mat_num].tally.append(float(temp[1]))
                            #print tally_num, Mat_num,Multiply_tally[tally_num].mult_mat[Mat_num].cell, temp[0]
                            Multiply_tally[tally_num].mult_mat[Mat_num].error.append(float(temp[2]))
                    #  This will be for a cross section tally
                    #               1tally 334        nps =     1000665
                    #   +                                     Tally for cell number 63653                                              
                    #              tally type 4    track length estimate of particle flux.      units   1/cm**2   
                    #              tally for  neutrons 
                    #    number of histories used for normalizing tallies =       950000.00
                    #   
                    #              volumes 
                    #                      cell:     63653                                                                                 
                    #                            4.07496E+01
                    #    
                    #           cell
                    #         63653      1.58353E-05 0.0417
                    #               
                                                  
                    #elif "cell" in line and len(temp)==1:# and len(temp_old)==1:
                    #    print temp, temp_old
                    #    #raw_input('')
                    #    Flux_tally[tally_num]=Tallies()  #  Define object tally
                    #    Flux_tally[tally_num].nps=NPS_value # nps for particle  (Dont know if this is always avalalble)    
                    #    line=input_file.next()
                    #    print line
                    #    temp=line.split()
                    #    Flux_tally[tally_num].tally_cell=int(temp[0])
                    #    Flux_tally[tally_num].tally_result=float(temp[1])
                    #    Flux_tally[tally_num].tally_error=float(temp[2])
                    #    Tally=False
    ##    
                    elif "==============================" in line:    
                        Tally=False 
                    elif "there are no nonzero tallies in the" in line:
                        Tally=False                
                    elif "run terminated when" in line:
                        Tally=False
    
    
    
    
    
    
    Power=85 #MW
    ER=1.6022E-19 #MeV/MJ
    Q=200  #MeV/fission
    Multiply=Power*Neutron_per_fission/ER/Q/KEFF
    Flux= Multiply #  Generic flux if none is specified
    print "The Multiply is %s based on Power=%s, ER=%s Q=%s and Nu=%s, Keff=%s"%(Flux,Power,ER,Q,Neutron_per_fission,KEFF)   
     

    

    #  Convert the tally to cell information
    Total_flux={}
    Heat_flux={}
    for tally_num in Flux_tally:
      for i in range(len(Flux_tally[tally_num].cell_num)):
        Cell=Flux_tally[tally_num].cell_num[i]
        Result=Flux_tally[tally_num].tally_result[i]
        Error=Flux_tally[tally_num].tally_error[i]
        Total_flux[Cell]=Tallies()
        Total_flux[Cell].error=Error
        if(Multple_value):
            Total_flux[Cell].result=Result*Multiply
        else:
            Total_flux[Cell].result=Result
        if '6' in "%s"%(tally_num):
            Heat_value=Flux_tally[tally_num].tally_result[i]*Multiply*1.60217646E-13
            Heat_flux[Cell]=Heat_value
        # Convert the Energy bin information so that cell is the library call word instead of tally

    Energy_bin={}
    Cell_old=0
    for tally_num in Energy_tally:                        
        for i in range(len(Energy_tally[tally_num].energy_tally)):
           Cell=Energy_tally[tally_num].energy_cell[i]
           Energy_min=Energy_tally[tally_num].energy_min[i]
           Energy_max=Energy_tally[tally_num].energy_max[i]
           Result= Energy_tally[tally_num].energy_tally[i]
           Error=Energy_tally[tally_num].energy_error[i]
           if Cell_old!=Cell:
              Energy_bin[Cell]=Tallies()
           Energy_bin[Cell].energy_min.append(Energy_min)
           Energy_bin[Cell].energy_max.append(Energy_max)
           Energy_bin[Cell].energy_tally.append(Result)
           Energy_bin[Cell].energy_error.append(Error)
           Cell_old=Cell

    
    
    print "Multiply_tally has the objects .mult_cell, .mult_mat, .mult_value, .mult_reaction, ,multi_micro=[] "
    for tally_num in Multiply_tally:
        for i in range(len(Multiply_tally[tally_num].mult_cell)):
            cell_num=Multiply_tally[tally_num].mult_cell[i]
            for flux_num in Total_flux:
                if cell_num==flux_num:
                   Material=Multiply_tally[tally_num].mult_mat[i]
                   Reaction=Multiply_tally[tally_num].mult_reaction[i]
                   
                   Result=Multiply_tally[tally_num].mult_tally[i]
                   Result_error=Multiply_tally[tally_num].mult_error[i]
                   Flux=Total_flux[flux_num].result
                   Flux_error=Total_flux[flux_num].error
                   #print tally_num, cell_num, Flux, Result
                   if (Multple_value):
                       Micro=Result*Multiply/(Flux+1E-15) 
                   else:
                        Micro=Result/(Flux+1E-35)
                   Micro_error=((Result_error)**2+(Flux_error)**2)**.5
                   Multiply_tally[tally_num].multi_micro.append(Micro)
                   Multiply_tally[tally_num].micro_error.append(Micro_error)
                   #print cell_num, Material, Reaction, Result, Flux, Micro 
                   
            
        
    
    
    
    
    #for i in Energy_bin:
    #    print i 
    #    for j in Energy_bin[i].energy_tally:
    #        print Energy_bin[i].energy_tally
    if RETURN_HEAT:
        return(Energy_bin,Total_flux,Heat_flux)
    else:
         return(Energy_bin,Total_flux,Multiply_tally)
          
        














#  Get heating tally
# ==================================GET TALLY====================================================
def get_heating_tally(Result_file,Multple_value,RETURN_HEAT):
    '''#!/usr/bin/env python
    #  Results file is the file where the results were saved to i.e mcnp output file
    #  The Multiple_value file is if to use the Multiple scalled oppripriate or not.
    #
    #
    #
    #     Code: get_tally.py 
    #
    #     Author:  Joshua Peterson
    #   
    #     Date:  Second week at work at ORNL
    #
    #     Description:  This gets data from MCNP tallies and parses to screen or processes ect.
    #     
    #     Date:  Week after Josh left made it an object of libraries for easier use
    ########################################
   ''' 
    
    
    
    
    
   
    
    #################   Check for the write inport format
    try:
        input_file = open(Result_file, 'r')
    except IndexError:
        print "ERROR 1:  The command should read ]$ get_tally.py [output.o] "
        sys.exit()
        
    PRINT_MULTIPLY=True
    #  Flux tally used to create tally objects
    Flux_tally={}
    #
    Neutron_per_fission=2.43
    #
    KEFF=1.0
    #
    #
    for line in input_file: 
        #  Gets nu from inpt
        if "the average number of neutrons produced per fission" in line:
            temp=line.split()
            Neutron_per_fission=float(temp[10])
            print "Nu is equal to ", Neutron_per_fission
        #  Gets the final keff
        if "= final keff =" in line: 
            #  Split line a seperate by space
            temp=line.split()
            #  There is keff) so seperating the ) from the keff value
            temp=temp[len(temp)-1].split(')')
            # saving KEFF for results
            KEFF=float(temp[0])
        
        #  This is where it looks for tally information
        #  Fluctuation chart is at the end and has not tally information
        if "1tally" in line and "fluctuation charts" not in line:
            #  This is a way to continue to loop through the results until the end of the tally is found
            Tally=True
            #  Creates strings objects from the line
            temp=line.split()
            #  Saving the tally number
            tally_num=int(temp[1])
            Flux_tally[tally_num]={}  #  Define object tally
            if "nps" in line:
                NPS=True
                # Saving the NPS number;  Never use it though
                NPS_value=temp[4]
            else:
                NPS=False
            # This statment Assign lib is used so that a new array of Tallies can be created without overwriting other information
            #  There is probably a cleaner way of doing this but I do not know
            ASSIGN_LIB=True 
            while(Tally):
                line=input_file.next()
                temp=line.split()
                if "cell" in line and len(temp)==2:
                    Cell=int(temp[1])
                    line=input_file.next()
                    temp=line.split()
                    #cell  8901
                    #                1.14575E+04 0.0098
                    #
                    #cell  8902
                    #                8.33106E+02 0.0424
                    #
                    #cell  8903
                    #                4.55796E+01 0.0984 
                    if len(temp)==2 and "cell" not in line:
                        Flux_tally[tally_num][Cell]=Tallies()
                        Flux_tally[tally_num][Cell].tally_result=float(temp[0])
                        Flux_tally[tally_num][Cell].tally_error=float(temp[1])



                

                if "==============================" in line:    
                    Tally=False 
                if "there are no nonzero tallies in the" in line:
                    Tally=False
                if "run terminated when" in line:
                    Tally=False
                    print "run terminated"               
                #  Formated ouptput section
                
                
                
                
                
                
                
                
                
                
                
                
                
                
    
    
    
    Power=85 #MW
    ER=1.6022E-19 #MeV/MJ
    Q=200  #MeV/fission
    Multiply=Power*Neutron_per_fission/ER/Q/KEFF
    Flux= Multiply #  Generic flux if none is specified
    print "The Multiply is %s based on Power=%s, ER=%s Q=%s and Nu=%s, Keff=%s"%(Flux,Power,ER,Q,Neutron_per_fission,KEFF)   
     

    

    #  Convert the tally to cell information
    #Total_flux={}
    #Heat_flux={}
    #for tally_num in Flux_tally:
    #    #This is the last number in the series
    #    last_number=("%s"%(tally_num))[-1:]
    #    print last_number
    #    #raw_input('pause')
    #    
    #    
    #    
    #    for i in range(len(Flux_tally[tally_num].cell_num)):
    #        Cell=Flux_tally[tally_num].cell_num[i]
    #        Result=Flux_tally[tally_num].tally_result[i]
    #        Error=Flux_tally[tally_num].tally_error[i]
    #      
    #      
    #        #  This is if it is a flux tally
    #        if '4' in "%s"%(tally_num):
    #            Total_flux[Cell]=Tallies()    
    #            Total_flux[Cell].error=Error  
    #            Total_flux[Cell].result=Result
    #        elif '6' in "%s"%(tally_num):
    #            Heat_value=Flux_tally[tally_num].tally_result[i]*Multiply*1.60217646E-13
    #            Heat_flux[Cell]=Heat_value
    #        elif '7' in "%s"%(tally_num):
    #            print tally_num
    #        # Convert the Energy bin information so that cell is the library call word instead of tally
    #
    #pickle.dump=open('pickle.dmp','w')
    #pickle.dumps(Flux_tally)
    return(Flux_tally)
    


















# ==================================WRITE TALLY====================================================
#  This writes tallys in mcnp  
##############################################################################################
def write_tally(Material, Energy_tally,CELLS,Reaction_rate, Tally_type,Start,File_name):  
    #  write_tally: will write, cell, energy, and reaction_rate tally for mcnp
    # 
    #  NOTE:  CHANGED so that only one tally number per request.  This is because I was exedding the maximum
    #  tallies for MCNP or at least it looked like that
    #
    #Material is the material used for the material multiplier tally
    #Energy is the energy bin structure used
    #CELLS are the cells that you want to write the tally for
    #Reactor rate are the reactons you want to look at
    #Tally_type is the type of tally you want
    NUM_CELLS_FORMAT=4 #Format of fm card to work with mcnp style
    # Making sure the input file is there
    Tally_start=Start   
    try:
       input_file = open(File_name, 'r')
       output_file=open('Temp.txt','w')
    except IndexError:
       print "ERROR 101:  The command should read ]$ MCNP_to_Heating_Decay.py [mcnp.i] "
       File=raw_input('Type in the name of the file ')
       try:
           input_file=open(File,'r')
       except IOError:
           print "File did not exist exiting"
           sys.exit()
    
    i_new=Tally_start
    for tally in Tally_type:
        
    # Number of Cells per rom

        if tally=='Reaction_rate':
            # Mat Number used for cross section tally
            Mat_num=[] 
            # Writing out material cards
            for i in range(len(Material)): #Go through all materials and create material card for each one by it self
               # Start number plus i
               Mat_num.append(i+Start)
               # Write out material information
               output_file.write( "m%i    %s.70c   1.00000 \n"%(Mat_num[i],Material[i]) ) #  Writing out material card
            

    
            #  Writing out f4 tallys with multiplies to be used for obtaining cross sections
            output_file.write(  "f%i4c  Tally for ALL CELLS  \n"%(i_new)       )
            output_file.write(  "f%i4:n  "%(i_new))
            for i in range(len(CELLS)):
                #  Comment card
                output_file.write(  " %i  "%(CELLS[i])       )
                # Tally f4 card with increase number
                #  Starting the fm card
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            output_file.write("fm%i4 \n"%(i_new))
            # For each material
            for j in range(len(Mat_num)):
                # For each reaction type specified
                for k in range(len(Reaction_rate)):
                    
                    #  Write for material number and reaction with no other multiplication
                    output_file.write("        (1   %i  %i)\n"%(Mat_num[j], Reaction_rate[k])    ) 
                    #  Return after five steps if not at end 
            output_file.write('c\nc\n')
            i_new=i_new+1
        
        elif tally=='Energy':
            #  Energy tally
            #  Writing out energy depedent tallies
            output_file.write(  "f%i4c  Energy tally for all cells  \n"%(i_new)) #Writing out energy depedent flux tally
            output_file.write( "f%i4:n  "%(i_new))
            
            for i in range(len(CELLS)):
                #  Comment card
                
                #flux card
                output_file.write( " %i "%(CELLS[i]))       
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            # Energy card initally without any of the group structurs
            output_file.write(  "E%i4   "%(i_new) )                     #
            #  GOes through all the group structures
            for j in range(len(Energy_tally)):                                              #
               output_file.write(  "%.4e "%(Energy_tally[j]))                           #Looping over energy
               #  If j reached format row and it is not the last entry 
               if j%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and j!=len(Energy_tally)-1:               #
                    #  Go to next line
                    output_file.write( "\n      ")                                          #
            output_file.write("\nc\n")                                                #  Writing spaces between
            #  i_new is the max of the i
            i_new=i_new+1
            #  Writing out f4 tallies to obtain flux
        
        elif tally=='Flux':
            # Flux tally
            #  Loop through all of the cells
            output_file.write("f%i4c  Flux tall for all cells \n"%(i_new))
            output_file.write("f%i4:n  "%(i_new))
            for i in range(len(CELLS)):
                #  Comment card
                # Flux card for each of the cells
                output_file.write( " %i "%(CELLS[i]))
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            i_new=i_new+1
        elif tally=='Heat':
            #Heat tally
            #Loop through all of the cells
            output_file.write("f%i6c  Heat tally for all cells (MeV/g/source particle) \n"%(i_new))
            output_file.write("f%i6:n,p "%(i_new))
            for i in range(len(CELLS)):
                #  Comment card
                # Flux card for each of the cells
                output_file.write( " %i "%(CELLS[i]))
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            i_new=i_new+1            

        elif tally=='Neutron_Heat':
            #Heat tally
            #Loop through all of the cells
            output_file.write("f%i6c  Heat tally for all cells (MeV/g/source particle) \n"%(i_new))
            output_file.write("f%i6:n "%(i_new))
            for i in range(len(CELLS)):
                #  Comment card
                # Flux card for each of the cells
                output_file.write( " %i "%(CELLS[i]))
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            i_new=i_new+1  

        elif tally=='Gamma_Heat':
            #Heat tally
            #Loop through all of the cells
            output_file.write("f%i6c  Heat tally for all cells (MeV/g/source particle) \n"%(i_new))
            output_file.write("f%i6:p "%(i_new))
            for i in range(len(CELLS)):
                #  Comment card
                # Flux card for each of the cells
                output_file.write( " %i "%(CELLS[i]))
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            i_new=i_new+1                      
        
        elif tally=='Fission_Energy':
            #Heat tally
            #Loop through all of the cells
            output_file.write("f%i7c  Heat tally for all cells (MeV/g/source particle) \n"%(i_new))
            output_file.write("f%i7:n "%(i_new))
            for i in range(len(CELLS)):
                #  Comment card
                # Flux card for each of the cells
                output_file.write( " %i "%(CELLS[i]))
                if i%NUM_CELLS_FORMAT==NUM_CELLS_FORMAT-1 and i!=len(CELLS)-1:
                    output_file.write("\n       ")
            output_file.write("\n")
            i_new=i_new+1 
                    
        else:
            print 'ERROR write tally, the type of tally you want does not exist in this file'
            sys.exit()
    
    
 
    output_file.close()
    os.system('rm %s'%(File_name+'.new.i'))
    os.system('cat %s %s > %s'%(File_name,'Temp.txt',File_name+'.new.i'))
    print "Finished writing tally"    








    
