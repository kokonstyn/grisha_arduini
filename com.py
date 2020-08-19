import os
import sys
import time
import serial
import serial.tools.list_ports
import sound

while True:
        print('Search...')
        ports = serial.tools.list_ports.comports(include_links=False)
        for port in ports :
            print('Find port '+ port.device)
        try:
                ser = serial.Serial(port.device)
                if ser.isOpen():
                        ser.close()
      
                ser = serial.Serial(port.device, 9600)
                ser.reset_input_buffer( )
                ser.reset_output_buffer( )
                print('Connect ' + ser.name)

                while True:
                                              
                        r=""
                        for i in filter( str.isdigit , str(ser.readline())) :
                            r = r + i

                        soundlevel = int(r)/100
                        if soundlevel >= 1.0:
                                soundlevel = 1.0
                        print(soundlevel)
                        try:
                                ev = sound.IAudioEndpointVolume.get_default()
                                vol = ev.GetMasterVolumeLevelScalar()
                                if soundlevel>0.2:
                                    ev.SetMute(0)
                                ev.SetMasterVolumeLevelScalar(soundlevel)
                        except Exception:
                                time.sleep(1)
                                print('а всьо?')
        
        except serial.SerialException:
                print('а всьо')
                time.sleep(5)
                
        



