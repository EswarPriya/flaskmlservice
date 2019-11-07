import config
import pika

from .abstractBroker import AbstractBroker


class RabbitMqBroker(AbstractBroker):
    channel = None

    def __init__(self):
        pass

    def build_broker(self, host, port, userName, password):
        rabbitVhost = config.RABBITMQ_VHOST
        credentials = pika.PlainCredentials(userName, password)
        parameters = pika.ConnectionParameters(host,
                                               port,
                                               rabbitVhost,
                                               credentials)

        connection = pika.BlockingConnection(parameters)
        return connection

    def open_connection(self, connection):
        self.channel = connection.channel()

    def close_connection(self):
        if self.channel == None:
            raise Exception('please open connection')
        self.channel.close()

    def declare_exchange(self, exchangeName, exchangeType, durable=True):
        '''exchange types
            fanout
            direct
            topic
        '''
        if self.channel == None:
            raise Exception('please open connection')
        self.channel.exchange_declare(exchange=exchangeName, exchange_type=exchangeType, durable=durable)

    def declare_queue(self, queueName, durable=True):
        '''
        durable is to make sure that RabbitMQ will never lose our queue
        '''
        if self.channel == None:
            raise Exception('please open connection')
        self.channel.queue_declare(queue=queueName, durable=durable)

    def publish(self, exchange, route, message, deliveryMode=2):
        if self.channel == None:
            raise Exception('please open connection')
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=route,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=deliveryMode)
                                   )

    def subscribe(self, exchange, queueName, callback):
        '''prefetch count lets to  keep the message survive even if rabbitmq is restarted'''
        if self.channel == None:
            raise Exception('please open connection')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_bind(exchange=exchange, queue=queueName)
        self.channel.basic_consume(queue=queueName, on_message_callback=callback)
        self.channel.start_consuming()

    def queue_bind(self, queue, exchange, routing_key=None):
        self.channel.queue_bind(queue, exchange, routing_key)

    # def callback(self, connection, method, properties, body):
    #     '''
    #     TODO: override this method 
    #     but use the below code 
    #     connection.basic_ack(delivery_tag=method.delivery_tag)    
    # '''
