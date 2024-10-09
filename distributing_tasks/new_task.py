import sys
import pika


def main():
    # establish connextion with rabbitmq server
    credentials = pika.PlainCredentials(username='admin', password='admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # creating queue
    channel.queue_declare(queue='hello')

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    
    print(f" [x] Sent {message}")

    connection.close()

if __name__=='__main__':
    main()