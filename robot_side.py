import boto3

import time
import picamera
import pika
import logging

import usb.core, usb.util, time
 
#Allocate the name 'RoboArm' to the USB device
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x001)
 
#Check if the arm is detected and warn if not
if RoboArm is None:
    raise ValueError("Arm not found")
 
#Create a variable for duration
Duration=1
result = []
 
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
    end_flag = 0
    flag = 0
    b = None
# Process messages by printing out body
    for message in queue.receive_messages():
        a = '{0}'.format(message.body)
        b= str(a.split('"')[3])
        print(b)
        result = [x.strip() for x in b.split(',')]
        print(result)
        message.delete()
        flag = 1
    if(len(result) != 0):
        for val in result:
            if(b is not None):
                with picamera.PiCamera() as camera:
                    camera.resolution = (1024, 768)
                    camera.start_preview()
                    # Camera warm-up time
                    #time.sleep(0.2)
                    camera.capture('demo1.jpg')
                    
                f= open("demo1.jpg","rb")
                i= f.read()

                logging.basicConfig()
                credentials = pika.PlainCredentials('the_user','the_pass')
                connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.0.180',5672,'/',socket_timeout=15,credentials= credentials))
                channel = connection.channel()


                channel.queue_declare(queue='hello')

                channel.basic_publish(exchange='',
                                      routing_key='hello',
                                      body=i)
                print(" [x] Sent 'Hello World! 1'")
                connection.close()
                    
                position_top = []
                position_left = []
                compound = []
                final = []

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
                detected_flag = 0
                #print(response)
                #print('Matching faces')
                for text in textDetections:
                    print('Detected text:' + text['DetectedText'])
                    print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
                    print('Geometry: ' + str(text['Geometry']['BoundingBox']))
                    print('Id: {}'.format(text['Id']))
                    
                    if(str(text['DetectedText']) is val):
                           print( val + " received")
                           print("position of" + val + "is" + " " + str(text['Geometry']['BoundingBox']['Top']) + " " +str(text['Geometry']['BoundingBox']['Left']))
                           position_top.append(float(str(text['Geometry']['BoundingBox']['Top'])))
                           #print(position_top[i])
                           position_left.append(float(str(text['Geometry']['BoundingBox']['Left'])))
                           #print(position_left[i])
                           detected_flag = 1
                           end_flag = 1
                           #compound.append(x)
                    i = i+1
                
        ##        print("Final array :" + str(compound))
        ##        print(position_top[0])
        ##        print(position_top[1])
        ##        print(position_left[0])
        ##        print(position_left[1])
        ##        final = compound[len(compound)//2:]
                j = 0
                #for y in final:
                if(detected_flag == 1):
                    if(0.22 < position_top[0]):
                        if(position_top[0] < 0.30):    
                            if(0.32 < position_left[0]):
                                if(position_left[0] < 0.39):
                                    MoveArm(1.55,[0,1,0]) #Rotate base right
                                    time.sleep(1)
                                    MoveArm(2.30,[128,0,0]) #Shoulder down
                                    time.sleep(1)
                                    MoveArm(1.1,[1,0,0]) #Grip close
                                    time.sleep(1)
                                    MoveArm(3.7,[64,0,0]) #Shoulder up
                                    time.sleep(1)
                                    MoveArm(1.55,[0,2,0]) #Rotate base left
                                    time.sleep(1)
                                    MoveArm(1,[2,0,0]) #Grip open
                                    time.sleep(1)
                    else:
                        print("Not at proper state")
                        
                    if(0.37 < position_top[0]):
                        if(position_top[0] < 0.44):    
                            if(0.50 < position_left[0]):
                                if(position_left[0] < 0.56):
                                    print("Move to 2")
                                    MoveArm(2.8,[0,1,0]) #Rotate base right
                                    time.sleep(1)
                                    MoveArm(2.30,[128,0,0]) #Shoulder down
                                    time.sleep(1)
                                    MoveArm(1.1,[1,0,0]) #Grip close
                                    time.sleep(1)
                                    MoveArm(3.7,[64,0,0]) #Shoulder up
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
                                    MoveArm(3.7,[64,0,0]) #Shoulder up
                                    time.sleep(1)
                                    MoveArm(4,[0,2,0]) #Rotate base left
                                    time.sleep(1)
                                    MoveArm(1,[2,0,0]) #Grip open
                                    time.sleep(1)
                    else:
                        print("Not at proper state")
                        
                    j = j + 1
                    
                    del position_left[:]
                    del position_top[:]
     
    if(end_flag == 1):
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # Camera warm-up time
            #time.sleep(0.2)
            camera.capture('demo1.jpg')
            
        f= open("demo1.jpg","rb")
        i= f.read()

        logging.basicConfig()
        credentials = pika.PlainCredentials('the_user','the_pass')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.0.180',5672,'/',socket_timeout=15,credentials= credentials))
        channel = connection.channel()


        channel.queue_declare(queue='hello')

        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=i)
        print(" [x] Sent 'Hello World 2!'")
        connection.close()
        print("At end")
        end_flag = 0
