#!/usr/bin/python
import paho.mqtt.client as mqtt
import commands
import time

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))

MQTT_HOST = "84.242.134.74"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

mqttc = mqtt.Client("", True, None, mqtt.MQTTv31)
mqttc.on_connect = on_connect
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
print("Connected to host...")

def readPowerStatus():
    batteryVoltage = str(commands.getstatusoutput('cat /sys/class/power_supply/battery/voltage_now')).split('\'')[1]
    batteryVoltage = batteryVoltage[0] + "." + batteryVoltage[1:4]
    voltageNow = str(commands.getstatusoutput('cat /sys/class/power_supply/ac/voltage_now')).split('\'')[1]
    voltageNow = voltageNow[0] + "." + voltageNow[1:4]
    currentNow = str(commands.getstatusoutput('cat /sys/class/power_supply/ac/current_now')).split('\'')[1]
    currentNow = "0." + currentNow[0:4]
    batteryCurrent = str(commands.getstatusoutput('cat /sys/class/power_supply/battery/current_now')).split('\'')[1]
    batteryCurrent = "0." + batteryCurrent[0:4]
    batteryCapacity = str(commands.getstatusoutput('cat /sys/class/power_supply/battery/capacity')).split('\'')[1]
    batteryOnline = str(commands.getstatusoutput('cat /sys/class/power_supply/battery/online')).split('\'')[1]
    mqttc.publish("controllers/a20/battery/online", batteryOnline)
    mqttc.publish("controllers/a20/battery/voltage", batteryVoltage)
    mqttc.publish("controllers/a20/battery/current", batteryCurrent)
    mqttc.publish("controllers/a20/battery/capacity", batteryCapacity)
    mqttc.publish("controllers/a20/supply/voltage", voltageNow)
    mqttc.publish("controllers/a20/supply/current", currentNow)

def readMeterParameters():
    meterVL1N, meterVL2N, meterVL3N, meterFrequency, meterActiveEnergyImportTotal, meterActiveEnergyExportTotal = str(commands.getstatusoutput('./read_pm3255.py "VL1N VL2N VL3N Frequency ActiveEnergyImportTotal ActiveEnergyExportTotal"'))[5:-2].split("\\n")

    mqttc.publish("meters/pm3255/energy", str(float(meterActiveEnergyImportTotal) / 1000))
    mqttc.publish("meters/pm3255/energyx", str(float(meterActiveEnergyExportTotal) / 1000))
    mqttc.publish("meters/pm3255/voltage", meterVL1N)
    mqttc.publish("meters/pm3255/voltage2", meterVL2N)
    mqttc.publish("meters/pm3255/voltage3", meterVL3N)
    mqttc.publish("meters/pm3255/frequency", meterFrequency)

while(1):
    readPowerStatus()
    readMeterParameters()
    time.sleep(5)

mqttc.disconnect()
print("Disconnected from host!")
