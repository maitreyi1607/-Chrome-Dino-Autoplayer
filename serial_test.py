import serial
import time

arduino = serial.Serial('COM5', 9600, timeout=1)

time.sleep(2)

print("Arduino Connected!")

arduino.write(b'J')

print("Jump Command Sent!")

time.sleep(1)

arduino.close()

print("Connection Closed.")