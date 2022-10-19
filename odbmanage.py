from abaqusConstants import *
from abaqus import *
import csv
from odbAccess import *
from caeModules import *
from textRepr import *
# open odb

odbBuckle = openOdb(path='Job_1_buckle.odb')

eig1 = float(odbBuckle.steps['Step-1'].frames[1].description.split()[-1])
eig2 = float(odbBuckle.steps['Step-1'].frames[2].description.split()[-1])

odb = openOdb(path='Job_1_geoimp.odb')

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
lis = odb.steps['Step-1'].historyRegions.values()[-1].historyOutputs['RF3'].data
absLis = [(i[0], abs(i[1])) for i in lis]
enuAbsLis = enumerate(absLis)
maxValues = max(enuAbsLis, key=lambda item: item[1][1])
maxForce = maxValues[1][1]
maxIndex = maxValues[0]

outDict = {}
outDict['x'] = []
outDict['y'] = []
outDict['z'] = []
outDict['le3'] = []
outDict['id'] = []
for i in elementNames:
    le3 = odb.steps['Step-1'].historyRegions['Element Concrete Instance.' +
                                             str(i)+' Int Point 1'].historyOutputs['LE33'].data[maxIndex][1]
    xCo = odb.steps['Step-1'].historyRegions.values(
    )[-2].historyOutputs['COORDCOM1  of element set ASSEMBLY_Concrete Instance_ELEMENT'+str(i)].data[0][1]
    yCo = odb.steps['Step-1'].historyRegions.values(
    )[-2].historyOutputs['COORDCOM2  of element set ASSEMBLY_Concrete Instance_ELEMENT'+str(i)].data[0][1]
    zCo = odb.steps['Step-1'].historyRegions.values(
    )[-2].historyOutputs['COORDCOM3  of element set ASSEMBLY_Concrete Instance_ELEMENT'+str(i)].data[0][1]
    outDict['id'].append(i)
    outDict['x'].append(xCo)
    outDict['y'].append(yCo)
    outDict['z'].append(zCo)
    outDict['le3'].append(le3)

with open('mycsvfile.csv', 'wb') as f:
    w = csv.writer(f)
    key_list = list(outDict.keys())
    w.writerow(outDict.keys())
    for i in range(len(elementNames)):
        w.writerow([outDict[x][i] for x in key_list])
