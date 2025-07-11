import serial
import time


 
# coordinates in um
x_um, y_um, z_um = 100_000, 100_000, 100_000
porta_seriale = 'COM3'
 
# conversion from um to mm
def calculate_mm(micrometri):
    return micrometri / 1000  # CONVERSIONE: 1000 µm = 1 mm
 
def G90_command(gcode): #G90 absolute positioning
   gcode.append("G90")
 
def G21_command(gcode): #set millimeters as unit
   gcode.append("G21")
 
def M17_command(gcode): #activate stepper motors
   gcode.append("M17")
 
def M114_command(gcode): #control locations of each axes
   gcode.append("M114")
   
def M119_command(gcode): #controlo endstop status
   gcode.append("M119")
   
def M84_command(gcode): #disable stepper motors
   gcode.append("M84")
 
def set_position(x,y,z,gcode): #moves linearly to the target point
   gcode.append(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F3000")
 
def M106_command(gcode, fan, power): #set fan on/off | fan: P0, P1, P2 | power: S255 -> max power S0 ->min power
   gcode.append("M106 "+fan+" "+power)

# Comando per tornare a home
def return_Home(assi, gcode):
    gcode.append(f"G28 {assi}")
 
# generation of GCode commands to go to the target point
def generate_gcode(x_um, y_um, z_um):
   x = calculate_mm(x_um)
   y = calculate_mm(y_um)
   z = calculate_mm(z_um)
 
   gcode = []
   
   M17_command(gcode)
   G90_command(gcode)
   G21_command(gcode)
   return_Home("O",gcode)
   set_position(x,y,z,gcode)
   return_Home("O",gcode)
   gcode.append("M84")
   '''
   M106_command(gcode, "P0", "S255")
   M106_command(gcode, "P1", "S255")
   M106_command(gcode, "P2", "S255")
   M106_command(gcode, "P0", "S0")
   M106_command(gcode, "P1", "S0")
   M106_command(gcode, "P2", "S0")
   '''
 
   return gcode

def check_homing_done(serial_connection):
    serial_connection.write(b"M119\n")
    time.sleep(3)
    risposta = serial_connection.readlines()
    for riga in risposta:
        riga_decodificata = riga.decode().strip().lower()
        print("DEBUG:", riga_decodificata)
        if "z_probe: triggered" in riga_decodificata or "z_min: triggered" in riga_decodificata:
            return True
    return False

def setup_begin(ctr_connection):
   ctr_connection.write(("M17"+'\n').encode("ascii"))
   ctr_connection.write(("G90"+'\n').encode("ascii"))
   ctr_connection.write(("G28 X Y Z"+'\n').encode("ascii"))

 


try:
    ctr_connection = serial.Serial(porta_seriale, 115200, timeout=1) #serial communication
    risposta=""
    gcode = generate_gcode(x_um, y_um, z_um) 
    
    

    for line in gcode:
        #time.sleep(3) #attivato per test ventola
        
        ctr_connection.write((line+ '\n').encode("ascii")) #encoding to ascii
        print((line+ '\n'))
        while (risposta!="ok"):
            risposta = ctr_connection.readline().decode().strip()
            print(f"    answer: {risposta}")
        risposta=""
        
    print("connessione stabilita!")
      
    ctr_connection.close()
except Exception as e:
    print(f"Connessione non riuscita: {e}")
