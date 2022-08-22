partName = 'concrete'
modelName = 'A12'

partToInstance = {
    "concrete": 'Concrete Instance',
    'Beam': 'Profile Instance',
}

a = mdb.models['A12'].rootAssembly

set = mdb.models[modelName].parts[partName].Set(
    elements=mdb.models[modelName].parts[partName].elements.getByBoundingBox(zMin=1550, zMax=1590), name='z1550')

regionDef = a.allInstances[partToInstance[partName]].sets['z1550']

mdb.models[modelName].HistoryOutputRequest(name='H-Output-2',
                                           createStepName='Step-1', variables=('LE11', 'LE22', 'LE33', 'LE12', 'LE13',
                                                                               'LE23', 'LEP'), region=regionDef, sectionPoints=DEFAULT)

r1 = a.referencePoints
refPoints1 = (r1[r1.keys()[0]], )
a.Set(referencePoints=refPoints1, name='Set-RP')

regionDef = mdb.models['A12'].rootAssembly.sets['Set-RP']
mdb.models['A12'].HistoryOutputRequest(name='H-Output-3',
                                       createStepName='Step-1', variables=('RF3', ), region=regionDef,
                                       sectionPoints=DEFAULT)

elementNames = []

for i in set.elements:
    elementNames.append(i.label)

print(elementNames)

# Create history output request for these nodes to reach them in odb
