#!/usr/bin/python
import energymeter
import json
import sys

meter1 = energymeter.EnergyMeter('metsepm3255', '192.168.1.53', 502, 0x02)

with open(meter1.model + '.json') as json_file:
    registermap = json.load(json_file)

registerToRead = []

arguments = sys.argv[1].split(" ")

for argument in arguments:
    registerToRead.append(argument)

for element in registerToRead:
    startingregister, numberofregisters, datatype = registermap[element]
    result = meter1.readholdingregisters(startingregister, numberofregisters, datatype)
    print(str(result))

meter1.client.close()
