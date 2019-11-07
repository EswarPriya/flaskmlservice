import datetime
import json
import threading
import time

import config
import pika
from MessageBroker import MessageBrokerFactory
from service import DemoService
from util import Log


class Task():
    host = config.QUEUE_HOST
    userName = config.QUEUE_USER_NAME
    password = config.QUEUE_PASSWORD
    port = config.QUEUE_PORT

    def publish(self, data, queue, routeKey, exchangeName, exchangeType):
        Broker = self.createBroker(queue, exchangeName, exchangeType)
        Broker.queue_bind(queue, exchangeName, routeKey)
        Broker.publish(exchangeName, routeKey, data)
        Broker.close_connection()

    def subscribe(self):
        queue = config.SUBSCRIBE_QUEUE_NAME
        exchangeName = config.SUBSCRIBE_QUEUE_EXCHANGE_NAME
        exchangeType = config.SUBSCRIBE_QUEUE_EXCHANGE_TYPE
        exchangeKey = config.SUBSCRIBE_ROUTE_KEY
        Broker = self.createBroker(queue, exchangeName, exchangeType)
        Broker.queue_bind(queue, exchangeName, exchangeKey)
        Broker.subscribe(exchangeName, queue, self.callback)

    def createBroker(self, queue, exchange, exchangeType):
        subscribeBroker = MessageBrokerFactory()
        Broker = subscribeBroker.get_broker('rabbitmq')
        connection = Broker.build_broker(self.host, self.port, self.userName, self.password)
        Broker.open_connection(connection)
        Broker.declare_queue(queue)
        Broker.declare_exchange(exchange, exchangeType)
        return Broker

    def callback(self, channel, method, properties, body):
        try:
            data = json.loads(body)
            # this solves the issue of pikka time out when the process takes more than 180 sec

            thread = threading.Thread(target=self.process_data, args=(data,))
            thread.start()
            while thread.is_alive():  # Loop while the thread is processing
                channel._connection.sleep(1.0)

        except ValueError:
            Log.info("000", Log.LEVEL_ERROR, "Invalid Json: " + str(body))
        except Exception as e:
            Log.info(data["_id"], Log.LEVEL_ERROR, str(e))
            errorData = self.process_error(data, str(e))
            self.publish(errorData, config.ERROR_QUEUE_NAME, config.ERROR_ROUTE_KEY, config.ERROR_QUEUE_EXCHANGE_NAME,
                         config.ERROR_QUEUE_EXCHANGE_TYPE)
        finally:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def process_output(self, output, data):
        if output is not None:
            self.publish(output, config.PUBLISH_QUEUE_NAME, config.PUBLISH_ROUTE_KEY,
                         config.PUBLISH_QUEUE_EXCHANGE_NAME, config.PUBLISH_QUEUE_EXCHANGE_TYPE)
        else:
            error = "transcript was not generated"
            Log.info(data["_id"], Log.LEVEL_ERROR, error)
            errorData = self.process_error(data, error)
            self.publish(errorData, config.ERROR_QUEUE_NAME, config.ERROR_ROUTE_KEY, config.ERROR_QUEUE_EXCHANGE_NAME,
                         config.ERROR_QUEUE_EXCHANGE_TYPE)

    def process_data(self, data):
        # only change this method to call the service layer
        try:
            output = DemoService.doSomething()
            if output != "":
                output = json.dumps(data)
            else:
                output = None

            Log.info(data["_id"], Log.LEVEL_OUTPUT, "Done")
            self.process_output(output, data)
        except Exception as e:
            Log.info(data["_id"], Log.LEVEL_ERROR, str(e))
            errorData = self.process_error(data, str(e))
            self.publish(errorData, config.ERROR_QUEUE_NAME, config.ERROR_ROUTE_KEY, config.ERROR_QUEUE_EXCHANGE_NAME,
                         config.ERROR_QUEUE_EXCHANGE_TYPE)

    def process_error(self, data, error):
        currentDT = datetime.datetime.now()
        data['errorTime'] = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        data['api'] = config.APP_NAME
        data['error'] = error
        return json.dumps(data)


if __name__ == '__main__':
    task = Task()
    print("running task")
    try:
        task.subscribe()
    except pika.exceptions.StreamLostError:
        print("stream exception")
        time.sleep(2 * 60)
        task.subscribe()
