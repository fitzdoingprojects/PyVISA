import ivi
import numpy as np


def hp34401a(): 
	dmm1 = ivi.agilent.agilent34401A()
	dmm1.initialize('GPIB0::02::INSTR') #replace with actual instrument address
	dmm1.measurement_function = 'dc_volts'
	#dmm2.measurement_function = 'dc_current'
	dmm1.measurement.read(1)
	

	