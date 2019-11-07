from .rabbitMqBroker import RabbitMqBroker


class MessageBrokerFactory():

    def __init__(self):
        pass

    def get_broker(self, broker):
        if broker == 'rabbitmq':
            broker = RabbitMqBroker()
            return broker
        elif broker == 'Kafka':
            return None
        else:
            return None
