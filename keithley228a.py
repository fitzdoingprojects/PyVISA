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
	
	


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
							 
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" or ".join((", ".join(map(str,
                                                                     range_[:-1])),
                                                       str(range_[-1])))))
        else:
            return ui
			
	

def main():
	print("Hello World!")

	stream_ids = tls.get_credentials_file()['stream_ids']
	print(stream_ids)

	# Get stream id from stream id list 
	stream_id0 = stream_ids[0]
	stream_id1 = stream_ids[1]
	
	# Make instance of stream id object 
	stream_0 = go.Stream(
		token=stream_id0,  # link stream id to 'token' key
		maxpoints=200      # keep a max of 200 pts on screen
	)
	
	# Make instance of stream id object 
	stream_1 = go.Stream(
		token=stream_id1,  # link stream id to 'token' key
		maxpoints=200      # keep a max of 200 pts on screen
	)

	stream_voltage = go.Scatter(
		x=[],
		y=[],
		mode='lines+markers',
		name = 'voltage',
		stream=stream_0         # (!) embed stream id, 1 per trace
	)

	
	# Create traces
	stream_current = go.Scatter(
		x =[],
		y =[],
		mode = 'lines+markers',
		name = 'current',
		yaxis='y2',
		stream=stream_1         # (!) embed stream id, 1 per trace
	)
	data = go.Data([stream_voltage, stream_current])

	# Add title to layout object
	layout = go.Layout(title='Keithley 228A LEAD ACID CHARGING (13.6V 0.5A)',
		yaxis=dict(
			title='Volts',
			range=[1, 15]
		),
		yaxis2=dict(
			title='Amps',
			titlefont=dict(
				color='rgb(148, 103, 189)'
			),
			tickfont=dict(
				color='rgb(148, 103, 189)'
			),
			overlaying='y',
			side='right',
			range=[0, 1.5]
		)
	)

	# Make a figure object
	fig = go.Figure(data=data, layout=layout)

	# Send fig to Plotly, initialize streaming plot, open new tab
	py.plot(fig, filename='python-streaming')


	# We will provide the stream link object the same token that's associated with the trace we wish to stream to
	v = py.Stream(stream_id0)
	c = py.Stream(stream_id1)
	

	# We then open a connection
	v.open()
	c.open()

	# (*) Import module keep track and format current time
	import datetime
	import time

	i = 0    # a counter
	k = 5    # some shape parameter

	# Delay start of stream by 5 sec (time to switch tabs)
	time.sleep(1)
	
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
		# Send data to your plot
		v.write(dict(x=x, y=y))
		
		# Send data to your plot
		y = values[1]
		c.write(dict(x=x, y=y))
		#     Write numbers to stream to append current data on plot,
		#     write lists to overwrite existing data on plot

		time.sleep(1)  # plot a point every second    
	# Close the stream when done plotting
	s.close()

  
if __name__== "__main__":
	main()