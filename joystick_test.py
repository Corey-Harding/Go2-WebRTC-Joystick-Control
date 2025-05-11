# Joystick test by Corey Harding
# Test your joystick in pygame to make configuraiton via config_file.py easier

import asyncio
import pygame
from time import time
from config_file import *

async def main():

    try:
        pygame.init()
        clock = pygame.time.Clock()
        if pygame.joystick.get_count() == 0:
            print("No joystick detected...")
            return
        joystick = pygame.joystick.Joystick(JOYSTICK_NUMBER)
        joystick.init()
        print("Joystick Initialized...")
        
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
                print(f"BUTTON ({event.button}) PRESSED")
                if event.button == START:
                    print("START")
                if event.button == SELECT:
                    print("SELECT")
                if event.button == A_BUTTON:
                    print("A_BUTTON")
                if event.button == B_BUTTON:
                    print("B_BUTTON")
                if event.button == X_BUTTON:
                    print("X_BUTTON")
                if event.button == Y_BUTTON:
                    print("Y_BUTTON")
                if event.button == LEFT_BUMPER:
                    print("LEFT_BUMPER")
                if event.button == RIGHT_BUMPER:
                    print("RIGHT_BUMPER")
                if event.button == F1:
                    print("F1")
                if event.button == F3:
                    print("F3")

            #Test Joystick Button Release Events
            elif event.type == pygame.JOYBUTTONUP:
                print(f"BUTTON ({event.button}) RELEASED")
                if event.button == START:
                    print("START")
                if event.button == SELECT:
                    print("SELECT")
                if event.button == A_BUTTON:
                    print("A_BUTTON")
                if event.button == B_BUTTON:
                    print("B_BUTTON")
                if event.button == X_BUTTON:
                    print("X_BUTTON")
                if event.button == Y_BUTTON:
                    print("Y_BUTTON")
                if event.button == LEFT_BUMPER:
                    print("LEFT_BUMPER")
                if event.button == RIGHT_BUMPER:
                    print("RIGHT_BUMPER")
                if event.button == F1:
                    print("F1")
                if event.button == F3:
                    print("F3")

            #Test Joystick Hats
            elif event.type == pygame.JOYHATMOTION:
                print(f"HAT NUMBER: {str(event.hat)} HAT POSITION: {str(event.value)}")
                if event.value == (0, 0):
                    print("D_PAD_NEUTRAL")
                if event.value == D_PAD_UP:
                   print("D_PAD_UP")
                if event.value == D_PAD_DOWN:
                   print("D_PAD_DOWN")
                if event.value == D_PAD_LEFT:
                   print("D_PAD_LEFT")
                if event.value == D_PAD_RIGHT:
                   print("D_PAD_RIGHT")

            #Test Joystick Axis
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == LEFT_TRIGGER_AXIS or event.axis == RIGHT_TRIGGER_AXIS:
                    print(f"AXIS: ({str(event.axis)}) POSITION: ({str(event.value)})")
                    if event.axis == LEFT_TRIGGER_AXIS and event.value > LT_NEUTRAL:
                        print(f"LEFT_TRIGGER_AXIS Postion: ({str(event.value)})")
                    if event.axis == RIGHT_TRIGGER_AXIS and event.value > LT_NEUTRAL:
                        print(f"RIGHT_TRIGGER_AXIS Postion: ({str(event.value)})")
                elif event.value > DEADZONE or event.value < -DEADZONE:
                    print(f"AXIS: ({str(event.axis)}) POSITION: ({str(event.value)})")
                    if event.axis == LEFT_X_AXIS:
                        print(f"LEFT_X_AXIS Postion: ({str(event.value)})")
                    if event.axis == LEFT_Y_AXIS:
                        print(f"LEFT_Y_AXIS Postion: ({str(event.value)})")
                    if event.axis == RIGHT_X_AXIS:
                        print(f"RIGHT_X_AXIS Postion: ({str(event.value)})")
                    if event.axis == RIGHT_Y_AXIS:
                        print(f"RIGHT_Y_AXIS Postion: ({str(event.value)})")

#            Joyball Not Tested
#            elif event.type == pygame.JOYBALLMOTION:
#                print(f"JOYBALL POSITION: ({str(event.value)})")

        clock.tick(CONTROLLER_FPS_LIMIT) # Limit how many times a second the script is able to run
        


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully.
        print("\nProgram interrupted by user")
        pygame.quit()
