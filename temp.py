 #!/usr/bin/env python
import serial, sys, time, glob, struct
import numpy as np
def send(ser,device, command, data=0):
    # send a packet using the specified device number, command number, and data
    # The data argument is optional and defaults to zero
    packet = struct.pack('<BBl', device, command, data)
    # Return a string containing the values v1, v2, ... packed according to the given format. 
    # The arguments must match the values required by the format exactly.
    ser.write(packet)
    # Writes binary data to the serial port. This data is sent as a byte or series of bytes; 
    # sends the characters representing the digits of a number use the print() function instead.
 
def receive(ser):
    # return 6 bytes from the receive buffer
    # there must be 6 bytes to receive (no error checking)
    r = [0,0,0,0,0,0]
    for i in range (6):
        r[i] = ord(ser.read(1)) #read up to 1 byte 
    return r

def testIT(device=3): #device = 0 selects all the device
    try:
        ser = serial.Serial("COM6", 9600, 8, 'N', 1, timeout=5)   
        # open serial port
        # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    except:
        print("Error opening com port. Quitting.")
        #sys.exit(0)
    print(ser)
    print("Opening " + ser.portstr)

    #device = 1
    command = 52 # supply voltage query
    data = 0
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    time.sleep(1) # wait for 1 second

    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4

        print("Receiving reply " + str(reply))
        print("Device number: " + str(reply[0]))
        print("Command number: " +  str(reply[1]))
        print("Supply voltage: " + str(replyData/10) + "V") # Supply voltage must be divided by ten
    except:
        print("No reply was received.")


    #device = 1
    command = 60 # current position
    data = 0
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    time.sleep(1) # wait for 1 second
                
    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        #last 4 bytes(replyDAta) is used to calculate data which is also the step value 
        if reply[5] > 127:
           replyData -= 256.0**4

        print("Receiving reply " + str(reply))
        print("Device number: " + str(reply[0]))
        print("Command number: " +  str(reply[1]))
        print("Current Pos: " + str(replyData) + " step") #data
        print("Current Pos: " + str(replyData/21000) + " mm")
    except:
        print("No reply was received.")
    
    command = 51 # current position
    data = 0
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    time.sleep(1) # wait for 1 second
    
    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        #last 4 bytes(replyDAta) is used to calculate data which is also the step value 
        if reply[5] > 127:
           replyData -= 256.0**4

        print("Current version: " + str(replyData/100)) #data
    except:
        print("No reply was received.")


    print("Closing " + ser.portstr)
    ser.close()
 
# send(ser,device, 20, 10110); # move absolute
# reply=receive(ser);
# replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
# print replyData 

def getPosition(tty="COM6",device=3,scale=21000):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)



    #device = 1
    command = 60 # current position
    data = 0
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    #time.sleep(1) # wait for 1 second?
    
    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4

        print("Receiving reply " + str(reply))
        print("Device number: " + str(reply[0]))
        print("Command number: " +  str(reply[1]))
        print("Current Pos: " + str(replyData) + "[enc steps]") #
        print("Current Pos: " + str(replyData/scale) + "[mm]") # 
    except:
        print("No reply was received.")


    
def moveAbsolute(position,device, position1 = 0, device1 = 100, position2 = 0, device2 = 100, tty="COM6",scale=21000):

    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)

    #device = 0
    command = 20 # move Absolute command

    #data = position # what units?
    data = np.int64(position*scale)
    data1 = np.int64(position1*scale)
    data2 = np.int64(position2*scale)
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    if position1 != 0:
        print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device1, command, data1))
        send(ser,device1, command, data1)
    if position2 != 0:
        print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device2, command, data2))
        send(ser,device2, command, data2)
    print('')
    #time.sleep(1) # wait for 1 second # NO waiting (dont now how long use stepping for blocking)
    # max distance = 25.3969mm and 101.5873
    try:
        reply = receive(ser)
        if device1 != 100:
            reply1 = receive(ser)
            replyData1 = (256.0**3.0*reply1[5]) + (256.0**2.0*reply1[4]) + (256.0*reply1[3]) + (reply1[2])
            if reply1[5] > 127:
                replyData1 -= 256.0**4
            print("Requested Position for device %i: " % (device1) + str(data1) + "[Steps]") #
            print("Absolute Position for device %i: " % (device1) + str(replyData1) + "[Steps]") #
            print("Requested Position for device %i: " % (device1) + str(data1/scale) + "[mm]") #
            print("Absolute Position for device %i: " % (device1) + str(replyData1/scale) + "[mm]") #
            print('')
            
        if device2 != 100:
            reply2 = receive(ser)
            replyData2 = (256.0**3.0*reply2[5]) + (256.0**2.0*reply2[4]) + (256.0*reply2[3]) + (reply2[2])
            if reply2[5] > 127:
                replyData2 -= 256.0**4
            print("Requested Position for device %i: " % (device2) + str(data2) + "[Steps]") #
            print("Absolute Position for device %i: " % (device2) + str(replyData2) + "[Steps]") #
            print("Requested Position for device %i: " % (device2) + str(data2/scale) + "[mm]") #
            print("Absolute Position for device %i: " % (device2) + str(replyData2/scale) + "[mm]") #
            print('')
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4
        #print("Receiving reply " + str(reply))
        #print("Device number: " + str(reply[0]))
        #print("Command number: " +  str(reply[1]))
        
        print("Requested Position for device %i: " % (device) + str(data) + "[Steps]") #
        print("Absolute Position for device %i: " % (device) + str(replyData) + "[Steps]") #
        print("Requested Position for device %i: " % (device) + str(data/scale) + "[mm]") #
        print("Absolute Position for device %i: " % (device) + str(replyData/scale) + "[mm]") #
    except:
        print("No reply was received.")
        #print("Receiving reply " + str(reply))
        #print("Device number: " + str(reply[0]))
        #print("Command number: " +  str(reply[1]))

        
    else:
        pass
        
    print("Closing " + ser.portstr)
    ser.close()

