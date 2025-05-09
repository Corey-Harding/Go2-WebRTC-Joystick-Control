#Joystick Config

JOYSTICK_NUMBER = 0 # Device number for joystick
#Below numbers represent the button/axis number as seen by pygame
LEFT_X_AXIS = 0
LEFT_Y_AXIS = 1
RIGHT_X_AXIS = 3
RIGHT_Y_AXIS = 4
LEFT_TRIGGER_AXIS = 2
RIGHT_TRIGGER_AXIS = 5
LEFT_BUMPER = 4
RIGHT_BUMPER = 5
LT_NEUTRAL = 0 # Greater than this value = Left Trigger Pulled
RT_NEUTRAL = 0 # Greater than this value = Right Trigger Pulled
D_PAD_UP = (0, 1)
D_PAD_DOWN = (0, -1)
D_PAD_LEFT = (-1, 0)
D_PAD_RIGHT = (1, 0)
SELECT = 6
START = 7
A_BUTTON = 0
B_BUTTON = 1
X_BUTTON = 2
Y_BUTTON = 3
#Analog Stick Sensitivity
DEADZONE = 0.1
Lxsensitivity = 1
Lysensitivity = 1
Rxsensitivity = 1
Rysensitivity = 1
ObstacleAvoidMultiplier = 1.25 # Increase movement speed in obstacle avoidance mode


#Connection Config
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod

# Choose a connection method (uncomment the correct one)
# WEBRTC_CONNECTION_TYPE = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.12.1")
# WEBRTC_CONNECTION_TYPE = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, serialNumber="B42D2000XXXXXXXX")
# WEBRTC_CONNECTION_TYPE = Go2WebRTCConnection(WebRTCConnectionMethod.Remote, serialNumber="B42D2000XXXXXXXX", username="email@gmail.com", password="pass")
WEBRTC_CONNECTION_TYPE = Go2WebRTCConnection(WebRTCConnectionMethod.LocalAP)