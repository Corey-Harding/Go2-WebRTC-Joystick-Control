# Unitree Go2 Webrtc Controller by Corey Harding
# Requires https://github.com/legion1581/go2_webrtc_connect
# Includes code from Legion1581 https://github.com/legion1581/go2_webrtc_connect
# Unfinished crude implementation of the wireless_controller

import asyncio
import threading
import pygame
from time import time
import ctypes
import json
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from go2_webrtc_driver.constants import RTC_TOPIC, SPORT_CMD
from config_file import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Disable pygame welcome message

import asyncio
import pygame
from time import time
import numpy as np
from config_file import *

async def main():

    #Define Keys
    keys =       0b0000000000000000
    #Bitmask Positions
    BITMASK_R1 =     0b0000000000000001
    BITMASK_L1 =     0b0000000000000010
    BITMASK_START =  0b0000000000000100
    BITMASK_SELECT = 0b0000000000001000
    BITMASK_R2 =     0b0000000000010000
    BITMASK_L2 =     0b0000000000100000
    BITMASK_F1 =     0b0000000001000000
    BITMASK_F3 =     0b0000000010000000
    BITMASK_A =      0b0000000100000000
    BITMASK_B =      0b0000001000000000
    BITMASK_X =      0b0000010000000000
    BITMASK_Y =      0b0000100000000000
    BITMASK_D_PAD_UP =     0b0001000000000000
    BITMASK_D_PAD_RIGHT =  0b0010000000000000
    BITMASK_D_PAD_DOWN =   0b0100000000000000
    BITMASK_D_PAD_LEFT =   0b1000000000000000

    Lx = 0
    Ly = 0
    Rx = 0
    Ry = 0


    try:
        #Initialize pygame joystick support
        pygame.init()
        clock = pygame.time.Clock()
        if pygame.joystick.get_count() == 0:
            print("No joystick detected...")
            return
        joystick = pygame.joystick.Joystick(JOYSTICK_NUMBER)
        joystick.init()
        print("Joystick Initialized...")

        #Initialize go2_webrtc_driver
        conn = WEBRTC_CONNECTION_TYPE
        await conn.connect() # Connect to the WebRTC service.

        #print(f"Keys variable initialized as: {bin(keys)[2:].zfill(16)}")

    except ValueError as e:
        # Log any value errors that occur during the process.
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

    run = True

    while run:
        for event in pygame.event.get():
            #Quit pygame while loop
            if event.type == pygame.QUIT:
                print("Closing application...")
                run = False

            #Test Joystick Button Press Events
            elif event.type == pygame.JOYBUTTONDOWN:
                #print(f"BUTTON ({event.button}) PRESSED")
                if event.button == START:
                    #print("START")
                    keys |= BITMASK_START # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == SELECT:
                    #print("SELECT")
                    keys |= BITMASK_SELECT # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == A_BUTTON:
                    #print("A_BUTTON")
                    keys |= BITMASK_A # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == B_BUTTON:
                    #print("B_BUTTON")
                    keys |= BITMASK_B # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == X_BUTTON:
                    #print("X_BUTTON")
                    keys |= BITMASK_X # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == Y_BUTTON:
                    #print("Y_BUTTON")
                    keys |= BITMASK_Y # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == LEFT_BUMPER:
                    #print("LEFT_BUMPER")
                    keys |= BITMASK_L1 # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == RIGHT_BUMPER:
                    #print("RIGHT_BUMPER")
                    keys |= BITMASK_R1 # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == F1:
                    #print("F1")
                    keys |= BITMASK_F1 # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == F3:
                    #print("F3")
                    keys |= BITMASK_F3 # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")

            #Test Joystick Button Release Events
            elif event.type == pygame.JOYBUTTONUP:
                #print(f"BUTTON ({event.button}) RELEASED")
                if event.button == START:
                    #print("START")
                    keys &= ~ BITMASK_START # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == SELECT:
                    #print("SELECT")
                    keys &= ~ BITMASK_SELECT # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == A_BUTTON:
                    #print("A_BUTTON")
                    keys &= ~ BITMASK_A # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == B_BUTTON:
                    #print("B_BUTTON")
                    keys &= ~ BITMASK_B # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == X_BUTTON:
                    #print("X_BUTTON")
                    keys &= ~ BITMASK_X # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == Y_BUTTON:
                    #print("Y_BUTTON")
                    keys &= ~ BITMASK_Y # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == LEFT_BUMPER:
                    #print("LEFT_BUMPER")
                    keys &= ~ BITMASK_L1 # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == RIGHT_BUMPER:
                    #print("RIGHT_BUMPER")
                    keys &= ~ BITMASK_R1 # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == F1:
                    #print("F1")
                    keys &= ~ BITMASK_F1 # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.button == F3:
                    #print("F3")
                    keys &= ~ BITMASK_F3 # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")

            #Test Joystick Hats
            elif event.type == pygame.JOYHATMOTION:
                #print(f"HAT NUMBER: {str(event.hat)} HAT POSITION: {str(event.value)}")
                if event.value == (0, 0):
                    #print("D_PAD_NEUTRAL")
                    keys &= ~ BITMASK_D_PAD_UP # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_DOWN # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_LEFT # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_RIGHT # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.value == D_PAD_UP:
                    #print("D_PAD_UP")
                    keys |= BITMASK_D_PAD_UP # Set bit to 1
                    keys &= ~ BITMASK_D_PAD_DOWN # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_LEFT # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_RIGHT # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.value == D_PAD_DOWN:
                    #print("D_PAD_DOWN")
                    keys &= ~ BITMASK_D_PAD_UP # Set bit to 0
                    keys |= BITMASK_D_PAD_DOWN # Set bit to 1
                    keys &= ~ BITMASK_D_PAD_LEFT # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_RIGHT # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.value == D_PAD_LEFT:
                    #print("D_PAD_LEFT")
                    keys &= ~ BITMASK_D_PAD_UP # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_DOWN # Set bit to 0
                    keys |= BITMASK_D_PAD_LEFT # Set bit to 1
                    keys &= ~ BITMASK_D_PAD_RIGHT # Set bit to 0
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                if event.value == D_PAD_RIGHT:
                    #print("D_PAD_RIGHT")
                    keys &= ~ BITMASK_D_PAD_UP # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_DOWN # Set bit to 0
                    keys &= ~ BITMASK_D_PAD_LEFT # Set bit to 0
                    keys |= BITMASK_D_PAD_RIGHT # Set bit to 1
                    #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")

            #Test Joystick Axis
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == LEFT_TRIGGER_AXIS or event.axis == RIGHT_TRIGGER_AXIS:
                    #print(f"AXIS: ({str(event.axis)}) POSITION: ({str(event.value)})")
                    if event.axis == LEFT_TRIGGER_AXIS and event.value > LT_NEUTRAL:
                        #print(f"LEFT_TRIGGER_AXIS Postion: ({str(event.value)})")
                        keys |= BITMASK_L2 # Set bit to 1
                        #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                    else:
                        #print(f"LEFT_TRIGGER_AXIS Postion: ({str(event.value)})")
                        keys &= ~ BITMASK_L2 # Set bit to 0
                        #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                    if event.axis == RIGHT_TRIGGER_AXIS and event.value > LT_NEUTRAL:
                        #print(f"RIGHT_TRIGGER_AXIS Postion: ({str(event.value)})")
                        keys |= BITMASK_R2 # Set bit to 1
                        #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")
                    else:
                        #print(f"RIGHT_TRIGGER_AXIS Postion: ({str(event.value)})")
                        keys &= ~ BITMASK_R2 # Set bit to 0
                        #print(f"Keys variable: {bin(keys)[2:].zfill(16)}")

        Lx = joystick.get_axis(LEFT_X_AXIS)*Lxsensitivity # Left analog stick X-axis
        Ly = -joystick.get_axis(LEFT_Y_AXIS)*Lysensitivity # Left analog stick Y-axis
        Rx = joystick.get_axis(RIGHT_X_AXIS)*Rxsensitivity # Right analog stick X-axis
        Ry = -joystick.get_axis(RIGHT_Y_AXIS)*Rysensitivity # Right analog stick Y-axis
        if (abs(Lx) > DEADZONE or abs(Ly) > DEADZONE or abs(Rx) > DEADZONE):
            try:
                print(f"Sending command( lx: {Lx}, ly: {Ly}, rx: {Rx}, ry: {Ry}, keys: 0 )")
                response = await asyncio.wait_for(conn.datachannel.pub_sub.publish(
                RTC_TOPIC["WIRELESS_CONTROLLER"],
                {
                    "lx": Lx,
                    "ly": Ly,
                    "rx": Rx,
                    "ry": Ry,
                    "keys": 0
                }
                ),
                timeout = .1
                )
                print(f"Response: {response}")
                await asyncio.sleep(.1)
            except asyncio.TimeoutError:
                #print("Timeout Error")
                timeout = .1

        if keys > 0:
            try:
                print(f"Sending command( lx: 0, ly: 0, rx: 0, ry: 0, keys: {keys} )")
                response = await asyncio.wait_for(conn.datachannel.pub_sub.publish(
                RTC_TOPIC["WIRELESS_CONTROLLER"],
                {
                    "lx": 0,
                    "ly": 0,
                    "rx": 0,
                    "ry": 0,
                    "keys": keys
                }
                ),
                timeout = .1
                )
                print(f"Response: {response}")
                await asyncio.sleep(.5)
            except asyncio.TimeoutError:
                #print("Timeout Error")
                timeout = .1

        #Workaround to keep webrtc connection from randomly disconnecting
        def lowstate_callback(message):
            current_message = message['data']
        conn.datachannel.pub_sub.subscribe(RTC_TOPIC['LOW_STATE'], lowstate_callback)
        await asyncio.sleep(.1)

        clock.tick(CONTROLLER_FPS_LIMIT) # Limit how many times a second the script is able to run
        


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully.
        print("\nProgram interrupted by user")
        pygame.quit()