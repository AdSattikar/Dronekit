from dronekit import connect,VehicleMode, LocationGlobalRelative,Vehicle
import time 
from pymavlink import mavutil
vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)

def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("waiting to initialize.....")
        time.sleep(1)
    print("arming motors")

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True 

    while not vehicle.armed:
        print("waiting to arm")
        time.sleep(1)



    print("Taking off....")
    vehicle.simple_takeoff(altitude)

    while True:
        print('Altitude {}'.format(vehicle.location.global_relative_frame.alt))
        if vehicle.location.global_relative_frame.alt >= 0.95 * altitude:
            print("Target altitude reached ")
            break
        time.sleep(1)
def send_ned_velocity(Vx, Vy, Vz, duration):
 
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,      
        0, 0,  
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
        0b0000111111000111, 
        0, 0, 0, 
        Vx, Vy, Vz, 
        0, 0, 0, 
        0, 0)   

def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 
   
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, 
        0, #confirmation
        heading,                   # param 1, yaw in degrees
        0,                         # param 2, yaw speed deg/s
        1,                         # param 3, direction -1 ccw, 1 cw
        is_relative,               # param 4, relative offset 1, absolute angle 0
        0, 0, 0)                   # param 5 ~ 7 not used
    vehicle.send_mavlink(msg)

arm_and_takeoff(30)
condition_yaw(90)
send_ned_velocity(0,10,0,5)
