# Go2-WebRTC-Joystick-Control
Control your Unitree Go2 with a Gamepad using Legion1581's Go2_WebRTC_Connect Driver

## This is a work in progress and is not ready for actual use yet  
#### I welcome pull requests, please help improve the script

```
Requires https://github.com/legion1581/go2_webrtc_connect

Before first run, modify values in config_file.py to suit your application.

Joystick values can be retrieved by running the joystick_test.py script

Run "python dog.py" to receive video from the dog AND to control it via joystick(uses video.py example by legion1581 to display video while using joystick).

If you ONLY need joystick control of the dog, run "python joy.py", and no video will be displayed.

If you want to get an idea on how the official unitree remote works take a look at wireless_remote.py
It is also unfinished and very basic for now

Upon Successful Connection of controller the Dog switches to Sport Mode, and if the Greet flag is set in config file the dog then performs the Hello(Greet) Command.

Controller Assumes X-Box Style Button Layout(Tested using xbox controller connected via usb)
Nintendo style layout will swap a/b and x/y

Left Analog Sticks control Movement Front/Back and Strafe Left/Right
Right Analog Sticks control Pivot/Heading/Turn

Controls
Damping: Select
Recovery Stand: D-Pad Up
Toggle StandDown(Crouch): D-Pad Down
Toggle Obstacle Avoidance: D-Pad Left
Toggle Headlight Brightness: D-Pad Right
Toggle Pose Mode: Left Trigger
Toggle Continuous Gait: Right Bumper + Right Trigger
Toggle Gaits(Walk, Run, Stair Climb, Down Stairs): Right Trigger

Sport Mode Only Controls
Sit Toggle: A Button
FingerHeart: B Button
WiggleHips: X Button
Hello(Greet): Y Button

AI Mode Only Controls
Toggle AI Mode/Sport Mode: Left Bumper + Start
Toggle WalkUpright: Left Bumper + D-Pad Up
Toggle StandOut(HandStand): Left Bumper + D-Pad Down
```
