from abaqusConstants import *
from abaqus import *
import csv
from odbAccess import *
from caeModules import *
from textRepr import *
from collections import OrderedDict
# open odb
modelNo = 55

odbBuckle = openOdb(path='Job_'+str(modelNo)+'_buckle.odb')

eig1 = float(odbBuckle.steps['Step-1'].frames[1].description.split()[-1])
eig2 = float(odbBuckle.steps['Step-1'].frames[2].description.split()[-1])

odb = openOdb(path='Job_'+str(modelNo)+'_geoimp.odb')

# initialize empty list
elementNames = []

# populate the list based on concrete instance history output regions. This loop extracts the element number from dictionary keys
for text in odb.steps['Step-1'].historyRegions.keys():
    left = 'Concrete Instance.'
    right = ' Int'
    try:
        found = text[text.index(left)+len(left):text.index(right)]
        elementNames.append(int(found))
    except:
        pass

# get the output of loading at reference point, take absolute value of forces
# enumerate the list of tuples to find the index of the tuple with max force
lis = odb.steps['Step-1'].historyRegions.values()[-2].historyOutputs['RF3'].data
absLis = [(i[0], abs(i[1])) for i in lis]
enuAbsLis = enumerate(absLis)
maxValues = max(enuAbsLis, key=lambda item: item[1][1])
maxForce = maxValues[1][1]
maxIndex = maxValues[0]

outDict = OrderedDict()
outDict['id'] = []
outDict['x'] = []
outDict['y'] = []
outDict['z'] = []
outDict['le3'] = []
outDict['u'] = []
outDict['f'] = []
outDict['max u'] = []
outDict['max f'] = []
outDict['eigens'] = []

for i in elementNames:
    le3 = odb.steps['Step-1'].historyRegions['Element Concrete Instance.' +
                                             str(i)+' Int Point 1'].historyOutputs['LE33'].data[maxIndex][1]
    xCo = odb.steps['Step-1'].historyRegions.values(
    )[-3].historyOutputs['COORDCOM1  of element set ASSEMBLY_Concrete Instance_ELEMENT'+str(i)].data[0][1]
    yCo = odb.steps['Step-1'].historyRegions.values(
    )[-3].historyOutputs['COORDCOM2  of element set ASSEMBLY_Concrete Instance_ELEMENT'+str(i)].data[0][1]
    zCo = odb.steps['Step-1'].historyRegions.values(
    )[-3].historyOutputs['COORDCOM3  of element set ASSEMBLY_Concrete Instance_ELEMENT'+str(i)].data[0][1]
    outDict['id'].append(i)
    outDict['x'].append(xCo)
    outDict['y'].append(yCo)
    outDict['z'].append(zCo)
    outDict['le3'].append(le3)

for i in range(180):
    outDict['u'].append(odb.steps['Step-1'].historyRegions.values()
                        [-1].historyOutputs.values()[0].data[i][1])
    outDict['f'].append(absLis[i][1])

uAtMax = abs(outDict['u'][maxIndex])
outDict['max u'].append(uAtMax)
outDict['max f'].append(maxForce)

outDict['eigens'].append(eig1)
outDict['eigens'].append(eig2)

with open(str(modelNo)+'.csv', 'wb') as f:
    w = csv.writer(f)
    key_list = list(outDict.keys())
    w.writerow(outDict.keys())
    for i in range(len(elementNames)):
        w.writerow([outDict[x][i] for x in key_list])

odb.close()
odbBuckle.close()
