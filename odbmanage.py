from abaqusConstants import *
from abaqus import *
import csv
from odbAccess import *
from caeModules import *
from textRepr import *
##open odb
odb = openOdb(path='Job_A12.odb')

##in this line, only one element of chosen region is picked
elementNodes = odb.steps['Step-1'].historyRegions.values()[1].point.element.connectivity
elementLabel = odb.steps['Step-1'].historyRegions.values()[1].point.element.label
##all nodes in the part of interest are chosen
allNodes = odb.rootAssembly.instances['PART-1-1'].nodes

xSum = 0
ySum = 0
zSum = 0

##query the nodes with labels of vertices of element of interest and average them to find element centroid
for i in elementNodes:
    node = [node for node in allNodes if node.label == i]
    xSum += node[0].coordinates[0]
    ySum += node[0].coordinates[0]
    zSum += node[0].coordinates[0]
    midpoint = [xSum/8,ySum/8,zSum/8]

print("centroid of element: ",elementLabel,"is ",midpoint)

##why need mdb?