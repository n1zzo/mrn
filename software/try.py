import serial
import time

class Connection:
    
    def __init__(self,serial_port,baud):
        self.serial_connection = serial.Serial(serial_port, baud, timeout=1) #serial communication
        
    def set_position(self,x,y,z): #moves linearly to the target point
        x=self.__calculate_mm(x)
        y=self.__calculate_mm(y)
        z=self.__calculate_mm(z)
        
        self.send_command("M114")
        answers = []
        while "ok" not in answers:
            answers.append(self.serial_connection.readline().decode().strip())
            print(answers)
        
        if "X:0.00 Y:0.00 Z:0.00 E:0.00 Count X:0 Y:0 Z:0" not in answers:
            if x!=0.00 and y!=0.00 and z!=0-00: #x=0 y=0 z=0 is a restricted position used only to check if the homing has been performed
                self.send_command(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F3000") 
        else:
            print("ciao")
            self.homing()
            self.send_command(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F3000")                    
             
    def send_command(self,command):
        self.serial_connection.write((command+'\n').encode('ascii'))
    
    def homing(self):
        self.send_command("M17")
        self.send_command("G90")
        self.send_command("G28 X Y Z")
        '''ris = []
        while True:
            ris.append(self.serial_connection.readline().decode().strip())
            print(ris)'''
    
    @staticmethod
    def  __calculate_mm(micrometri):
        return micrometri / 1000  # CONVERSIONE: 1000 µm = 1 mm
    
try: 
    skr_pico = Connection("COM3", 115200)
    #skr_pico.homing()
    skr_pico.set_position(60000,1000000,150000)
except Exception as e:
    print(f"Connessione non riuscita: {e}")