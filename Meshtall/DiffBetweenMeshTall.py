
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
REF_FILE="reference.meshtal"
PERT_FILE="pertrubed.meshtal"
DIFF_FILE="diffResult.meshtal"
PERCENT_DIFF_FILE="percentDiff.meshtal"
MULTIPLICATION_NUMBER=6.4234E+18;

NUM_LINE=15
resultArrayRef=[]
errorArrayRef=[]
resultArrayPert=[]
errorArrayPert=[]
inputRefFile=open(WORKING_DIR+REF_FILE,'r')
inputPertFile=open(WORKING_DIR+PERT_FILE,'r')
outputDiffFile=open(WORKING_DIR+DIFF_FILE,'w')
outputPercentDiff=open(WORKING_DIR+PERCENT_DIFF_FILE,'w')
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
count=0
for line in inputPertFile:
    count+=1
    if count>NUM_LINE:
        temp=line.split()
        results=float(temp[3])
        error=float(temp[4])
        resultArrayPert.append(results)
        errorArrayPert.append(error)
inputPertFile.close()

inputRefFile=open(WORKING_DIR+REF_FILE,'r')
count=0
for line in inputRefFile:
    line2=line
    count+=1
    if count>NUM_LINE:
        refResultsString=resultArrayRef[count-NUM_LINE-1]
        refResults=float(resultArrayRef[count-NUM_LINE-1])
        perResults=float(resultArrayPert[count-NUM_LINE-1])
        # print refResults,perResults
        # if (refResults!=0):
        #     percentDiff=(refResults-perResults)/refResults
        # else:
        #     percentDiff=0

        #  Used to SCALE MCNP results to per source partcile
        diff=(refResults-perResults)*MULTIPLICATION_NUMBER


        #  For formatting purposes
        if diff<0:
            line=line.replace(refResultsString, "%.4E"%(diff))
        else:
             line=line.replace(refResultsString, "%.5E"%(diff))

        #  Percent diff captures to much noise
        # if percentDiff<0:
        #     line2=line2.replace(refResultsString, "%.4E"%(percentDiff))
        #     # line2=line2.replace(refResultsString, "%.4E"%(0))
        # else:
        #     line2=line2.replace(refResultsString, "%.5E"%(percentDiff))
    outputDiffFile.write(line)
    outputPercentDiff.write(line2)


