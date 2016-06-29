#!/usr/bin/env python
#
#
#     Code: Generic_ARP_Origen_OPUS.py
#
#     Author:  Joshua Peterson
#
#     Date:    Feb 25
#
#     Description: This code create the tables needed for the NRC report in 2014.  It uses the arp generated cross sections
#
########################################



import sys
import os

# name your file tag here
file_tag='pwr_ref'

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
       print "ERROR 780: Number of cycles not equal to irradation times irr_time=%s, average_power=%s, num_lib=%s,num_cycle=%s"%(len(irr_time),len(average_pow),len(num_lib),num_cycle)
       sys.exit()


   # Witing opus library:  See page D1.3.5 in Scale manual for better understanding
   output_file.write("=arp     \n")
   output_file.write("%s  \n"%(lib_name))
   output_file.write("%.7E      \n"%(initenr))
   output_file.write("%i        \n"%(num_cycle))
   for time in irr_time:
       output_file.write("%.7E \n"%(time))
   for pow in average_pow:
       output_file.write("%.7E       \n"%(pow))
   for lib in num_lib:
       output_file.write("%i        \n"%(lib))
   output_file.write("%.7E   \n"%(mod_den))
   output_file.write("ft33f001 \n")
   output_file.write("end      \n")


# ==================================WRITE ORIGIN====================================================
def write_origen(USE_FT33,DECAY_STEPS,IRRADIATE,FORMAT_ROW,TITLE,UNITS,IRRADIATION, \
              DECAY,FINAL_DECAY,MIX_NUM,output_file,Isotopes,Frac,Mat,FISSION,FLUX,Power_instead_Flux):


    # Number of isotopes used
    FACTOR=1.151
    NUM_ISO=len(Isotopes)
    NFISW=len(FISSION) # Number of fission enteries above

    #  Used for tracking decay steps
    DECAY_STEPS_OLD=DECAY_STEPS
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
           #  This is to allow plotting larger final decays then specified
           if irr ==len(IRRADIATION)-1 and len(FINAL_DECAY)>1:
              DECAY_STEPS=len(FINAL_DECAY)

           output_file.write('%s \n' %(TITLE))
           #  NOTE in second loop A16 is not there
           if irr==0:
                output_file.write('3$$ 33 a3 %i  27 a16 2 a33 47 e t \n'%(irr+1))
           else:
                #  IF USE_FT33 is true then incrementally use the ft33f001 file from Trition
                if USE_FT33:
                    output_file.write('3$$ 33 a3 %i  27 a16 0 a33 47 e t \n'%(irr+1))
                else:
                    output_file.write('3$$ 33 a3 %i  27 a16 0 a33 47 e t \n'%(irr+1))
           output_file.write('35$$ 0 t \n')
           #  For irr=0 the number of isotopes are written here.  After that isotopes are not inputed
           if Power_instead_Flux:
              if irr==0:
                   output_file.write('56$$ %s %s  a10 0 a13 %s a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE,NUM_ISO))  #a3 is for flux being read in
              else:
                  output_file.write('56$$ %s %s a6 1 a10 1 a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE))# a10 1 a13 not there
           else:
               if irr==0:
                    output_file.write('56$$ %s %s a3 1 a6 1 a10 0 a13 %s a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE,NUM_ISO))  #a3 is for flux being read in
               else:
                   output_file.write('56$$ %s %s a3 1 a6 1 a10 %s a15 3 a18 1 e \n'%(IRRADIATE,IRRADIATE,DECAY_STEPS))# a10 1 a13 not there
           #This is where the initall time from the previous run is used.  So the output is nice looking
           output_file.write('57** %10.6E a3 1e-05 0.1666667  e \n'%(TIME))#time[i]))  #used to get better results
           output_file.write('95$$ 1 t \n')
           #  Input stuff into the comment line
           output_file.write('Cycle %i %s \n' %(irr+1,TITLE))

           # Writing out average power instead of flux
           if Power_instead_Flux:
               #  Writeing the flux out which is a function of burnup
               #print FLUX
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
           if irr==len(IRRADIATION)-1:
                output_file.write('56$$ a2 %s a6 1 a10 10 a15 3 a17 2 e \n'%(DECAY_STEPS)) # changed by hu, re-set time unit to days.
                #output_file.write('56$$ a2 %s a6 1 a10 10 a14 5 a15 3 a17 2 e \n'%(DECAY_STEPS))
           else:
               output_file.write('56$$ a2 %s a6 1 a10 10 a15 3 a17 2 e \n'%(DECAY_STEPS_OLD)) # changed by hu, re-set time unit to days.
               #output_file.write('56$$ a2 %s a6 1 a10 10 a14 5 a15 3 a17 2 e \n'%(DECAY_STEPS_OLD))
           #  This writes the next time incrementally
           #output_file.write('57** %10.6E a3 1e-05 e \n'%(TIME))
           output_file.write('57** 0 a3 1e-05 e \n')
           output_file.write('95$$ 0 t \n')
           output_file.write('Decay %i %s for flux %s \n' %(irr+1,TITLE,FLUX[irr]))
           output_file.write('Decay for experiment \n')
           output_file.write('60**  ')
           Count_time=TIME
           #  Doing a intremental step to specified decay with the number of steps being DECAY steps

           verySmallSteps=0.00001
           Decay_Count_time=0
           smallDecaySteps=verySmallSteps
           for t in range(DECAY_STEPS):
               #  if it is the last decay step
               if irr ==len(IRRADIATION)-1:
                   #  This is if the user just specifies the final decay or how the decay is broken up
                   if type(FINAL_DECAY)==int or type(FINAL_DECAY)==float:
                       #break it up evenly
                       # break it up logrithmitacllly
                       #New_Count_time=Count_time+(FINAL_DECAY/FACTOR**(float(DECAY_STEPS)))*FACTOR**(t+1)
                       Decay_Count_time=(FINAL_DECAY/FACTOR**(float(DECAY_STEPS)))*FACTOR**(t+1)
                   else:
                       #New_Count_time=Count_time+FINAL_DECAY[t]
                       Decay_Count_time=FINAL_DECAY[t]
                       print Decay_Count_time
                       print "Warning Warning FINAL_DECAY IS NOT INCREMENTAL BUT EXPLICIT"
                       #raw('Enter to continue')
                       print "Final decay step", Count_time,FINAL_DECAY[t]
               else:

                   Decay_Count_time=(DECAY[irr]/3**(float(DECAY_STEPS)-(t+1)))


               output_file.write(' %10.6E Test'%(Decay_Count_time+smallDecaySteps))
               smallDecaySteps+=verySmallSteps
               if t%FORMAT_ROW==FORMAT_ROW-1:
                    output_file.write('\n       ')
           output_file.write( ' \n')
           #  Saving the last inputedtime step
           #TIME=New_Count_time
           output_file.write('61** f0.05 \n')
           output_file.write('65$$ \n')
           output_file.write('\'Gram-Atoms   Grams   Curies   Watts-All   Watts-Gamma \n')
           output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')
           output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')
           output_file.write(' 3z   1   0   0   3z   3z   3z   6z \n')

           #   Saving information to the ft71f001 card
           output_file.write(' 81$$ a1 2 a3 26 e  \n ')
           output_file.write(' 82$$   ')
           for step in range(DECAY_STEPS):
               output_file.write(' 2 ')
               if step%FORMAT_ROW==FORMAT_ROW-1:
                  output_file.write('\n         ')
           output_file.write(' e\n')

           output_file.write('83**                                                                  \n')
           output_file.write('2.0000000e+07 1.4000000e+07 1.2000000e+07 1.0000000e+07 8.0000000e+06 \n')
           output_file.write('7.5000000e+06 7.0000000e+06 6.5000000e+06 6.0000000e+06 5.5000000e+06 \n')
           output_file.write('5.0000000e+06 4.5000000e+06 4.0000000e+06 3.5000000e+06 3.0000000e+06 \n')
           output_file.write('2.7500000e+06 2.5000000e+06 2.3500000e+06 2.1500000e+06 2.0000000e+06 \n')
           output_file.write('1.8000000e+06 1.6600000e+06 1.5700000e+06 1.5000000e+06 1.4400000e+06 \n')
           output_file.write('1.3300000e+06 1.2000000e+06 1.0000000e+06 9.0000000e+05 8.0000000e+05 \n')
           output_file.write('7.0000000e+05 6.0000000e+05 5.1200000e+05 5.1000000e+05 4.5000000e+05 \n')
           output_file.write('4.0000000e+05 3.0000000e+05 2.6000000e+05 2.0000000e+05 1.5000000e+05 \n')
           output_file.write('1.0000000e+05 7.5000000e+04 7.0000000e+04 6.0000000e+04 4.5000000e+04 \n')
           output_file.write('3.0000000e+04 2.0000000e+04 1.0000000e+04 e                           \n')
           output_file.write('84**                                                                  \n')
           output_file.write('2.0000000e+07 6.3763000e+06 3.0119000e+06 1.8268000e+06               \n')
           output_file.write('1.4227000e+06 9.0718000e+05 4.0762000e+05 1.1109000e+05 1.5034000e+04 \n')
           output_file.write('3.0354000e+03 5.8295000e+02 1.0130000e+02 2.9023000e+01 1.0677000e+01 \n')
           output_file.write('3.0590000e+00 1.8554000e+00 1.3000000e+00 1.1253000e+00 1.0000000e+00 \n')
           output_file.write('8.0000000e-01 4.1399000e-01 3.2500000e-01 2.2500000e-01 1.0000000e-01 \n')
           output_file.write('5.0000000e-02 3.0000000e-02 1.0000000e-02 1.0000000e-05 e             \n')



           output_file.write('t \n')

           for step in range(DECAY_STEPS):
               output_file.write('56$$ 0 0 a10  %i e t \n'%(step+1))
           #  For the last decay step need to add this card to say stop.
           if irr==len(IRRADIATION)-1:
               output_file.write('56$$ f0 t \n')
               output_file.write('end \n')
           else:
               #  This is the input file for the next step
               output_file.write('56$$ 0 1 a6 3 a10 %i a17 4 e t \n'%(DECAY_STEPS))
               output_file.write('60** 0 t \n')


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

    if unit=='GSPECTRUM':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=%s \n'%(unit))
        output_file.write('UNITS=PARTICLES \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i "$INPDIR/%s_%s.plt" \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')


    elif unit=='NSPECTRUM':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=%s \n'%(unit))
        output_file.write('UNITS=PARTICLES \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i "$INPDIR/%s_%s.plt" \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')

    elif '_' in unit:
        UNITS,TYPARAMS=unit.split('_')
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=%s \n'%(TYPARAMS))
        output_file.write('UNITS=%s \n'%(UNITS))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('NRANK=100 \n')

        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')

    elif unit=='Grams':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        # below is the list of 117 nuclides important to decay heat, reactivity, mass, burnup credit
        #and MACCS (ranked by J. Hu).
        output_file.write('symnuc=Ag-109 Am-241 Am-242 Am-242m Am-243 Ba-137 Ba-137m Ba-138 Ba-139    \n')
        output_file.write(' Ba-140 Ce-140 Ce-141 Ce-142 Ce-143 Ce-144 Cm-242 Cm-243 Cm-244      \n')
        output_file.write(' Cm-245 Co-58 Co-60 Cs-133 Cs-134 Cs-136 Cs-137 Eu-151 Eu-153        \n')
        output_file.write(' Eu-154 Eu-155 Gd-155 I-131 I-132 I-133 I-134 I-135 Kr-85 Kr-85m     \n')
        output_file.write(' Kr-87 Kr-88 La-139 La-140 La-141 La-142 Mo-100 Mo-95 Mo-97 Mo-98    \n')
        output_file.write(' Mo-99 Nb-93m Nb-95 Nb-97 Nb-97m Nd-143 Nd-144 Nd-145 Nd-147 Nd-148  \n')
        output_file.write(' Np-237 Np-239 Pm-147 Pr-141 Pr-143 Pr-144 Pr-144m Pu-238 Pu-239     \n')
        output_file.write(' Pu-240 Pu-241 Pu-242 Rb-86 Rb-88 Rh-103 Rh-103m Rh-105 Rh-106       \n')
        output_file.write(' Ru-101 Ru-103 Ru-105 Ru-106 Sb-125 Sm-147 Sm-149 Sm-150 Sm-151      \n')
        output_file.write(' Sm-152 Sr-89 Sr-90 Sr-91 Sr-92 Tc-99 Tc-99m Te-125m Te-127 Te-127m  \n')
        output_file.write(' Te-129 Te-129m Te-131 Te-131m Te-132 U-234 U-235 U-236 U-238 Xe-132 \n')
        output_file.write(' Xe-133 Xe-134 Xe-135 Xe-135m Xe-136 Y-90 Y-91 Y-91m Y-92 Y-93       \n')
        output_file.write(' Zr-93 Zr-95 Zr-97   end                                             \n')

        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')

    elif unit=='Curies':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        # list of vogtle 69 nuclides.
        output_file.write('symnuc=Am-241 Ba-137m Ba-139 Ba-140 Ce-141 Ce-143 Ce-144 Cm-242 Cm-244 Co-58   \n')
        output_file.write(' Co-60 Cs-134 Cs-136 Cs-137 I-131 I-132 I-133 I-134 I-135 Kr-85 Kr-85m   \n')
        output_file.write(' Kr-87 Kr-88 La-140 La-141 La-142 Mo-99 Nb-95 Nb-97 Nb-97m Nd-147 Np-239 \n')
        output_file.write(' Pr-143 Pr-144 Pr-144m Pu-238 Pu-239 Pu-240 Pu-241 Rb-86 Rb-88 Rh-103m  \n')
        output_file.write(' Rh-105 Rh-106 Ru-103 Ru-105 Ru-106 Sr-89 Sr-90 Sr-91 Sr-92 Tc-99m      \n')
        output_file.write(' Te-127 Te-127m Te-129 Te-129m Te-131 Te-131m Te-132 Xe-133 Xe-135      \n')
        output_file.write(' Xe-135m Y-90 Y-91 Y-91m Y-92 Y-93 Zr-95 Zr-97      end                 \n')

        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s1.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')

    elif unit=='CURIES':
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
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s2.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')

    elif unit=='WATTS':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('NRANK=100 \n')

        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n')


    elif unit=='GAMAWATTS':
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('NRANK=100 \n')

        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n\n')

    else:
        output_file.write('\n=opus \n')
        output_file.write('LIBUNIT=%s \n'%(LIBUNIT))
        output_file.write('TYPARAMS=NUCLIDES \n')
        output_file.write('UNITS=%s \n'%(unit))
        output_file.write('LIBTYPE=ALL \n')
        output_file.write('TIME=DAYS \n')
        output_file.write('NRANK=100 \n')
        # list of vogtle 69 nuclides.
        output_file.write('symnuc=Am-241 Ba-137m Ba-139 Ba-140 Ce-141 Ce-143 Ce-144 Cm-242 Cm-244 Co-58   \n')
        output_file.write(' Co-60 Cs-134 Cs-136 Cs-137 I-131 I-132 I-133 I-134 I-135 Kr-85 Kr-85m   \n')
        output_file.write(' Kr-87 Kr-88 La-140 La-141 La-142 Mo-99 Nb-95 Nb-97 Nb-97m Nd-147 Np-239 \n')
        output_file.write(' Pr-143 Pr-144 Pr-144m Pu-238 Pu-239 Pu-240 Pu-241 Rb-86 Rb-88 Rh-103m  \n')
        output_file.write(' Rh-105 Rh-106 Ru-103 Ru-105 Ru-106 Sr-89 Sr-90 Sr-91 Sr-92 Tc-99m      \n')
        output_file.write(' Te-127 Te-127m Te-129 Te-129m Te-131 Te-131m Te-132 Xe-133 Xe-135      \n')
        output_file.write(' Xe-135m Y-90 Y-91 Y-91m Y-92 Y-93 Zr-95 Zr-97      end                 \n')

        if type(MINPOSITION)!=int:
            output_file.write('nposition = %s end \n'%(MINPOSITION[1]))
            MINPOSITION=MINPOSITION[0]
        output_file.write('MINPOSITION=%i \n'%(MINPOSITION))
        output_file.write('MAXPOSITION=%i \n'%(MAXPOSITION))
        output_file.write('end \n\n')
        output_file.write('=shell \n')
        output_file.write('  mv _plot*000%i $INPDIR/%s_%s.plt \n'%(opus_counter,cell_num,unit))
        output_file.write('end \n\n')
    opus_counter=opus_counter+1
    return(opus_counter)

#================ User input
USE_FT33=False
#  Number of steps per decay
DECAY_STEPS=7
#  These are the number of steps between each cross section WARNING Keep as 1 for now.
Steps_between_irradation=1
# Number of sub steps for irradation
IRRADIATE=10
#  Number of Steps per cycle for cross sections being used
#  How many inputs per row.  Origen has a max limit so this should be small
FORMAT_ROW=4
# Origen Title
TITLE='Irrdation decay'
#  Burnup desired for each step
burnupPerStep=2 #GWd/MTHM
#  Is you want to deplete by power instead of flux
Power_instead_Flux=True
#
Time_increament=['Log','Linear','Table']
#  Use new cross section library or old one
# NEW_LIBRARY=True
NEW_LIBRARY=False

#Choose if the user wants to specify irradation time instead of specific power
#IrradationInsteadOfPower=True

# Choose if you want to use burnup (True) or specific power (False) to control the steps
UseBurnup=False



if NEW_LIBRARY:

    #Lib_name='bwr8x8_4_6'
    #Lib_name='bwr10x10_4_6'
    Lib_name='w17vplus'
    #Lib_name='mox'

else:
    print "Why are you using an old library"
    Lib_name='w17x17'
    #Lib_name='ge9x9-7'
    #Lib_name='ge10x10-8'
   # Lib_name='ge8x8-4'
   # Lib_name='ge7x7-0'

#  =================
# Isotopes being irradated
if Lib_name=='mox':
    Isotopes=[92234,92235,92236, 92238, 94239,94240, 94241, 94242, 8016]
    # Material number associated with the isotope (actinides=2)
    Mat=[2,2,2,2,2,2,2,2,0]
    #  This allows you to use the flux of mcnp but the cross sections from keno for incremental locations on the FT33 file
    SCALE=1E4
    Frac=[0.002*SCALE,0.166*SCALE,0.001*SCALE,83.984*SCALE,3.740*SCALE,0.237*SCALE,0.016*SCALE,0.004*SCALE,11.85*SCALE]

else:

    Isotopes=[92234,92235,92236, 92238]
    # Material number associated with the isotope (actinides=2)
    Mat=[2,2,2,2]
    #  This allows you to use the flux of mcnp but the cross sections from keno for incremental locations on the FT33 file
for times in Time_increament:
    UNITS=['Curies','CURIES', 'Grams', 'WATTS','GSPECTRUM','NSPECTRUM','GAMWATTS']
    if times=='Linear':
        UNITS=['GramsLinear']
        FILE_NAME='%s_Origen_Linear.inp'%(file_tag)
        # Opening the file
        output_file = open(FILE_NAME, 'w')
    elif times=='Table':
        FILE_NAME='%s_Origen_Table.inp'%(file_tag)
        # Opening the file
        output_file = open(FILE_NAME, 'w')
    else:
        print "Log result"
        FILE_NAME='%s_Origen.inp'%(file_tag)
        # Opening the file
        output_file = open(FILE_NAME, 'w')


    #  Final decay time (Not completely sure what this is)
    #FINAL_DECAY=[0.3, 1, 2, 3, 4, 8, 12, 16, 32, 48, 64, 128, 192, 256, 512, 768, 1024, 2048, 3072, 4096, 6144, 12288, 18432, 24576, 36864, 73728]
    FINAL_DECAY=[0.01, 0.1, 1, 90, 180, 365, 730, 1825, 2048, 3072, 3650, 5475, 12288, 18432, 24576, 36500, 54750, 73000]
    if UNITS[0]=='GramsLinear' or UNITS[0]=='CuriesLinear_ELEMENT':
        print "Units is GramsLinear"
        #FINAL_DECAY=[0, 1825, 3650, 5475, 7300, 9125, 10950, 12775, 14600, 16425, 18250, 20075, 21900, 23725, 25550, 27375, 29200, 31025, 32850, 34675, 36500, 38325, 40150, 41975, 43800, 45625, 47450, 49275, 51100, 52925, 54750, 56575, 58400, 60225, 62050, 63875, 65700, 67525, 69350, 71175, 73000]
        FINAL_DECAY=[0, 2, 10, 90, 180, 365, 730, 1825, 2048, 3072, 3650, 5475, 7300,  10950,  14600,  18250, 20075,  25550,  29200,  32850,  36500,  40150,  43800,  47450,  51100,  54750,  58400, 62050,  65700,  69350,  73000]
    if times=='Table':
        #FINAL_DECAY=[0.365000,3.65000,36.5000,365.000,3650,36500,73000] #josh
        FINAL_DECAY=[0.208,1,90, 365,1825,3650,18250,36500,73000] #hu
        #FINAL_DECAY=[0.365,3.65,36.5,365,1825] #hu

    #  Fission reactions to be considered
    FISSION=[922320, 922330, 922340, 922350,
                             922360, 922370, 922380, 932370, 932380, 942380, 942390, 942400,
                             942410, 942420, 952410, 952430, 962420, 962440, 962450, 962460,
                             962480]

    if 'w17' in Lib_name:

    # Moderator Density
        Mod_den=0.7332
        Burnup=[28,39,47,72] #GWd/MTHM
        Enrichment=[2.94,3.61,4.28,5.0] #wt% U235
        Num_cycles=[3,3,3,3] # Number of cycles (fixed at three)
        #This allows the uses to specify if he wants to use specific power or irradation time to acheive the desired burnup specified above.
        if UseBurnup:

            Average_power=[0,0,0,0]
            Average_power[0]=[38,38,38]
            Average_power[1]=[38,38,38]
            Average_power[2]=[38,38,38]
            Average_power[3]=[38,38,38]
        else:
            Irradiation_time=[0,0,0,0]
            Irradiation_time[0]=[300, 200, 250]
            Irradiation_time[1]=[300, 200, 250]
            Irradiation_time[2]=[300, 200, 250]
            Irradiation_time[3]=[100, 60, 80]

            Average_power=[0,0,0,0]
            Average_power[0]=[37.33,37.33,37.33]
            Average_power[1]=[38.66,38.66,38.66]
            Average_power[2]=[62.66,62.66,62.66]
            Average_power[3]=[30,40,50]

            Decay_time=[0,0,0,0]
            Decay_time[0]=[45,45,45]
            Decay_time[1]=[45,45,45]
            Decay_time[2]=[45,45,45]
            Decay_time[3]=[45,45,45]



    # Cross section library name
    elif Lib_name=='mox':
        Burnup=[40] #GWd/MTHM
        Mod_den=0.7332
        # Enrichment of the fuel
        Enrichment=['4.25'] #wt% U235
        Num_cycles=[3] # Number of cycles (fixed at three)
        #This allows the uses to specify if he wants to use specific power or irradation time to acheive the desired burnup specified above.
        if UseBurnup:
            Average_power=[0]
            Average_power[0]=[38,38,38]

        else:
            Irradiation_time=[0]
            Irradiation_time[0]=[300, 200, 250]
            Average_power=[0]
            Average_power[0]=[38,38,38]

        Decay_time=[0]
        Decay_time[0]=[45,45,45]

    else :
    # Moderator Density
        Mod_den=0.45
        Burnup=[5,15,25,35,45,55] #GWd/MTHM
        Enrichment=[3.0,3.0,3.0,3.0,3.0,3.0] #wt% U235
        Num_cycles=[3,3,3,3,3,3] # Number of cycles (fixed at three)
        #This allows the uses to specify if he wants to use specific power or irradation time to acheive the desired burnup specified above.
        if UseBurnup:

            Average_power=[0,0,0,0,0,0]
            Average_power[0]=[24,24,24]
            Average_power[1]=[24,24,24]
            Average_power[2]=[24,24,24]
            Average_power[3]=[24,24,24]
            Average_power[4]=[24,24,24]
            Average_power[5]=[24,24,24]

        else:
            Average_power=[0,0,0,0,0,0]
            Average_power[0]=[24,24,24]
            Average_power[1]=[24,24,24]
            Average_power[2]=[24,24,24]
            Average_power[3]=[24,24,24]
            Average_power[4]=[24,24,24]
            Average_power[5]=[24,24,24]

            Irradiation_time=[0,0,0,0,0,0]
            Irradiation_time[0]=[300, 200, 250]
            Irradiation_time[1]=[300, 200, 250]
            Irradiation_time[2]=[300, 200, 250]
            Irradiation_time[3]=[300, 200, 250]
            Irradiation_time[4]=[300, 200, 250]
            Irradiation_time[5]=[300, 200, 250]

        Decay_time=[0,0,0,0,0,0]
        Decay_time[0]=[45,45,45]
        Decay_time[1]=[45,45,45]
        Decay_time[2]=[45,45,45]
        Decay_time[3]=[45,45,45]
        Decay_time[4]=[45,45,45]
        Decay_time[5]=[45,45,45]

    # Cross sections per cycle based on how many GWd/MTHM per step

    #  This calculates the time needed for run for a specific burnup in GWd/MTHM for specific number of cycles
    # Equal_Irradiation_time=True

    #Used it the user wants to specify irradation time instead of specific power
    if UseBurnup:
        Irradiation_time=[]
        for i in range(len(Average_power)):
            Irradiation_time.append(0)
            #Irradiation_time=[0,0,0,0]
        for ipower in range(len(Average_power)):
            Irradiation_time[ipower]=[]
            for avgPower in Average_power[ipower]:
                Irradiation_time[ipower].append(Burnup[ipower]*1E3/avgPower/len(Average_power[ipower]))
        crossSectionPerCycle=[]
        for burn in range(len(Burnup)):
            crossSectionPerCycle.append(int(Burnup[burn]/burnupPerStep/Num_cycles[burn]))
    # This is if the user wants to specify specific power instead of irradation time for the desired burnup
    else:
        totalBurnup=[]
        for i in range(len(Irradiation_time)):
            sumBurnup=0
            for j in range(len(Irradiation_time[i])):
                #print Irradiation_time[i][j],Average_power[i][j], Irradiation_time[i][j]*Average_power[i][j]
                sumBurnup=sumBurnup+Irradiation_time[i][j]*Average_power[i][j]
            if abs(sumBurnup/1E3-Burnup[i])>.1:
                raw_input("Warning Sum Irradiation_time*Average_power %s not equal to specified Burnup %s \n Press Enter to continue"%(sumBurnup/1E3,Burnup[i]))
                #print sumBurnup/1E3,Burnup[i]
            else:
                print "Sum Irradiation_time*Average_power %s ~= to specified Burnup %s %s"%(sumBurnup/1E3,Burnup[i],abs(sumBurnup/1E3-Burnup[i]))
                #raw_input("Can not continue")
            totalBurnup.append(sumBurnup)

        crossSectionPerCycle=[]
        for burn in range(len(totalBurnup)):
            crossSectionPerCycle.append(int(totalBurnup[burn]/1000/burnupPerStep/Num_cycles[burn]))




        #Irradiation_time=[]
        # for i in range(len(Average_power)):
        #     Irradiation_time.append(0)
        #     #Irradiation_time=[0,0,0,0]
        # for ipower in range(len(Average_power)):
        #     Irradiation_time[ipower]=[]
        #     for avgPower in Average_power[ipower]:
        #         Irradiation_time[ipower].append(Burnup[ipower]*1E3/avgPower/len(Average_power[ipower]))



    #CROSS_SECTION_STEPS_PER_CYCLE
    #Need to create array of Decat_time, Average_power, and Irradiation_time
    PowerExpanded=[]
    for power in range(len(Average_power)):
        PowerExpanded.append([])
        for cyclePower in range(len(Average_power[power])):
            for cross_section in range(crossSectionPerCycle[power]):
                PowerExpanded[power].append(Average_power[power][cyclePower])

    #  Expand the number of cycle
    #Num_cycle_expanded=[[]]
    Num_cycle_expanded=[[0 for x in range(len(crossSectionPerCycle))]for x in range(len(Num_cycles))]

    for cross in range(len(crossSectionPerCycle)):
        for cycle in range(len(Num_cycles)):
            Num_cycle_expanded[cross][cycle]=(Num_cycles[cycle]*crossSectionPerCycle[cross])

    #  Expand decay time
    Decay_time_expanded=[]
    for decTime in range(len(Decay_time)):
        Decay_time_expanded.append([])
        for decableTime in range(len(Decay_time[decTime])):
            for cross_section in range(crossSectionPerCycle[decTime]):
                if cross_section==crossSectionPerCycle[decTime]-1:
                    Decay_time_expanded[decTime].append(Decay_time[decTime][decableTime])
                else:
                    Decay_time_expanded[decTime].append(0)

    #  Expand variable time
    Irradiation_time_expanded=[]
    for verTime in range(len(Irradiation_time)):
        Irradiation_time_expanded.append([])
        for variableTime in range(len(Irradiation_time[verTime])):
            for cross_section in range(crossSectionPerCycle[verTime]):
                Irradiation_time_expanded[verTime].append(float(Irradiation_time[verTime][variableTime])/crossSectionPerCycle[verTime])

    # Cross section library name
    MIX_NUM=Lib_name

    #  END USER input ===============================

    opus_counter=0
    for i in range(len(Enrichment)):

    #  This is the burnup time steps needed
        Average_pow=[]
        Irradiation_time=[]
        Num_lib=[]
        Decay=[]
        Average_pow=(PowerExpanded[i])
        Irradiation_time=(Irradiation_time_expanded[i])
        Decay=(Decay_time_expanded[i])
        Num_cycles=Num_cycle_expanded[i]
        for j in range(Num_cycles[i]):
            #    Irradiation_time.append(Burnup[i]*1E3/Specific_Power/Num_cycles[i])
            #    Average_pow.append(Specific_Power)
            Num_lib.append(Steps_between_irradation)

        #  Name of the run
        ReactorID="%s_%s_%s"%(Lib_name, Burnup[i], Enrichment[i])
        if times=='Table':
            ReactorID="%s_%s_%s_for_table"%(Lib_name, Burnup[i], Enrichment[i])

        if Lib_name!='mox':
            # The composition of the uranium based on enrichment
            #Frac_U234=0.015+0.058*Enrichment[i]+0.000054*Enrichment[i]*Enrichment[i]
            # Fraction U238
            #Frac_U238=100-Frac_U234-Enrichment[i]
            # Fraction Array
            Frac_U234=0.0089*Enrichment[i]
            Frac_U236=0.0046*Enrichment[i]
            Frac_U238=100-Frac_U234-Frac_U236-Enrichment[i]

            Frac=[Frac_U234*1E4,Enrichment[i]*1E4,Frac_U236*1E4, Frac_U238*1E4]
            #print Frac

        PLOT_DECAY=True
        # Min position in OPUS
        if PLOT_DECAY:
            MINPOSITION=len(Irradiation_time)*IRRADIATE+(len(Irradiation_time)-1)*(DECAY_STEPS)+1
            # Max Position in OPUS
            MAXPOSITION=len(Irradiation_time)*IRRADIATE+(len(Irradiation_time)-1)*(DECAY_STEPS)+len(FINAL_DECAY)
        else:
            MINPOSITION=1
            # Max Position in OPUS
            MAXPOSITION=len(Irradiation_time)*IRRADIATE+(len(Irradiation_time)-1)*(DECAY_STEPS)


        if UNITS[0]=='CuriesLinear_ELEMENT':
            print "Units is GramsLinear"
            MINPOSITION=len(Irradiation_time)*IRRADIATE+(len(Irradiation_time)-1)*(DECAY_STEPS)+2

        if NEW_LIBRARY:
            if Lib_name !='mox':
                if i==0:
                    ARP_File_location='/home/h56/NRC_2015/NRC_Sumamry_Burnup_Study/ARPLibrary'
                    #output_file.write('=shell\n   cp %s/arpdata.txt arpdata.txt\n'%(ARP_File_location))
                    output_file.write('=shell\n  ln -s %s/* .\nend \n\n'%(ARP_File_location))
                    #output_file.write('  cp "/Users/f4p/Desktop/Burnup Study Summary/ARPLibrary/%s" . \nend\n\n'%(Lib_name))

        # Write ARP librariy information
        FT33='w17vplus.f33'
        if Lib_name=='mox':
            FT33='w17vplus_e4.75_m0.74478_mox.f33'
            output_file.write('=shell \n')
            #output_file.write('cp $INPDIR/%s f71f001 \n'%(FT71))
            output_file.write('=shell\n  cp %s/%s ft33f001 \nend \n\n" \n'%(ARP_File_location,FT33))
            output_file.write('end \n\n')

        else:
            write_arp(output_file,Lib_name,Enrichment[i],Num_cycles[i],Irradiation_time,Average_pow,Num_lib,Mod_den)
        # output_file=file where the input deck will be written

        write_origen(USE_FT33,DECAY_STEPS,IRRADIATE,FORMAT_ROW,TITLE,UNITS,Irradiation_time,  \
              Decay,FINAL_DECAY,MIX_NUM,output_file,Isotopes,Frac,Mat,FISSION,Average_pow,Power_instead_Flux)

        for unit in UNITS:
            opus_counter=write_opus(MINPOSITION,MAXPOSITION,unit,output_file,opus_counter,ReactorID,33)

    output_file.close()
    SCALE_EXE='/scale/release/6.1.3/Linux_x86_64/bin/scalerte'
    #os.system('%s -m %s' %(SCALE_EXE,FILE_NAME))
    table_inp='%s_Origen_Table.inp'%(file_tag)
    #os.system('%s -m %s' %(SCALE_EXE,table_inp))