def moveStep(step,tty="COM6",scale=21000):
    x = getPosition(tty=tty,scale=scale) #returns value of final position
    moveAbsolute(x+step,tty=tty,scale=scale)
    # time
    v= 20.0 # mm/sec
    t = step/v
    print("move time",t)

    
def home(device=0,tty="COM6"):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)

    #device = 0
    command = 1 # move home command

    print('Sending instruction. Device: %i, Command: %i, Data: 0 ' % (device, command))
    send(ser,device, command)
    #time.sleep(1) # wait for 1 second # NO waiting (dont know how long use stepping for blocking)
   
    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4 
           #handles negative data

        print("Absolute Position: " + str(replyData) + "[Steps]")
        print("Absolute Position: 0" + "[mm]") #
        
    except:
        print("No reply was received.")

    print("Closing " + ser.portstr)
    ser.close()

    
def testrun1(device=0,tty="COM6", scale = 21000):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)
    #device = 0
    command = 20 # move Absolute command

    #data = position # what units?
    data = np.int64(25.3969*scale)
    print('Sending instruction. Device: %i, Command: %i,' % (device, command))
    send(ser,device, command, data)
    reply = receive(ser)

    for i in range(66):
        # 34 for 5 mins
        # 66 for 10 mins
        command = 1 # current position
        data = 0
        print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
        send(ser,device, command, data)
        reply = receive(ser)
        print('Sending instruction. Device: 3, Command: 20, Data: 533334')
        send(ser,device, 20, np.int64(25.3969*scale))
        reply = receive(ser)
    send(ser,device, 1)

def targetspeed(speed,device=0,tty="COM6"):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)

    #device = 0
    command = 42 # change target speed command 
    data = np.int64(speed / ( 9.375 * 0.047625*10**-3))
    #data = position # what units?
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    #time.sleep(1) # wait for 1 second # NO waiting (dont now how long use stepping for blocking)
    # max distance = 25.3969mm

    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4

        #print("Receiving reply " + str(reply))
        #print("Device number: " + str(reply[0]))
        #print("Command number: " +  str(reply[1]))
        print("Requested Speed: " + str(replyData) + "[Steps]") #
        print("Absolute Speed: " + str(replyData) + "[Steps]") #
        print("Requested Speed: " + str(speed) + "[mm/s]") #
        print("Absolute Speed: " + str(speed) + "[mm/s]") #

    except:
        print("No reply was received.")

    print("Closing " + ser.portstr)
    ser.close()
    
def runningcurrent(current,device=0,tty="COM6"):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)

    command = 38 # change running current command 
    data = np.int64(current * 500*10**-2)
    #default current = 4.6A, current capacity = 500mA, formula: data = (10 * current capacity)/current
    print('Sending instruction. Device: %i, Command: %i, Data: %i' % (device, command, data))
    send(ser,device, command, data)
    #time.sleep(1) # wait for 1 second # NO waiting (dont now how long use stepping for blocking)
    # max distance = 25.3969mm

    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4

        #print("Receiving reply " + str(reply))
        #print("Device number: " + str(reply[0]))
        #print("Command number: " +  str(reply[1]))
        print("Requested Current: " + str(replyData) + "[Steps]") #
        print("Absolute Current: " + str(replyData) + "[Steps]") #
        print("Requested Current: " + str(current) + "[A]") #
        print("Absolute Current: " + str(current) + "[A]") #

    except:
        print("No reply was received.")

    print("Closing " + ser.portstr)
    ser.close()
            
def reset(device=0,tty="COM6"):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)

    #device = 0
    command = 36 # factory reset
    #data = position # what units?
    print('Resetting device')
    send(ser,device, command, 0)
    receive(ser)

def settings(data, device=0,tty="COM6"):
    # open serial port
    # replace "/dev/ttyUSB0" with "COM1", "COM2", etc in Windows
    try:
        #ser = serial.Serial("/dev/ttyUSB0", 9600, 8, 'N', 1, timeout=5)   
        ser = serial.Serial(tty, 9600, 8, 'N', 1, timeout=5)   
    except:
        print("Error opening com port. Quitting.")
        sys.exit(0)
    print("Opening " + ser.portstr)

    command = 53 # return settings
    #data = position # what units?
    print('Getting information')
    send(ser,device, command, data)
    try:
        reply = receive(ser)
        # Reply data is calculated from all reply bytes
        replyData = (256.0**3.0*reply[5]) + (256.0**2.0*reply[4]) + (256.0*reply[3]) + (reply[2])
        if reply[5] > 127:
           replyData -= 256.0**4

        print("Requested Information: " + str(replyData) + "[Steps]") #

    except:
        print("No reply was received.")

    print("Closing " + ser.portstr)
    ser.close()

    
    
    
    
    
    
    
    
    
