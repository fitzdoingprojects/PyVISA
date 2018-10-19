# PyVISA

Hardware Requirements:

GPIP to USB adapter
    - Agilent 82357B 

Software Setup:

    Setup linux-gpib (https://sourceforge.net/projects/linux-gpib/files/latest/download)    
        (https://linux-gpib.sourceforge.io/doc_html/supported-hardware.html#AGILENT-82357A)
        Follow instructions in "INSTALL" txt file, will need kernel source code
        Follow these additional instructions for supporting the Agilent 82357B 
        https://gist.github.com/turingbirds/6eb05c9267a6437183a9567700e8581a
        Also note you will need to re-install anytime the kernel updates!
    Use pipenv (https://pipenv.readthedocs.io/en/latest/) to install python dependencies.
        make sure to run:
        pipenv --three --site-packages
        so that the linux-gpib python bindings are available in the pipenv environment
        Then sync:
        pipenv sync
        This should install the necessary packages to talk to instruments (pyusb, PyVISA, pyvisa-py, ivi) and some additional packages for graphing/displaying results.
        
    For setup on raspi: https://xdevs.com/guide/agilent_gpib_rpi/

GPIB to USB test:

verify that 'lsusb' shows 82357B 
    "Bus xxx Device xxx: ID 0957:0718 Agilent Technologies, Inc. "
check connection with 'ibtest'
    (you probably want to open a device): d #enter 'd' for devices
    enter primary gpib address for device you wish to open [0-30]: 11 #enter gpib address of test equipment
    (w)rite data string #enter w, to write
    *IDN? #ask the device to identify



Supported Test Equipement:
    Agilent/HP 34401A DMM
    Agilent/HP 66311A/B DC source
    Keithley 228A Voltage/Current Source

Todo:
    Write custom IVI drivers for 66311 and 228A 
    http://alexforencich.com/wiki/en/python-ivi/writing-drivers

