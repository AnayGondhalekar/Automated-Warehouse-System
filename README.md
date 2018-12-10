# Automated-Warehouse-System

## Repository for the super project -'Automated Warehouse System using AWS and Robotic Arm' for the course EID (ECEN 5053-002)

### Names of Developers and Students-

This project is a result of the efforts of-
#### Anay Gondhalekar - MQTT, Client Side Code, Configuring Robotic Arm,Lambda Function, HTML page, Extra credit
#### Nikhil Divekar - UI on Client Side, Precise Pick-n-Place of Robotic Arm, Image Processing(AWS), SQS, Extra credit
#### Shubham Jaiswal - Robotic Arm Assembly,Lambda Function, UI on Client Side, Server Code, Websockets, Extra credit

#### Project Information-
In this project an automated warehouse system is developed. It uses 2 Raspberry Pi, one on client and server side each. the client side opens a QT UI when executed. It calls a thread for communication to an HTML page through websockets, and a thread to start consume for the RabbitMQ. When it gets a order from the QT, it sends the placed order of the objects over MQTT to AWS Broker which is accessed by the Lambda function. The Lambda function further sends the placed order with a time stamp to a SQS queue.The queue is subscribed to from the server side and when it gets a object value or name, it captures an image from the camera and sends it over cloud to AWS Rekognition Service. The AWS service gives the location of the found objects in the warehouse and matches it to the object received from the queue. When the object is found, it gives the arm a command to pick up the received objects based on its coordinates received. Thereby user receives its order.

#### Project Minimum Requirement-
1. Protocols Used: MQTT, Websockets, USB, RabbitMQ (Extra Credit)
2. Python & Node.js elements
3. Qt & HTMl UIs
4. AWS Frameworks: AWS Rekognition, AWS IOT Core, Lambda Function, SQS Queue
5. Sensors and Actuators: Camera, Robotic Arm
6. 2 Raspberry Pis
7. Message Queues: MQTT, AWS SQS(FIFO), RabbitMQ
8. 6 weeks of development per team member

#### Installation Instructions-

#### Prerequisites(Make sure these are installed in your RPI):
1. Robotic Arm: Pyusb library
2. QT: Python qt5 libraries
3. Websocket: Tornado
4. AWS: AWS account, services and keys
5. RabbitMQ: AWS CLI, rabbitmq_server

#### Steps & Installation:
1. Download and clone this repository.
2. Run the server side file, robot_side.py, using sudo python3 robot_side.py
3. Run the client side file, robot2.py, using sudo python3 robot3.py
4. Open Login.html, enter the credentials to Login and go to the main html page
5. Connect the Websocket with suitable IP.
6. Place your order as per the requirements on the QT UI

#### Project Extra Credits-
1. RabbitMQ for image transfer
2. Image Processing(Character recognition) using AWS Rekogniton
3. Login screen in HTML
4. Fetching more than 1 value from Database on a button click
5. Position tracking of objects in warehouse
6. Improved Secuity in Warehouse by displaying before and after images on client side 
7. Improved effeciency by discarding unmatching requests those are not servicing
8. Displaying the current warehouse image on HTML page and QT
9. Storing images in an S3 Bucket
10. Drop down button in QT and non editable Cart for not accepting Invalid Requests

#### References-
1. https://www.wikihow.com/Use-a-USB-Robotic-Arm-with-a-Raspberry-Pi-(Maplin)
2. https://aws.amazon.com/rekognition/
3. https://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto
4. https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html


