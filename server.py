import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sqlite3
import asyncio
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("new connection")
      
    #When message is received
    def on_message(self, message):
        print("message received:" + message)
        # Reverse Message and send it back
        connection = sqlite3.connect("user.db")
        curs = connection.cursor()
        
        if (message ==  "temp_min_val"):
            curs.execute("SELECT * FROM DATA WHERE TEMP_VALUE =(SELECT MIN(TEMP_VALUE) FROM DATA)")
            for reading in curs.fetchall():
                print(str(reading[0]) + " " + str(reading[1]) + " " + str(reading[2]))
            self.write_message(str(reading[0])[:5])
            
        elif(message == "temp_val"):
            curs.execute("SELECT * FROM DATA ORDER BY TIME_DATE_VALUE DESC LIMIT 1 ")
            for reading in curs.fetchall():
                print(str(reading[0]) + " " + str(reading[1]) + " " + str(reading[2]))
            self.write_message(str(reading[0])[:5])
            
        elif(message == "temp_max_val"):
            curs.execute("SELECT * FROM DATA WHERE TEMP_VALUE =(SELECT MAX(TEMP_VALUE) FROM DATA)")
            for reading in curs.fetchall():
                print(str(reading[0]) + " " + str(reading[1]) + " " + str(reading[2]))
            self.write_message(str(reading[0])[:5])
        
        elif(message == "temp_avg_val"):
            curs.execute("SELECT AVG(TEMP_VALUE) FROM DATA")
            for reading in curs.fetchall():
                print(str(reading[0]))
            self.write_message(str(reading[0])[:5])
         
        elif(message == "hum_val"):
            curs.execute("SELECT * FROM DATA ORDER BY TIME_DATE_VALUE DESC LIMIT 1 ")
            for reading in curs.fetchall():
                print(str(reading[0]) + " " + str(reading[1]) + " " + str(reading[2]))
            self.write_message(str(reading[1])[:5])
            
        elif(message == "hum_max_val"):
            curs.execute("SELECT * FROM DATA WHERE HUM_VALUE =(SELECT MAX(HUM_VALUE) FROM DATA)")
            for reading in curs.fetchall():
                print(str(reading[0]) + " " + str(reading[1]) + " " + str(reading[2]))
            self.write_message(str(reading[1])[:5])
        
        elif(message == "hum_avg_val"):
            curs.execute("SELECT AVG(HUM_VALUE) FROM DATA")
            for reading in curs.fetchall():
                print(str(reading[0]))
            self.write_message(str(reading[0])[:5]) 
        
        elif(message == "hum_min_val"):
            curs.execute("SELECT * FROM DATA WHERE HUM_VALUE =(SELECT MIN(HUM_VALUE) FROM DATA) ")
            for reading in curs.fetchall():
                print(str(reading[0]) + " " + str(reading[1]) + " " + str(reading[2]))
            self.write_message(str(reading[1])[:5])
       
        else:
            print(message)
            curs.execute("SELECT DISTINCT TEMP_VALUE FROM DATA WHERE TIME_DATE_VALUE = ?", [message])
            for reading in curs.fetchall():
                print(str(reading[0]))
            self.write_message(str(reading[0])[:5])
    def on_close(self):
        print("connection closed")
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print("*** Websocket Server Started ***")
    tornado.ioloop.IOLoop.instance().start()
 
