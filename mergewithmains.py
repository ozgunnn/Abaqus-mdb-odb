partName = 'concrete'
modelName = 'A12'

partToInstance = {
    "concrete": 'Concrete Instance',
    'Beam': 'Profile Instance',
}

mdb.models[modelName].parts[partName].Set(elements=mdb.models[modelName].parts[partName].elements.getByBoundingBox(zMin=1550, zMax=1590), name='z1550')

regionDef = mdb.models['A12'].rootAssembly.allInstances[partToInstance[partName]].sets['z1550']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2',
                                           createStepName='Step-1', variables=('LE11', 'LE22', 'LE33', 'LE12', 'LE13',
                                                                               'LE23', 'LEP'), region=regionDef, sectionPoints=DEFAULT)

for i in mdb.models['A12'].parts['concrete'].sets['z1550'].elements:
    elo=i.label
    mdb.models[modelName].parts[partName].SetFromElementLabels(elementLabels=(elo,), name='element'+str(elo))
    regionDef = mdb.models['A12'].rootAssembly.allInstances[partToInstance[partName]].sets['element'+str(elo)]
    #regionDef = mdb.models['A12'].parts['concrete'].sets['element'+str(elo)]
    mdb.models[modelName].HistoryOutputRequest(name='H-Output-'+str(elo),createStepName='Step-1', variables=('COORDCOM1','COORDCOM2','COORDCOM3',), region=regionDef, sectionPoints=DEFAULT)

odb.steps['Step-1'].historyRegions.values()[-1].historyOutputs.values()[-1].data[0]