partName = 'concrete'
modelName = 'A12'

partToInstance = {
    "concrete": 'Concrete Instance',
    'Beam': 'Profile Instance',
}

set = mdb.models[modelName].parts[partName].Set(
    elements=mdb.models[modelName].parts[partName].elements.getByBoundingBox(zMin=1550, zMax=1590), name='z1550')

regionDef = mdb.models['A12'].rootAssembly.allInstances[partToInstance[partName]].sets['z1550']

mdb.models[modelName].HistoryOutputRequest(name='H-Output-2',
                                           createStepName='Step-1', variables=('LE11', 'LE22', 'LE33', 'LE12', 'LE13',
                                                                               'LE23', 'LEP'), region=regionDef, sectionPoints=DEFAULT)
sa
elementNames = []

for i in set.elements:
    elementNames.append(i.label)

print(elementNames)

# Create history output request for these nodes to reach them in odb
