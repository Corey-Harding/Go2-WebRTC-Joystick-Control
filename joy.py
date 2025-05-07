# Unitree Go2 Webrtc Controller by Corey Harding
# Requires https://github.com/legion1581/go2_webrtc_connect
# Based on code by
# Robotics Club - https://roboticsclub.com.br/cool/controller
# DannyH in theroboverse Discord
# Legion1581 https://github.com/legion1581/go2_webrtc_connect
# oscgonfer https://github.com/oscgonfer/iron-skulls-dog/

import asyncio
import threading
import pygame
from time import time
import ctypes
import json
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from go2_webrtc_driver.constants import RTC_TOPIC, SPORT_CMD

async def main():
    pygame.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick detected...")
        return
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick Initialized...")

    #Analog Stick Sensitivity
    deadzone = 0.1
    Lxsensitivity = 1
    Lysensitivity = 1
    Rxsensitivity = 1
    Rysensitivity = 1
    ObstacleAvoidMultiplier = 1.25 # Increase movement speed in obstacle avoidance mode

    #Define Some Toggles
    WalkUpright = False
    StandOut = False
    StandDown = False
    Sit = False
    ContinuousGait = False
    aiMode = False
    ObstaclesAvoid = True

    #Initialize some values
    Brightness = 0
    Gait = 1
    DogMode = 1 # 1 Walk, 2 Standing
    Moving = False

    try:
        # Choose a connection method (uncomment the correct one)
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.12.1")
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, serialNumber="B42D2000XXXXXXXX")
        # conn = Go2WebRTCConnection(WebRTCConnectionMethod.Remote, serialNumber="B42D2000XXXXXXXX", username="email@gmail.com", password="pass")
        conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)

        # Connect to the WebRTC service.
        await conn.connect()

        ####### NORMAL MODE ########
        print("Checking current motion mode...")

        # Get the current motion_switcher status
        response = await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["MOTION_SWITCHER"], 
            {"api_id": 1001}
        )

        if response['data']['header']['status']['code'] == 0:
            data = json.loads(response['data']['data'])
            current_motion_switcher_mode = data['name']
            print(f"Current motion mode: {current_motion_switcher_mode}")

        # Switch to "normal" mode if not already
        if current_motion_switcher_mode != "normal":
            print(f"Switching motion mode from {current_motion_switcher_mode} to 'normal'...")
            await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"], 
                {
                    "api_id": 1002,
                    "parameter": {"name": "normal"}
                }
            )
            await asyncio.sleep(5)  # Wait

        # Perform a "Hello" movement
        print("Performing 'Hello' movement...")
        await conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"], 
            {"api_id": SPORT_CMD["Hello"]}
        )

        await asyncio.sleep(.25)  # Wait
        
    except ValueError as e:
        # Log any value errors that occur during the process.
        logging.error(f"An error occurred: {e}")

    while True:
        pygame.event.pump()

        # Note Inverted Axis (-) For Controller Setup * Sensitivity Multiplier for more or less movement below 1=less sensitive above 1=more sensitive
        Lx = -joystick.get_axis(0)*Lxsensitivity # Left analog stick X-axis
        Ly = -joystick.get_axis(1)*Lysensitivity # Left analog stick Y-axis
        Rx = -joystick.get_axis(3)*Rxsensitivity # Right analog stick X-axis
        Ry = -joystick.get_axis(4)*Rysensitivity # Right analog stick Y-axis

        if DogMode == 1: #Move

            # Check obstacle Avoidance Mode
            response = await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["OBSTACLES_AVOID"], 
                {"api_id": 1002}
            )

            if response['data']['header']['status']['code'] == 0:
                data = json.loads(response['data']['data'])
                ObstaclesAvoid = data['enable']

            if (abs(Lx) > deadzone or abs(Ly) > deadzone or abs(Rx) > deadzone):
                Moving = True
                if ObstaclesAvoid == False:
                    print(f"Sending move command(Obstacle Avoidance:Off)...")
                    await conn.datachannel.pub_sub.publish_request_new(
                     RTC_TOPIC["SPORT_MOD"],
                     {
                         "api_id": SPORT_CMD["Move"],
                         "parameter": {"x": Ly, "y": Lx, "z": Rx}
                     }
                     )
                    await asyncio.sleep(0.25)
                elif ObstaclesAvoid == True:
                    print(f"Sending move command(Obstacle Avoidance:On)")
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["OBSTACLES_AVOID"],
                        {
                            "api_id": 1004,
                            "parameter": {"is_remote_commands_from_api": True}
                        }
                    )
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["OBSTACLES_AVOID"],
                        {
                            "api_id": 1003,
                            "parameter": {"x": Ly*ObstacleAvoidMultiplier, "y": Lx*ObstacleAvoidMultiplier, "yaw": Rx*ObstacleAvoidMultiplier, "mode": 0}
                        }
                    )
                    await asyncio.sleep(0.25)
            elif Moving == True & ObstaclesAvoid == True:
                print(f"Stop move command(Obstacle Avoidance:On)")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["OBSTACLES_AVOID"],
                    {
                        "api_id": 1003,
                        "parameter": {"x": 0, "y": 0, "yaw": 0, "mode": 0}
                    }
                )
                await asyncio.sleep(0.25)
                Moving = False

        elif DogMode == 2: #Standing
            if abs(Ry) > deadzone or abs(Lx) > deadzone or abs(Rx) > deadzone:
                print(f"Sending Euler(Pose) movement...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"],
                    {
                        "api_id": SPORT_CMD["Euler"],
                        "parameter": {"x": Lx, "y": Ry, "z": Rx}
                    }
                )
                await asyncio.sleep(0.25)
        
        lb_pressed = joystick.get_button(4)  # LB
        rb_pressed = joystick.get_button(5)  # RB
        lt_value = joystick.get_axis(2)  # LT
        rt_value = joystick.get_axis(5)  # RT

        hat_state = joystick.get_hat(0)

        if hat_state == (0, 1):  # Dpad Up
            if lb_pressed == True:
                # Toggle WalkUpright Mode
                WalkUpright = not WalkUpright #Toggle
                print("Toggling WalkUpright Mode...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {
                        "api_id": 1050,
                        "parameter": {"data": WalkUpright}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            else:
                print("Performing Recovery Stand...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {
                        "api_id": 1006,
                        "parameter": {}
                    }
                )
                await asyncio.sleep(.25)  # Wait

        if hat_state == (0, -1):  # Dpad Down
            if lb_pressed == True:
                # Toggle StandOut Mode (Handstand Walk)
                StandOut = not StandOut #Toggle
                print("Toggling StandOut Mode...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {
                        "api_id": SPORT_CMD["StandOut"],
                        "parameter": {"data": StandOut}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            else:
                # Toggle Stand Down movement (Crouch)
                StandDown = not StandDown
                if StandDown == True:
                    print("Performing 'Stand Down' movement...")
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["SPORT_MOD"], 
                       {"api_id": SPORT_CMD["StandDown"]}
                	)
                    await asyncio.sleep(.25)  # Wait
                elif StandDown == False:
                    if aiMode == False and ObstaclesAvoid == True:
                        print("Performing 'Stand Up' movement...")
                        await conn.datachannel.pub_sub.publish_request_new(
                            RTC_TOPIC["SPORT_MOD"], 
                            {"api_id": SPORT_CMD["StandUp"]}
                            )
                        await asyncio.sleep(.25)  # Wait
                    elif aiMode == True:
                        print("Performing 'BalanceStand' movement...")
                        await conn.datachannel.pub_sub.publish_request_new(
                            RTC_TOPIC["SPORT_MOD"], 
                            {"api_id": SPORT_CMD["BalanceStand"]}
                            )
                        await asyncio.sleep(.25)  # Wait
                    elif ObstaclesAvoid == False:
                        print("Performing Recovery Stand...")
                        await conn.datachannel.pub_sub.publish_request_new(
                            RTC_TOPIC["SPORT_MOD"], 
                            {
                                "api_id": 1006,
                                "parameter": {}
                            }
                        )
                        await asyncio.sleep(.25)  # Wait

        if hat_state == (-1, 0): # Dpad Left
            ObstaclesAvoid = not ObstaclesAvoid
            await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["OBSTACLES_AVOID"], 
                {
                    "api_id": 1001,
                    "parameter": {"enable": ObstaclesAvoid}
                }
            )
            await asyncio.sleep(.25)  # Wait
            print(f"Setting obstacle avoidance status: {ObstaclesAvoid}")

        if hat_state == (1, 0):  # Dpad Right
            #Toggle Headlight Brightness
            if Brightness == 0:
                Brightness = 25
                print("Setting headlight brightness to 25%...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["VUI"], 
                    {
                        "api_id": 1005,
                        "parameter": {"brightness": 2.5}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            elif Brightness == 25:
                Brightness = 50
                print("Setting headlight brightness to 50%...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["VUI"], 
                    {
                        "api_id": 1005,
                        "parameter": {"brightness": 5}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            elif Brightness == 50:
                Brightness = 75
                print("Setting headlight brightness to 75%...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["VUI"], 
                    {
                        "api_id": 1005,
                        "parameter": {"brightness": 7.5}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            elif Brightness == 75:
                Brightness = 100
                print("Setting headlight brightness to 100%...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["VUI"], 
                    {
                        "api_id": 1005,
                        "parameter": {"brightness": 10}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            elif Brightness == 100:
                Brightness = 0
                print("Setting headlight brightness to 0%...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["VUI"], 
                    {
                        "api_id": 1005,
                        "parameter": {"brightness": 0}
                    }
                )
                await asyncio.sleep(.25)  # Wait

        if joystick.get_button(6):  # Select
            print("Switch to Damping mode...")
            await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {
                    "api_id": 1001,
                    "parameter": {}
                }
            )
            await asyncio.sleep(.25)  # Wait

        if joystick.get_button(7):  # Start
            if lb_pressed == True: # Toggle AI Mode
                aiMode = not aiMode # Toggle
                if aiMode == True: # Activate AI Mode
                    response = await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["MOTION_SWITCHER"], 
                        {"api_id": 1001}
                    )
                    if response['data']['header']['status']['code'] == 0:
                        data = json.loads(response['data']['data'])
                        current_motion_switcher_mode = data['name']
                        print(f"Current motion mode: {current_motion_switcher_mode}")
                    # Switch to "ai" mode if not already
                    if current_motion_switcher_mode == "normal":
                        print(f"Switching motion mode from {current_motion_switcher_mode} to 'ai'...")
                        await conn.datachannel.pub_sub.publish_request_new(
                            RTC_TOPIC["MOTION_SWITCHER"], 
                            {
                                "api_id": 1002,
                                "parameter": {"name": "ai"}
                            }
                        )
                        await asyncio.sleep(5)  # Wait
                elif aiMode == False: # Activate Sport Mode
                    response = await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["MOTION_SWITCHER"], 
                        {"api_id": 1001}
                    )
                    if response['data']['header']['status']['code'] == 0:
                        data = json.loads(response['data']['data'])
                        current_motion_switcher_mode = data['name']
                        print(f"Current motion mode: {current_motion_switcher_mode}")
                    # Switch to "normal" mode if not already
                    if current_motion_switcher_mode != "normal":
                        print(f"Switching motion mode from {current_motion_switcher_mode} to 'normal'...")
                        await conn.datachannel.pub_sub.publish_request_new(
                            RTC_TOPIC["MOTION_SWITCHER"], 
                            {
                                "api_id": 1002,
                                "parameter": {"name": "normal"}
                            }
                        )
                        await asyncio.sleep(5)  # Wait
            else: # Balance Mode (Unlock)
                print("Switching to Balance Mode...")
                RTC_TOPIC["SPORT_MOD"], 
                {
                    "api_id": 1002, # Switch to Balance Mode
                    "parameter": {}
                }
                await asyncio.sleep(.25)  # Wait

        if joystick.get_button(0):  # A
            Sit = not Sit #Toggle
            if Sit == True:
                print("Toggling 'Sit' movement...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {"api_id": SPORT_CMD["Sit"]}
                )
                await asyncio.sleep(.25)  # Wait
            elif Sit == False:
                print("Toggling 'Sit' movement...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {"api_id": SPORT_CMD["RiseSit"]}
                )
                await asyncio.sleep(.25)  # Wait

        if joystick.get_button(1):  # B
            print("Switch to 'FingerHeart' movement...")
            await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {"api_id": SPORT_CMD["FingerHeart"]}
            )
            await asyncio.sleep(.25)  # Wait

        if joystick.get_button(2):  # X
            print("Switch to 'WiggleHips' movement...")
            await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {"api_id": SPORT_CMD["WiggleHips"]}
            )
            await asyncio.sleep(.25)  # Wait

        if joystick.get_button(3):  # Y
            print("Switch to 'Hello' movement...")
            await conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"], 
                {"api_id": SPORT_CMD["Hello"]}
            )
            await asyncio.sleep(.25)  # Wait

        if lt_value > 0: # Left Trigger
            #Toggle Pose
            if DogMode == 1:
                DogMode = 2
                print("Pose Mode On...")
            elif DogMode == 2:
                DogMode = 1
                print("Pose Mode Off...")
            await asyncio.sleep(.25)  # Wait

        if rt_value > 0: # Right Trigger
            if rb_pressed == True:
                # Toggle Continuous Gait
                ContinuousGait = not ContinuousGait #Toggle
                print("Toggling Continuous Gait...")
                await conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"], 
                    {
                        "api_id": 1019,
                        "parameter": {"data": ContinuousGait}
                    }
                )
                await asyncio.sleep(.25)  # Wait
            else:
                #Toggle Gaits
                if Gait == 1:
                    Gait = 2
                    print("Setting gait 2...")
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["SPORT_MOD"], 
                        {
                            "api_id": 1011,
                            "parameter": {"data": 2}
                        }
                    )
                    await asyncio.sleep(.25)  # Wait
                elif Gait == 2:
                    Gait = 3
                    print("Setting gait 3...")
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["SPORT_MOD"], 
                        {
                            "api_id": 1011,
                            "parameter": {"data": 3}
                        }
                    )
                    await asyncio.sleep(.25)  # Wait
                elif Gait == 3:
                    Gait = 4
                    print("Setting gait 4...")
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["SPORT_MOD"], 
                        {
                            "api_id": 1011,
                            "parameter": {"data": 4}
                        }
                    )
                    await asyncio.sleep(.25)  # Wait
                elif Gait == 4:
                    Gait = 1
                    print("Setting gait 1...")
                    await conn.datachannel.pub_sub.publish_request_new(
                        RTC_TOPIC["SPORT_MOD"], 
                        {
                            "api_id": 1011,
                            "parameter": {"data": 1}
                        }
                    )
                    await asyncio.sleep(.25)  # Wait


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully.
        print("\nProgram interrupted by user")
        pygame.quit()
