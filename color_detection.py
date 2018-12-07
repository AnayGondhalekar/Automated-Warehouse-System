import boto3

import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    #time.sleep(0.2)
    camera.capture('demo1.jpg')

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
#print(response)
#print('Matching faces')
for text in textDetections:
    print('Detected text:' + text['DetectedText'])
    print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
    print('Geometry: ' + str(text['Geometry']['BoundingBox']))
    
##    box = text['BoundingBox']
##    left = imgWidth * box['Left']
##    top = imgHeight * box['Top']
##    width = imgWidth * box['Width']
##    height = imgHeight * box['Height']
##                
##
##    print('Left: ' + '{0:.0f}'.format(left))
##    print('Top: ' + '{0:.0f}'.format(top))
##    print('Face Width: ' + "{0:.0f}".format(width))
##    print('Face Height: ' + "{0:.0f}".format(height))
    #print('Geometry: ' +"{:.2f}".format(text['Geometry']))


##if __name__ == "__main__":
##
##    bucket='nikhilimagesbucket'
##    photo='bday.jpg'
##
##    client=boto3.client('rekognition')
##  
##    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
##
##                        
##    textDetections=response['TextDetections']
##    #print(response)
##    #print('Matching faces')
##    for text in textDetections:
##            print('Detected text:' + text['DetectedText'])
##            print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")





##            print('Id: {}'.format(text['Id']))
##            if 'ParentId' in text:
##                print('Parent Id: {}'.format(text['ParentId']))
##            print('Type:' + text['Type'])