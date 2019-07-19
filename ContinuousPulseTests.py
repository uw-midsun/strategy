import lab_equipment as lb
import time
import os


#ni backend, no pyvisa-py

CURRENT_A_BASE = 0.2
CURRENT_A_PULSE = 2
BASE_TIME_MS = 200
PULSE_TIME_MS = 200


load = lb.BK8600()
load.toggle_eload(False)

dmm = lb.DMM_34410A()


#generate new file name for logging in the current directory
i = 0
while os.path.exists("ContinuousPulse%s.txt" % i):
    i += 1
log = open("ContinuousPulse%s.txt" % i, "w")
log.write("Voltage, Current")

def logIV():
	v = dmm.measure_voltage()
	i = load.measure_current()
	#log to file
	log.write("{voltage}, {current}".format(voltage = v, current = i))
	print("{voltage}, {current}".format(voltage = v, current = i))

def pulse():
	print("pulse")
	logIV()
	#Set E-load output to base
	load.set_current(CURRENT_A_BASE)
	#wait base time
	time.sleep(BASE_TIME_MS/1000)
	logIV()
	#set e-load output to pulse
	load.set_current(CURRENT_A_PULSE)
	#wait pulse time
	time.sleep(PULSE_TIME_MS/1000)
	logIV()
	#set e-load output to 0A, don't turn off as it will take longer
	load.set_current(0)

#Turn e-load on
#load.toggle_eload(True)

#send pulse command
#pulse()
