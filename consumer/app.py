from kafka import KafkaProducer


def run():
    kafka_consumer = Consumer(
        {
            "enable.auto.commit": True,
            "bootstrap.servers": "queue:19092",
            "security.protocol": "ssl",
            "default.topic.config": {"auto.offset.reset": "smallest"}
        }
    )
    consumer.subscribe("items")

    # Now loop on the consumer to read messages
    running = True

    while running:
        message = kafka_consumer.poll()
        item = json.load(message.value.decode())
        print("Ready to consume {0}".format(item))

        # here we should finally perform my business logic!

    kafka_consumer.close()


if __name__ == '__main__':
    run()
