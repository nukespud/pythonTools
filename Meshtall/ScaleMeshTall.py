
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






WORKING_DIR="/Users/f4p/Desktop/HFIR_mesh/"
REF_FILE="pertrubed.meshtal"
SCALED_FILE="pertrubed_scaled.meshtal"
MULTIPLICATION_NUMBER=6.4234E+18;

NUM_LINE=15
resultArrayRef=[]
errorArrayRef=[]
resultArrayPert=[]
errorArrayPert=[]
inputRefFile=open(WORKING_DIR+REF_FILE,'r')
scalledFile=open(WORKING_DIR+SCALED_FILE,'w')
count=0
for line in inputRefFile:
    count+=1
    if count>NUM_LINE:
        temp=line.split()
        results=temp[3]
        error=temp[4]
        resultArrayRef.append(results)
        errorArrayRef.append(error)
inputRefFile.close()

inputRefFile=open(WORKING_DIR+REF_FILE,'r')
count=0
for line in inputRefFile:
    count+=1
    if count>NUM_LINE:
        refResultsString=resultArrayRef[count-NUM_LINE-1]
        refResults=float(resultArrayRef[count-NUM_LINE-1])

        reffResScalled=refResults*MULTIPLICATION_NUMBER


        #  For formatting purposes
        if reffResScalled<0:
            line=line.replace(refResultsString, "%.4E"%(reffResScalled))
        else:
             line=line.replace(refResultsString, "%.5E"%(reffResScalled))

    scalledFile.write(line)


