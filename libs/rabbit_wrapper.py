
import rabbitpy


from settings import RABITMQ_URL


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
            # msg.ack()

    def get_generator(self, exit_event):
        while not exit_event.is_set():
            msg = self.queue.get(acknowledge=True)
            yield msg

    def count(self):
        return len(self.queue)

    def close(self):
        self.channel.close()
        self.connection.close()


if __name__ == '__main__':
    rq = RabbitQueue('test-exchange', 'test-queue')

    if rq.count() == 0:
        for i in range(100):
            rq.publish({'url': f'http://{i}'})

        rq.publish({})

    from threading import Event
    ex_ev = Event()

    for raw_msg in rq.get_generator(ex_ev):
        if not raw_msg:
            break
        print(raw_msg.json())
        raw_msg.nack(requeue=False)

    rq.close()
