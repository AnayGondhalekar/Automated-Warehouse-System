#!/usr/bin/env python
import pika
import logging

f= open("image.jpeg","rb")
i= f.read()

logging.basicConfig()
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.198'))
channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=i)
print(" [x] Sent 'Hello World!'")
connection.close()