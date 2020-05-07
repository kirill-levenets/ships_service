
import rabbitpy


RABITMQ_URL = "amqp://guest:guest@localhost:5672/%2F"


class RabbitQueue:
    def __init__(self, exchange_name, queue_name):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = queue_name

        self.connection = rabbitpy.Connection(RABITMQ_URL)
        self.channel = self.connection.channel()

        self.exchange = rabbitpy.Exchange(
            self.channel, self.exchange_name, durable=True)
        self.exchange.declare()

        self.queue = rabbitpy.Queue(
            self.channel, self.queue_name, durable=True)
        self.queue.declare()

        self.queue.bind(self.exchange_name, routing_key=self.routing_key)

    def publish(self, msg: dict):
        m = rabbitpy.Message(self.channel, msg)
        m.publish(self.exchange_name, routing_key=self.routing_key)

    def consume_generator(self, threads=1):
        for msg in self.queue.consume(prefetch=threads):
            data = msg.json()
            if not data:
                msg.ack()
                break
            yield data
            msg.ack()
            # msg.nack(requeue=True)

    def count(self):
        return len(self.queue)

    def close(self):
        self.channel.close()
        self.connection.close()


rq = RabbitQueue('test-exchange', 'test-queue')

for i in range(100_000):
    rq.publish({'url': 'htpp://.......'})

rq.publish({})

for msg in rq.consume_generator():
    print(msg)

rq.close()
