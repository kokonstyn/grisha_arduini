from http.server import BaseHTTPRequestHandler,HTTPServer
from threading import Thread
import sound
import os
import sys
import time
import serial
import serial.tools.list_ports

ev = sound.IAudioEndpointVolume.get_default()
vol = round(ev.GetMasterVolumeLevelScalar()*100)


def f():
        
    class HttpProcessor(BaseHTTPRequestHandler):
        def do_GET(self):
            print('Считано ',self.path[1:])
            global vol

    #ответ на опрос датчика
            if self.path[1:]=='state':
                            
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write(str(vol).encode())
                print('Ответ датчику ',vol)
                
    #оброботка гета на звук
            if (self.path[1:].isdigit())and(int(self.path[1:])<=100):
                            
                soundlevel = int(self.path[1:])/100
                vol = self.path[1:]
                print('Отправлено ',soundlevel)
                                      
                if soundlevel>0.2:
                    ev.SetMute(0)
                ev.SetMasterVolumeLevelScalar(soundlevel)
                
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write(str(soundlevel).encode())
            

    serv = HTTPServer(("",80),HttpProcessor)
    serv.serve_forever()



def f_2():

    global vol
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
                            vol = round(soundlevel*100)
                            print(soundlevel)
                            try:

                                    if soundlevel>0.2:
                                        ev.SetMute(0)
                                    ev.SetMasterVolumeLevelScalar(soundlevel)
                                                                                      
                            except Exception:
                                    time.sleep(1)
            
            except serial.SerialException:
                    print('а всьо')
                    time.sleep(5)

th_1, th_2 = Thread(target=f), Thread(target = f_2)

if __name__ == '__main__':
    th_1.start(), th_2.start()
    th_1.join(), th_2.join()

