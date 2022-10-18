partName = 'concrete'
modelName = '1_geoimp'
halfLength = 1750.0
noCuts = 5

partToInstance = {
    "concrete": 'Concrete Instance',
    'Beam': 'Profile Instance',
}

rootA = mdb.models[modelName].rootAssembly
partC = mdb.models[modelName].parts[partName]
cutHeights = []

for i in range(1, noCuts+1):
    cutHeights.append(halfLength/noCuts*i)

for i in cutHeights:
    partC.Set(elements=partC.elements.getByBoundingBox(
        zMin=i-50, zMax=i+9), name='z'+str(int(i)))
    regionDef = rootA.allInstances[partToInstance[partName]
                                   ].sets['z'+str(int(i))]
    mdb.models[modelName].HistoryOutputRequest(name='H-Output-'+'z'+str(
        int(i)), numIntervals=180, createStepName='Step-1', variables=('LE33',), region=regionDef, sectionPoints=DEFAULT)

r1 = rootA.referencePoints
refPoints1 = (r1[r1.keys()[0]], )
rootA.Set(referencePoints=refPoints1, name='Set-RP')

regionDef = rootA.sets['Set-RP']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-3',
                                           createStepName='Step-1', numIntervals=180, variables=('RF3', ), region=regionDef,
                                           sectionPoints=DEFAULT)

for h in cutHeights:
    for i in partC.sets['z'+str(int(h))].elements:
        elo = i.label
        partC.SetFromElementLabels(
            elementLabels=(elo,), name='element'+str(elo))
        regionDef = rootA.allInstances[partToInstance[partName]
                                       ].sets['element'+str(elo)]
        mdb.models[modelName].HistoryOutputRequest(name='H-Output-'+str(elo), createStepName='Step-1', numIntervals=180, variables=(
            'COORDCOM1', 'COORDCOM2', 'COORDCOM3',), region=regionDef, sectionPoints=DEFAULT)

# Create history output request for these nodes to reach them in odb
