# TT_Engineering_Project
Engineering Project
The purpose of this project is to code a robot to move towards a person in need of medical supplies that is unable to get to it themselves, assuming there is no one else in the room to help. This robot is most appropriately used in a lab setting with flat flooring. 

The robot will tend to three main common lab injuriesL: burns, cuts, and eye contaminations. There will be separate compartments in the robot to house medical supplies appropriate for each injury. When in need of the robot's help, a user will use the wake word "help me", which the robot will detect with four microphones. Upon hearing the wake word, the robot will use its camera to identify a human in the room and move towards the user. When the robot is close enough to the user, it will stop and a light will turn on to indicate to the user that the robot is now listening for another audio cue: the type of injury. If the user specifies burns, the burn compartment will open with the appropriate medical supplies.

Additionally, a web app will be used for the user to manually move the robot with a control pad, open and close compartents, and view error messages.

For audio recognition, we will be importing the following: pvporcupine, pyaudio, struct, and os

For camera human detectoin, we will be importing the following: 
