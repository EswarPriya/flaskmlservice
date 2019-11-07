from abc import ABC, abstractmethod


class AbstractBroker(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def build_broker(self, host, port, userName, password):
        pass

    @abstractmethod
    def open_connection(self, connection):
        pass

    @abstractmethod
    def close_connection(self, connection):
        pass

    @abstractmethod
    def declare_exchange(self, connection, exchangeName, exchangeType):
        pass

    @abstractmethod
    def declare_queue(self, connection, queueName, durable=True):
        pass

    @abstractmethod
    def publish(self, connection, exchange, route, message):
        pass

    @abstractmethod
    def subscribe(self, connection, queueName, callback):
        pass
