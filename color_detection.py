import boto3

import time
import picamera

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
    
# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='MsgQueue.fifo')

while True:
    flag = 0
    b = None
# Process messages by printing out body
    for message in queue.receive_messages():
        a = '{0}'.format(message.body)
        b= str(a.split('"')[3])
        print(b)
        message.delete()
        flag = 1

    if(b is not None):
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # Camera warm-up time
            #time.sleep(0.2)
            camera.capture('demo1.jpg')
            
        position_top = []
        position_left = []

        bucketName = "nikhilimagesbucket"
        Key = "demo1.jpg"
        outPutname = "demo1.jpg"

        s3 = boto3.client('s3')
        s3.upload_file(Key, bucketName, outPutname)

        bucket='nikhilimagesbucket'
        photo='demo1.jpg'

        client=boto3.client('rekognition')
          
        response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                                
        textDetections=response['TextDetections']
        i = 0
        print("Here")
        #print(response)
        #print('Matching faces')
        for text in textDetections:
            print('Detected text:' + text['DetectedText'])
            print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print('Geometry: ' + str(text['Geometry']['BoundingBox']))
            print('Id: {}'.format(text['Id']))
            
            if(str(text['DetectedText']) is b):
                   print( b + " received")
                   print("position of" + b + "is" + " " + str(text['Geometry']['BoundingBox']['Top']) + " " +str(text['Geometry']['BoundingBox']['Left']))
                   position_top.append(float(str(text['Geometry']['BoundingBox']['Top'])))
                   print(position_top[0])
                   position_left.append(float(str(text['Geometry']['BoundingBox']['Left'])))
                   print(position_left[0])
            i = i+1
            
        if(0.23 < position_top[0]):
            if(position_top[0] < 0.27):    
                if(0.35 < position_left[0]):
                    if(position_left[0] < 0.39):
                        MoveArm(1.55,[0,1,0]) #Rotate base right
                        time.sleep(1)
                        MoveArm(2.30,[128,0,0]) #Shoulder down
                        time.sleep(1)
                        MoveArm(1.1,[1,0,0]) #Grip close
                        time.sleep(1)
                        MoveArm(3.5,[64,0,0]) #Shoulder up
                        time.sleep(1)
                        MoveArm(1.52,[0,2,0]) #Rotate base left
                        time.sleep(1)
                        MoveArm(1,[2,0,0]) #Grip open
                        time.sleep(1)
        else:
            print("Not at proper state")
            
        if(0.39 < position_top[0]):
            if(position_top[0] < 0.44):    
                if(0.52 < position_left[0]):
                    if(position_left[0] < 0.56):
                        print("Move to 2")
                        MoveArm(2.8,[0,1,0]) #Rotate base right
                        time.sleep(1)
                        MoveArm(2.30,[128,0,0]) #Shoulder down
                        time.sleep(1)
                        MoveArm(1.1,[1,0,0]) #Grip close
                        time.sleep(1)
                        MoveArm(3.5,[64,0,0]) #Shoulder up
                        time.sleep(1)
                        MoveArm(2.8,[0,2,0]) #Rotate base left
                        time.sleep(1)
                        MoveArm(1,[2,0,0]) #Grip open
                        time.sleep(1)
        else:
            print("Not at proper state")
            
        if(0.64 < position_top[0]):
            if(position_top[0] < 0.70):    
                if(0.64 < position_left[0]):
                    if(position_left[0] < 0.70):
                        print("Move to 3")
                        MoveArm(4,[0,1,0]) #Rotate base right
                        time.sleep(1)
                        MoveArm(2.30,[128,0,0]) #Shoulder down
                        time.sleep(1)
                        MoveArm(1.1,[1,0,0]) #Grip close
                        time.sleep(1)
                        MoveArm(3.5,[64,0,0]) #Shoulder up
                        time.sleep(1)
                        MoveArm(3.95,[0,2,0]) #Rotate base left
                        time.sleep(1)
                        MoveArm(1,[2,0,0]) #Grip open
                        time.sleep(1)
        else:
            print("Not at proper state")
                
            
        del position_left[:]
        del position_top[:]
