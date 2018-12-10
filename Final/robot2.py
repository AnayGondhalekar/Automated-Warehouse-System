# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robot.ui'
#
# Created by: PyQt5 UI code generator 5.7

import AWSIoTPythonSDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime
from PIL import Image
import paho.mqtt.client as mqtt
import threading
import numpy as np
import time
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sqlite3
import asyncio
import ssl
import os
import json
import pika

valueArray = []
new_val = None
items = None 

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(441, 449)
        MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 50, 101, 21))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(180, 50, 151, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Select item")
        self.comboBox.addItem("A")
        self.comboBox.addItem("B")
        self.comboBox.addItem("C")
        self.comboBox.activated[str].connect(self.selectionFunc)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 120, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_val)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 120, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.send_val)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 180, 241, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 220, 221, 33))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 310, 101, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.get_image)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 280, 191, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 441, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Object Name:"))
        self.pushButton.setText(_translate("MainWindow", "Add"))
        self.pushButton_2.setText(_translate("MainWindow", "Done"))
        self.label_3.setText(_translate("MainWindow", "You have following items in cart:"))
        self.pushButton_3.setText(_translate("MainWindow", "Get image"))
        self.label_2.setText(_translate("MainWindow", "Current warehouse image:"))
     
    def selectionFunc(self, text):
        self.new_val = text
        print(self.new_val)
    
    def add_val(self, Mainwindow):
        new_choice = None
        _translate = QtCore.QCoreApplication.translate
        print("Add-val")
        if(self.new_val is not None):
            valueArray.append(self.new_val)
            print(valueArray)
        self.lineEdit_2.setText(_translate("MainWindow", ', '.join(valueArray)))
        time_date_value = QtCore.QDateTime.currentDateTime().toString()
        
        connection = sqlite3.connect("user.db")
        connection.execute("INSERT INTO DATA VALUES(?,?)",(self.new_val, time_date_value))
        connection.commit()
        #connection.close()
        
        curs = connection.cursor()
        curs.execute("SELECT ITEM FROM DATA")
        for reading in curs.fetchall():
            print(str(reading[0]))
        connection.close()
##        pydict = {'Object': self.new_val}
##        jsondict = json.dumps(pydict)
##        self.myAWSIoTMQTTClient.publish('robotarm', jsondict, 1)
        
    def send_val(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        print("Done")
        message_queue = str(self.lineEdit_2.text())
        self.lineEdit_2.setText(_translate("MainWindow", ""))
        del valueArray[:]
##        client = mqtt.Client("RobotArm")
##        client.connect("iot.eclipse.org")
##        client.publish("Robot/test",self.message_queue)
##        client.disconnect()
        pydict = {'Objects': message_queue}
        jsondict = json.dumps(pydict)
        self.myAWSIoTMQTTClient.publish('myrobot', jsondict, 1)
        
    def get_image(self):
        image = Image.open("myimage.jpeg")
        image.show() 
        
    def mqttSetup(self):
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient("clientId")
        self.myAWSIoTMQTTClient.configureEndpoint("a1hfsu5g939d5k-ats.iot.us-east-2.amazonaws.com", 8883)
        self.myAWSIoTMQTTClient.configureCredentials("/home/pi/Desktop/SuperProject_Anay/Certs2/root-CA.crt","/home/pi/Desktop/SuperProject_Anay/Certs2/f143328a3c-private.pem.key", "/home/pi/Desktop/SuperProject_Anay/Certs2/f143328a3c-certificate.pem.crt")
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        self.myAWSIoTMQTTClient.connect()
        print ("MQTT Conn Success")
        self.myAWSIoTMQTTClient.subscribe('myrobot', 1, None)    
    
    
        
class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print("new connection")
     
    #When message is received
    def on_message(self, message):
        print("message received:" + message)
        if(message == "latest_item"):
            connection = sqlite3.connect("user.db")
            curs = connection.cursor()
            curs.execute("SELECT ITEM FROM DATA ORDER BY TIME_DATE_VALUE DESC LIMIT 1")
            for reading in curs.fetchall():
                print(str(reading[0]) )
            self.write_message(str(reading[0]))
            
        if(message == "value1"):
            connection = sqlite3.connect("user.db")
            curs = connection.cursor()
            curs.execute("SELECT ITEM FROM DATA ORDER BY TIME_DATE_VALUE DESC LIMIT 1")
            for reading in curs.fetchall():
                print(str(reading[0]) )
            self.write_message(str(reading[0]))
            
        if(message == "value2"):
            connection = sqlite3.connect("user.db")
            curs = connection.cursor()
            curs.execute("SELECT TIME_DATE_VALUE FROM DATA ORDER BY TIME_DATE_VALUE DESC LIMIT 1")
            for reading in curs.fetchall():
                print(str(reading[0]) )
            self.write_message(str(reading[0]))
       

        
    def on_close(self):
        print("connection closed")
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])

    
def thread1():
    asyncio.set_event_loop(asyncio.new_event_loop())
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print("*** Websocket Server Started ***")
    while(1):
        print("In thread 1")
        tornado.ioloop.IOLoop.instance().start()
        
def thread2():
    credentials = pika.PlainCredentials('the_user','the_pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.0.180',5672,'/',credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        #print(" [x] Received %r" % body)
        print("Receiving image")
        f=open("myimage.jpeg","wb")
        if(f is not None):
            f.write(body)
            f.close()
        image = Image.open("myimage.jpeg")
        image.show()

    channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
    
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.mqttSetup()
    MainWindow.show()
##    connection = sqlite3.connect("user.db")
##    connection.execute("CREATE TABLE DATA(ITEM TEXT, TIME_DATE_VALUE TEXT NOT NULL)")
    mythread = threading.Thread(name="thread1", target=thread1)
    mythread.daemon = True
    mythread.start()
    mythread2 = threading.Thread(name="thread2", target=thread2)
    mythread2.daemon = True
    mythread2.start()
    sys.exit(app.exec_())

