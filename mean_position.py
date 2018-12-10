#import the USB and Time librarys into Python
import usb.core, usb.util, time
 
#Allocate the name 'RoboArm' to the USB device
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x001)
 
#Check if the arm is detected and warn if not
if RoboArm is None:
    raise ValueError("Arm not found")
 
#Create a variable for duration
Duration=1
 
#Define a procedure to execute each movement
def MoveArm(Duration, ArmCmd):
    #Start the movement
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
    #Stop the movement after waiting a specified duration
    time.sleep(Duration)
    ArmCmd=[0,0,0]
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
    


#MoveArm(1,[0,0,1]) #Light on
#MoveArm(1,[0,0,0]) #Light off
MoveArm(0.05,[0,1,0]) #Rotate base right
#MoveArm(0.05,[0,2,0]) #Rotate base left
#MoveArm(0.1,[64,0,0]) #Shoulder up
#MoveArm(0.1,[128,0,0]) #Shoulder down
#MoveArm(2.8,[16,0,0]) #Elbow up
#MoveArm(0.5,[32,0,0]) #Elbow down
#MoveArm(1,[2,0,0]) #Grip open
#MoveArm(1,[1,0,0]) #Grip close
#MoveArm(1,[4,0,0]) #Wrist up
#MoveArm(1,[8,0,0]) # Wrist down
 
