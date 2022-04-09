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


def get_imu_data():
    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)


    gyro_x_bias=-250
    gyro_y_bias=266
    gyro_z_bias=43
    accel_x_bias= 348
    accel_y_bias= 13
    accel_z_bias= -16569

    print ("gyro data")
    print ("---------")

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print
    print ("accelerometer data")
    print ("------------------")

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = (accel_xout- accel_x_bias)/ 16384.0
    accel_yout_scaled = (accel_yout-accel_y_bias) / 16384.0
    accel_zout_scaled = (accel_zout-accel_z_bias+16384) / 16384.0

    print ("gyro_xout_raw: ", gyro_xout)
    print ("gyro_yout_raw: ", gyro_yout)
    print ("gyro_zout_raw: ", gyro_zout)
    print ("gyro_xout: ", gyro_xout-gyro_x_bias, " scaled: ", ((gyro_xout-gyro_x_bias) / 131.001))
    print ("gyro_yout: ", gyro_yout-gyro_y_bias, " scaled: ", ((gyro_yout -gyro_y_bias)/ 131.001))
    print ("gyro_zout: ", gyro_zout-gyro_z_bias, " scaled: ", ((gyro_zout-gyro_z_bias) / 131.001))
    print ("accel_xout: ", accel_xout- accel_x_bias,  " scaled: ", accel_xout_scaled)
    print ("accel_yout: ", accel_yout-accel_y_bias, " scaled: ", accel_yout_scaled)
    print ("accel_zout: ", accel_zout-accel_z_bias+16384, " scaled: ", accel_zout_scaled)

for i in range(5):
    get_imu_data()