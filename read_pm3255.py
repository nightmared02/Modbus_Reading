#!/usr/bin/python
import energymeter
import json

meter1 = energymeter.EnergyMeter('metsepm3255', '192.168.1.35', 502, 0x02)

with open(meter1.model + '.json') as json_file:
    registermap = json.load(json_file)

startingregister, numberofregisters, datatype = registermap["VL1N"]
VL1N = meter1.readholdingregisters(startingregister, numberofregisters, datatype)

startingregister, numberofregisters, datatype = registermap["ActiveEnergyImportTotal"]
ActiveEnergyImportTotal = meter1.readholdingregisters(startingregister, numberofregisters, datatype)/1000

print(VL1N, str(ActiveEnergyImportTotal))

meter1.client.close()
