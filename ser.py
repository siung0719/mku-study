import serial
import random
import time
#ser = serial.Serial('COM14', 9600, parity='N', stopbits=1)

ser = serial.Serial('COM14', 115200)
while True:
    pan=random.randint(-100,100)
    til=random.randint(-100,100)
    data='p'+str(pan).zfill(5)+'t'+str(til).zfill(5)+'\n'
    data=data.encode()
    ser.write(data)
    print(data)
    #time.sleep(0.1)
    