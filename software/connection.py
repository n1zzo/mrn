import serial
import time

class HomingNeededException(Exception):
   """exception raised when nyou must execute homing"""
   pass

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
        
        
        # Check if controller has been power cycle and thus needs homing
        if "X:0.00 Y:0.00 Z:0.00 E:0.00 Count A:0B:0 Z:0" not in answers:
            if x!=0.00 and y!=0.00 and z!=0.00: #x=0 y=0 z=0 is a restricted position used only to check if the homing has been performed
                self.send_command(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F3000") 
                self.send_command("M114")
                print(y)
                
       
        else:
            raise HomingNeededException
                            
             
    def send_command(self,command):
        self.serial_connection.write((command+'\n').encode('ascii'))
    
    def homing(self):
        self.send_command("M17")
        self.send_command("G90")
        self.send_command("M119")
        self.send_command("G28 X Y Z")
        self.send_command("M119")
        
        risposta=" "
        while risposta!="z_min: TRIGGERED" :
            risposta=self.serial_connection.readline().decode().strip()
            print(risposta)
        
       
    
    @staticmethod
    def  __calculate_mm(micrometri):
        return micrometri / 1000  # CONVERSIONE: 1000 µm = 1 mm

def main():
    try: 
        skr_pico = Connection("COM3", 115200)  
    except Exception as e:
        print(f"Connessione non riuscita: {e}")
        exit(-1)
    #skr_pico.homing()
    try:
        print("ciao")
        skr_pico.set_position(6000,10000,15000)
    except HomingNeededException as e:
        print(e)
        skr_pico.homing()
        print("done!")
        skr_pico.set_position(6000,10000,15000)
    skr_pico.serial_connection.close()

if __name__ == "__main__":
    main()