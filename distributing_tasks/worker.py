import time
import pika
import os
import sys


# paralellisation of work, we can use more workers
# 1 task + 2 workers
# each worker gets the same number of messages - round robin
# added FEATURE for ack after worker finishes, in case it dies message is handed to other worker
# NEW FEATURE: in case node crashes, queue is not lost -> durable

def main():
     # establish connextion with rabbitmq server
    credentials = pika.PlainCredentials(username='admin', password='admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hello_durable', durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # added fair dispatch so dispatcher gives one message to worker at the time
    channel.basic_consume(queue='hello_durable', on_message_callback=callback) # remove auto_ack=True arg

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)