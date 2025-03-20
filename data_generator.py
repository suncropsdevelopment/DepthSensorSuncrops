import serial
import time

class SerialWrapper:
    def __init__(self):
        self.com = "COM1"
        self.baudrate = 9600
        self.timeout = 1
        self.ser = serial.Serial(self.com,self.baudrate,timeout=self.timeout)
        self.generate_data()
        
    
    def generate_data(self):
        
        try:
            print(f"Connected to {self.com} at {self.baudrate} baud.")
            
            data = ["$SDDBT,1.05,f,2.0,M,0.0,F*03,20,C\r\n",
                    "$SDDBT,1.05,f,2.12,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,2.34,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,3.4,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,3.7,M,0.0,F*03,24,C\r\n",
                    "$SDDBT,1.05,f,4.67,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,5.1,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,5.21,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,5.5,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,5.6,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,6.32,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,6.34,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,7.6,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,7.8,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,8.56,M,0.0,F*03,23,C\r\n"
                    "$SDDBT,1.05,f,9.0,M,0.0,F*03,20,C\r\n",
                    "$SDDBT,1.05,f,10.12,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,11.34,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,11.4,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,11.7,M,0.0,F*03,24,C\r\n",
                    "$SDDBT,1.05,f,12.67,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,12.81,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,13.21,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,13.5,M,0.0,F*03,21,C\r\n",
                    "$SDDBT,1.05,f,14.1,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,14.32,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,14.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,15.1,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,16.1,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,16.56,M,0.0,F*03,24,C\r\n",
                    "$SDDBT,1.05,f,17.56,M,0.0,F*03,25,C\r\n",
                    "$SDDBT,1.05,f,19.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,20.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,21.26,M,0.0,F*03,26,C\r\n",
                    "$SDDBT,1.05,f,22.23,M,0.0,F*03,26,C\r\n",
                    "$SDDBT,1.05,f,22.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,22.81,M,0.0,F*03,26,C\r\n",
                    "$SDDBT,1.05,f,23.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,24.26,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,25.23,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,26.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,27.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,28.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,29.26,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,30.23,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,31.56,M,0.0,F*03,26,C\r\n",
                    "$SDDBT,1.05,f,32.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,33.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,34.23,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,35.56,M,0.0,F*03,24,C\r\n",
                    "$SDDBT,1.05,f,36.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,37.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,38.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,39.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,40.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,41.56,M,0.0,F*03,25,C\r\n",
                    "$SDDBT,1.05,f,42.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,42.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,43.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,44.56,M,0.0,F*03,26,C\r\n",
                    "$SDDBT,1.05,f,45.81,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,46.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,47.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,48.56,M,0.0,F*03,23,C\r\n",
                    "$SDDBT,1.05,f,49.81,M,0.0,F*03,25,C\r\n",
                    "$SDDBT,1.05,f,50.56,M,0.0,F*03,28,C\r\n",
                    
                    ]
            
            while True:
                for i in data:
                    self.ser.write(i.encode())
                    print(i)
                    time.sleep(1)
                
            
        except serial.SerialException as e:
            print(f"Error: {e}")

def main():
    ser = SerialWrapper()
    
if __name__=="__main__":
    main()
    