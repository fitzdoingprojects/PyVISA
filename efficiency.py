import visa
import ivi
import numpy
import datetime
import time

#Requires Keithley 228A hooked up as dc load
#Requires Agilent/HP 34401A hooked up as voltmeter at load
#Requires Agilent/HP 34401A hooked up as ampmeter at load
#Requires Agilent/HP 63xxx hooked up as dc source

class efficiency():
    
    def __init__(self):

        self.startVoltage = 0.8
        self.endVoltage = 3.3
        self.stepVoltage = 0.1
        self.startCurrent = -0.1
        self.endCurrent = -1
        self.stepCurrent = -0.1
        self.delay = 1

        instr = visa.ResourceManager()
        0
        self.psu1 = instr.open_resource('GPIB0::04::INSTR') #replace with actual address
        self.psu1.write('VOLT:PROT 16') #set over voltage higher than possible voltages
        self.psu1.write('VOLT '+str(0)) #set voltage to 0
        self.psu1.write('CURR '+str(3)) #set max current to 2 amps
        self.psu1.write('OUTPut ON')

        instr = visa.ResourceManager()
        instr.list_resources()
        self.psu2 = instr.open_resource('GPIB0::11::INSTR')
        self.psu2.write("V7") #put k228a in remote mode
        #self.psu2.write("V4.2X") #set voltage to maximum battery voltage
        #self.psu2.write("I0.0X") #set current to zero
        self.psu2.write("V" + str(15) + "X")#set voltage to maximum battery voltage
        self.psu2.write("I" + str(0.0) + "X") #set current to zero
        self.psu2.write("F1X")

        self.dmm1 = ivi.agilent.agilent34401A()
        self.dmm1.initialize('GPIB0::02::INSTR') #replace with actual instrument address
        self.dmm1.measurement_function = 'dc_volts'

        self.dmm2 = ivi.agilent.agilent34401A()
        self.dmm2.initialize('GPIB0::03::INSTR') #replace with actual instrument address
        self.dmm2.measurement_function = 'dc_current'



    def sourceVoltage(self, volts):
        self.psu1.write('VOLT '+str(volts))

    def loadCurrent(self, amps):
        self.psu2.write("I" + str(amps) + "X")
        
    def loadVoltage(self, volts):
        self.psu2.write("V" + str(volts) + "X")

    def measure(self):
        sourceVoltage = self.psu1.query('MEAS:VOLT?')
        sourceCurrent = self.psu1.query('MEAS:CURR?')

        loadVoltage = self.dmm1.measurement.read(1)
        loadCurrent = self.dmm2.measurement.read(1)

        return float(sourceVoltage), float(sourceCurrent), loadVoltage, loadCurrent 

    def report(self):
        Vi, Ii, Vo, Io = self.measure()
        e = (Vo * Io) / (Vi * Ii) * 100
        print(Vi, Ii, Vo, Io, e, Vo * Io)

    def efficiencyVoltSweep(self):
        f = open("efficiencyVoltSweep " + str(datetime.datetime.now()) + ".txt", "w")
        self.loadVoltage(0)
        self.loadCurrent(1.5)
        for loadVolts in numpy.arange(2.8, 4.1, 0.1):
            self.loadVoltage(loadVolts)
            for voltage in numpy.arange(0.8, 3.5, 0.1):
                self.sourceVoltage(voltage)
                time.sleep(self.delay)
                Vi, Ii, Vo, Io = self.measure()
                e = (Vo * Io) / (Vi * Ii) * 100
                f.write(str(Vi)+ ", " + str(Ii) + ", " + str(Vo) + ", " + str(Io) + ", " + str(e) + ", " + str(Vo * Io) + '\n')
                print(Vi, Ii, Vo, Io, e, Vo * Io )

        self.sourceVoltage(0)
        self.loadVoltage(0)
        self.loadCurrent(0)
        self.measure()
        f.close()

    def efficiency12VoltSweep(self):
        f = open("efficiency12VoltSweep " + str(datetime.datetime.now()) + ".txt", "w")
        self.loadVoltage(0)
        self.loadCurrent(1.5)
        for loadVolts in numpy.arange(8, 15, 0.1):
            self.loadVoltage(loadVolts)
            for voltage in numpy.arange(3, 22, 0.2):
                self.sourceVoltage(voltage)
                time.sleep(self.delay)
                Vi, Ii, Vo, Io = self.measure()
                e = (Vo * Io) / (Vi * Ii) * 100
                f.write(str(Vi)+ ", " + str(Ii) + ", " + str(Vo) + ", " + str(Io) + ", " + str(e) + '\n')
                print(Vi, Ii, Vo, Io, e)

        self.sourceVoltage(0)
        self.loadVoltage(0)
        self.loadCurrent(0)
        self.measure()
        f.close()

    def efficiency7Volt1CellSweep(self):
        f = open("efficiency7Volt1CellSweep " + str(datetime.datetime.now()) + ".txt", "w")
        self.loadVoltage(0)
        self.loadCurrent(1.5)
        for loadVolts in numpy.arange(2.8, 4.2, 0.1):
            self.loadVoltage(loadVolts)
            for voltage in numpy.arange(3, 7, 0.2):
                self.sourceVoltage(voltage)
                time.sleep(self.delay)
                Vi, Ii, Vo, Io = self.measure()
                e = (Vo * Io) / (Vi * Ii) * 100
                f.write(str(Vi)+ ", " + str(Ii) + ", " + str(Vo) + ", " + str(Io) + ", " + str(e) + '\n')
                print(Vi, Ii, Vo, Io, e)

        self.sourceVoltage(0)
        self.loadVoltage(0)
        self.loadCurrent(0)
        self.measure()
        f.close()



    def efficiencyLoadTest(self):
        f = open("efficiencyLoadTest" + str(datetime.datetime.now()) + ".txt", "w")
        self.loadCurrent(0)
        self.loadVoltage(5)
        for current in numpy.arange(-0.4, -1.3, -0.1):
            self.loadCurrent(current)
            for voltage in numpy.arange(1.2, 3.5, 0.1):
                self.sourceVoltage(voltage)
                time.sleep(self.delay)
                Vi, Ii, Vo, Io = self.measure()
                e = (Vo * Io) / (Vi * Ii) * 100
                f.write(str(Vi)+ ", " + str(Ii) + ", " + str(Vo) + ", " + str(Io) + ", " + str(e) + ", " + str(Vo * Io) + '\n')
                print(Vi, Ii, Vo, Io, e, Vo * Io )

        self.sourceVoltage(0)
        self.loadCurrent(0)
        f.close()
