from abaqusConstants import *
from abaqus import *
import csv
from odbAccess import *
from caeModules import *
from textRepr import *
<<<<<<< HEAD
##open odb
=======
# open odb
>>>>>>> 8808201219f1e431d35bf2ff9e11f64cd25b4d25
odb = openOdb(path='Job_A12.odb')

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

print(elementNames)

# all nodes in the part of interest are chosen
allNodes = odb.rootAssembly.instances['Concrete Instance'].nodes[:]

# connectivities of each element obtained with this loop
for i in elementNames:
    search = '.' + str(i) + ' '
    print('search', search)
    key = [key for key in odb.steps['Step-1'].historyRegions.keys()
           if search in key]
    print('key', key[0])
    elementNodes = odb.steps['Step-1'].historyRegions[key[0]
                                                      ].point.element.connectivity
    print(elementNodes)
    xSum = 0
    ySum = 0
    zSum = 0
# query the nodes with labels of vertices of element of interest and average them to find element centroid
    for i in elementNodes:
        node = [node for node in allNodes if node.label == i]
        xSum += node[0].coordinates[0]
        ySum += node[0].coordinates[0]
        zSum += node[0].coordinates[0]
        midpoint = [xSum/8, ySum/8, zSum/8]

    print("centroid of element: ", i, "is ", midpoint)

# why need mdb?
