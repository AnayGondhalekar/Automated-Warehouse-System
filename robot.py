# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robot.ui'
#
# Created by: PyQt5 UI code generator 5.7

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime
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

valueArray = []
new_val = None
items = None 

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
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
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 110, 67, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(180, 100, 113, 33))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 180, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_val)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 180, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.send_val)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 240, 241, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 270, 221, 33))
        self.lineEdit_2.setObjectName("lineEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
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
        self.label_2.setText(_translate("MainWindow", "Quantity:"))
        self.pushButton.setText(_translate("MainWindow", "Add"))
        self.pushButton_2.setText(_translate("MainWindow", "Done"))
        self.label_3.setText(_translate("MainWindow", "You have following items in cart:"))
        
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
        
    def send_val(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        print("Done")
        self.lineEdit_2.setText(_translate("MainWindow", ""))
        
        
class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print("new connection")
     
    #When message is received
    def on_message(self, message):
        print("message received:" + message)
        connection = sqlite3.connect("user.db")
        curs = connection.cursor()
        curs.execute("SELECT ITEM FROM DATA ORDER BY TIME_DATE_VALUE DESC LIMIT 1")
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
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #connection = sqlite3.connect("user.db")
    #connection.execute("CREATE TABLE DATA(ITEM TEXT, TIME_DATE_VALUE TEXT NOT NULL)")
    
    mythread = threading.Thread(name="thread1", target=thread1)
    mythread.daemon = True
    mythread.start()
    sys.exit(app.exec_())

