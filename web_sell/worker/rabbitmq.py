import pika
import json
class RabbitmqClient:
    def __init__(self, host, port, user_name, password, virtual_host):
        super().__init__()
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        self.virtual_host = virtual_host
        self.connection = None
    def connect(self):
        credentials = pika.PlainCredentials(self.user_name, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials)
        )
    def init_queue(self, queue_name,durable=True, max_priority=-1):
        channel = self.connection.channel()
        if max_priority == -1:
            channel.queue_declare(queue=queue_name, durable=durable)
        else:
            channel.queue_declare(queue=queue_name, durable=durable, arguments={'x-max-priority': max_priority})
        return channel
    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
    def is_connected(self):
        return self.connection is not None and self.connection.is_open
    @staticmethod
    def publish_message(channel, routing_key, body, priority=-1, delivery_mode=2, exchange=''):
        if priority == -1:
            channel.basic_publish(exchange = exchange, routing_key=routing_key,body=json.dumps(body),properties=pika.BasicProperties(delivery_mode=delivery_mode))
        else:
            channel.basic_publish(exchange = exchange, routing_key=routing_key,body=json.dumps(body),properties=pika.BasicProperties(delivery_mode=delivery_mode,priority=priority))
    @staticmethod
    def run_consummer(channel, queue_name, callback_func):
        print("  * wait message ")
        def callback(ch, method,_,body):
            body=json.loads(body)
            callback_func(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("  * done receive: ")
        channel.basic_qos(prefetch_count=10)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()