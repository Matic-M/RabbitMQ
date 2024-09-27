import pika
import pika.credentials

# program sends single message to the queue

def main():
    # establish connection with rabbitmq server
    credentials = pika.PlainCredentials(username='admin', password='admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # creating queue
    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body='hello world!')
    print(" [x] Sent 'Hello World!'")

    connection.close()

if __name__ == '__main__':
    main()