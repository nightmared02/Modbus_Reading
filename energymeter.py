from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import struct

class EnergyMeter:
    def __init__(self, model, gatewayipaddress, port ,deviceid):
        self.model = model
        self.gatewayipaddress = gatewayipaddress
        self.port = port
        self.deviceid = deviceid
        self.client = ModbusClient(self.gatewayipaddress, port=self.port)
        self.client.connect()

    def readholdingregisters(self, startingregister, numberofregisters = 1, datatype = 'int16'):
        self.startingresiter = startingregister
        self.numberofregisters = numberofregisters
        self.datatype = datatype
        result = self.client.read_holding_registers(startingregister, numberofregisters, unit=self.deviceid)
        if datatype == 'int32' or  datatype == 'int64':
            concatResult = []
            for register in result.registers:
                binRegister = "{0:b}".format(register)
                binRegister = binRegister[::-1]
                while len(binRegister) < 16:
                    binRegister += "0"
                binRegister = binRegister[::-1]
                concatResult.append(binRegister)
            concatResult = ''.join(concatResult)
            concatResult = (float(int(concatResult, 2)))
            return concatResult
        elif datatype == 'float32':
            concatResult = []
            for register in result.registers:
                binRegister = "{0:b}".format(register)
                binRegister = binRegister[::-1]
                while len(binRegister) < 16:
                    binRegister += "0"
                binRegister = binRegister[::-1]
                concatResult.append(binRegister)
            concatResult = ''.join(concatResult)
            if len(concatResult) < 32:
                concatResult = "0" + concatResult
            else:
                pass
            concatResultHexValue = hex(int(concatResult, 2))[2:]
            if (concatResultHexValue) == 'ffc00000L':
                return("NaN")
            elif (concatResultHexValue == '7f800000'):
                return("Inf")
            elif (concatResultHexValue == 'ff800000'):
                return("-Inf")
            else:
                pass
            finalResult = str(struct.unpack('!f', concatResultHexValue.decode('hex'))[0])[:-7]
            return finalResult
        else:
            return result.registers
