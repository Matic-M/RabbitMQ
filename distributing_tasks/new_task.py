import sys
import pika

# NEW FEATURE: in case node crashes, queue and messages are not lost

def main():
    # establish connextion with rabbitmq server
    credentials = pika.PlainCredentials(username='admin', password='admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # creating queue
    channel.queue_declare(queue='hello_durable', durable=True) # added durability for queue

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='', routing_key='hello_durable', body=message, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)) # message are saved to cache or disc (not 100% certain, there is short window for lose)
    
    print(f" [x] Sent {message}")

    connection.close()

if __name__=='__main__':
    main()