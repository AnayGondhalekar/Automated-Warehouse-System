#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('the_user','the_pass')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.0.180',5672,'/',credentials))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    f=open("myimage.jpg","wb")
    if(f is not None):
        f.write(body)
        f.close()

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()