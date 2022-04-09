#!/usr/bin/python
from time import time
import smbus
import math
import tf
from sensor_msgs.msg import Imu
import rospy
import numpy as np


power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68  
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
gyro_x_bias=-250
gyro_y_bias=266
gyro_z_bias=43
accel_x_bias=348
accel_y_bias= 13
accel_z_bias= -16569
g=9.81

bus = smbus.SMBus(1) 
if __name__== "__main__":

    rospy.init_node("imu_read")
    pub= rospy.Publisher("imu_data_raw", Imu, queue_size=1000 )


    rate = rospy.Rate(80)



    

    while not rospy.is_shutdown():
        
        bus.write_byte_data(address, power_mgmt_1, 0)

        imu_data_raw = Imu()
        imu_data_raw.header.stamp=rospy.Time.now()
        imu_data_raw.header.frame_id="base_link"
        imu_data_raw.orientation_covariance = [1e6, 0, 0, 0, 1e6, 0, 0, 0, 1e-6]
                                            
        imu_data_raw.angular_velocity_covariance = imu_data_raw.orientation_covariance
        imu_data_raw.linear_acceleration_covariance = [-1,0,0,0,0,0,0,0,0]
        imu_data_raw.angular_velocity.x =  (read_word_2c(0x43)-gyro_x_bias)/131.0
        imu_data_raw.angular_velocity.y =   (read_word_2c(0x45)-gyro_y_bias)/131.0
        #imu_data_raw.angular_velocity.x = 0.001
        #imu_data_raw.angular_velocity.y = 0.001
        imu_data_raw.angular_velocity.z =  (read_word_2c(0x47)-gyro_z_bias)/131.0
        imu_data_raw.linear_acceleration.x =  (read_word_2c(0x3b)- accel_x_bias)/ 16384.0
        imu_data_raw.linear_acceleration.y = (read_word_2c(0x3d)- accel_y_bias)/ 16384.0
        #imu_data_raw.linear_acceleration.x = 0.001
        #imu_data_raw.linear_acceleration.y = 0.001
        imu_data_raw.linear_acceleration.z = (read_word_2c(0x3f)- accel_z_bias+ 16384.0)/ 16384.0*g

        imu_data_raw.orientation.x = 0
        imu_data_raw.orientation.y = 0
        imu_data_raw.orientation.z =0
        imu_data_raw.orientation.w = 0
        
        pub.publish(imu_data_raw)
        rate.sleep()



