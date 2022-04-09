#!/usr/bin/python
from ast import If
from audioop import bias
import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

#print ("gyro data")
#print ("---------")

gyro_x_list=[]
gyro_y_list=[]
gyro_z_list=[]
accel_x_lsit=[]
accel_y_lsit=[]
accel_z_lsit=[]

for i in range (2000):

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)



    #print
    #print ("accelerometer data")
    #print ("------------------")

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    gyro_x_list.append(gyro_xout)
    gyro_y_list.append(gyro_yout)
    gyro_z_list.append(gyro_zout)
    accel_x_lsit.append(accel_xout)
    accel_y_lsit.append(accel_yout)
    accel_z_lsit.append(accel_zout)

gyro_x_bias = sum(  gyro_x_list)/len(  gyro_x_list)
gyro_y_bias = sum(  gyro_y_list)/len(  gyro_x_list)
gyro_z_bias = sum(  gyro_z_list)/len(  gyro_x_list)

accel_x_bias = sum( accel_x_lsit)/len(accel_x_lsit)
accel_y_bias = sum( accel_y_lsit)/len(accel_x_lsit)
accel_z_bias = sum( accel_z_lsit)/len(accel_x_lsit)


print(gyro_x_bias, gyro_y_bias, gyro_z_bias)
print(accel_x_bias, accel_y_bias, accel_z_bias )

accel_xout_scaled = (accel_xout- accel_x_bias)/ 16384.0
accel_yout_scaled = (accel_yout-accel_y_bias) / 16384.0
accel_zout_scaled = (accel_zout-accel_z_bias+16384) / 16384.0

print ("gyro_xout: ", gyro_xout-gyro_x_bias, " scaled: ", ((gyro_xout-gyro_x_bias) / 131.001))
print ("gyro_yout: ", gyro_yout-gyro_y_bias, " scaled: ", ((gyro_yout -gyro_y_bias)/ 131.001))
print ("gyro_zout: ", gyro_zout-gyro_z_bias, " scaled: ", ((gyro_zout-gyro_z_bias) / 131.001))
print ("accel_xout: ", accel_xout- accel_x_bias,  " scaled: ", accel_xout_scaled)
print ("accel_yout: ", accel_yout-accel_y_bias, " scaled: ", accel_yout_scaled)
print ("accel_zout: ", accel_zout-accel_z_bias+16384, " scaled: ", accel_zout_scaled)

#print ("x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
#print ("y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))