import visa
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go


def keith228a(): 
	#init
	instr = visa.ResourceManager()
	instr.list_resources()
	keithley = instr.open_resource('GPIB0::11::INSTR')
	keithley.write("V7") #put k228a in remote mode

	#command reference
	keithley.query("G0X") #read current output set point (NOT ACTUAL VALUES)
	keithley.write("V12.6X") #sets voltage to 12.6V
	keithley.write("I0.10X") #sets current to 100mA
	keithley.write("F0X") #turns off outputs
	keithley.write("F1X") #turns on outputs
	keithley.query("G4X") #reads current voltage/current (only works with outputs turned on) with prefixes
	keithley.query("G5X") #reads current voltage/current (only works with outputs turned on) without prefixes 
	keithley.query_ascii_values("G5X") #returns array with current voltage a 0th element and current as 1st element
	#dont forget to switch between source and sink
	
	

def main():
	#init
	instr = visa.ResourceManager()
	instr.list_resources()
	keithley = instr.open_resource('GPIB0::11::INSTR')
	time.sleep(1)
	keithley.write("V7") #put k228a in remote mode
	print("Keithley 228A in remote mode\n")
	time.sleep(1)
	keithley.query("G0X") #read current output set point (NOT ACTUAL VALUES)
	keithley.write("V13.6X") #sets voltage to 12.6V
	keithley.write("I0.5X") #sets current to 100mA
	print("set to 13.6V and 0.5A\n")
	time.sleep(1)
	keithley.write("F1X") #turns on outputs
	print("turn outputs on\n")
	time.sleep(1)

	while True:
		# Current time on x-axis, random numbers on y-axis
		x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
		values = keithley.query_ascii_values("G5X")
		y = values[0]

		print(x,y)
		time.sleep(1)  # plot a point every second    
	# Close the stream when done plotting
	s.close()

  
if __name__== "__main__":
	main()