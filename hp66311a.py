import visa

def hp66331a():
    instr = visa.ResourceManager()
    instr.list_resources()
    psu = instr.open_resource('GPIB0::04::INSTR') #replace with actual address
    psu.write('VOLT:PROT 16') #set over voltage protection level, make sure it larger than max voltage
    psu.write('VOLT '+str(11.1))
    psu.write('CURR '+str(1))
    psu.write('OUTPut ON')
    psu.query('MEAS:VOLT?')
    psu.query('MEAS:CURR?')
