import pygame
from dronekit import connect,VehicleMode, LocationGlobalRelative,Vehicle
import time 
from pymavlink import mavutil

pygame.init()  
# sets the window title  
pygame.display.set_caption(u'Keyboard events')  
# sets the window size  
s = pygame.display.set_mode((400, 400))  

vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)

def arm_and_takeoff(altitude):# takes off to the altitude entered
    while not vehicle.is_armable: #wait until change is observed
        print("Waiting to Initialize.....")
        time.sleep(1)
    print("Arming Motors")

    vehicle.mode = VehicleMode("GUIDED") #flying copter autonomously without a predefined mission
    vehicle.armed = True  #vehicle is armable before flying

    while not vehicle.armed: 
        print("Waiting to Arm")
        time.sleep(1)



    print("Taking off....")
    vehicle.simple_takeoff(altitude) 

    while True:
        print('Altitude {}'.format(vehicle.location.global_relative_frame.alt))
        if vehicle.location.global_relative_frame.alt >= 0.95 * altitude:
            print("Target altitude reached ")
            break
        time.sleep(1)

def send_ned_velocity(Vx, Vy, Vz, duration): # NED = North East Down relative to the frame of Home location
 
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,      
        0, 0,  
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
        0b0000111111000111, 
        0, 0, 0, 
        Vx, Vy, Vz, 
        0, 0, 0, 
        0, 0)    

    # send command to vehicle on 1 Hz cycle
    for i in range(0,duration):
        vehicle.send_mavlink(msg)
        

    
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
        
    for i in range(0,heading):
        # send command to vehicle
        vehicle.send_mavlink(msg)

def Key():
    while True :
        event = pygame.event.wait()  
        if event.type == pygame.QUIT:
            print("Returning to Launch") # returns to launch position when the pygame window is closed
            vehicle.mode = VehicleMode("RTL")    
            break  
        #--> pressed
        if event.type in (pygame.KEYDOWN, pygame.KEYUP): # reads a event i.e whether a key is pressed or released
            key_name = pygame.key.name(event.key)
            key_name = key_name.upper() # converts the key read into uppercase
            if event.type == pygame.KEYDOWN:  
            # prints on the console the key pressed  
                print(u'"{}" key pressed'.format(key_name)) # formats the ASCII code to a String 
                if key_name == "UP":
                    i = int(input("Enter Yaw in degrees "))
                    condition_yaw(i)
                elif key_name == "W":
                    print("Move forward")
                    send_ned_velocity(20,0,0,1)
                    time.sleep(5)
                elif key_name == "A":
                    print("Move Left")
                    send_ned_velocity(0,-20,0,1)
                elif key_name == "D":
                    print("Move Right")
                    send_ned_velocity(0,20,0,1)
                elif key_name == "S":
                    print("Move Back")
                    send_ned_velocity(-20,0,0,1)
                else:
                    print("Please Enter only W, A, S, D and UP keys to control the vehicle")

arm_and_takeoff(30)
Key()
