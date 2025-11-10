import os
import time
import threading
import random

from cyclonedds.core import Listener
from cyclonedds.domain import DomainParticipant
from cyclonedds.internal import InvalidSample
from cyclonedds.pub import Publisher, DataWriter
from cyclonedds.sub import Subscriber, DataReader
from cyclonedds.topic import Topic

from vehicles import Vehicle

PAYLOAD_BYTES=1024*1024

# Publishes Vehicle message with additional 'data' field filled with 1MB random paybload. Topic name is passed in 'name'. 
def vehicle_publisher(topic_name):
    domain_participant = DomainParticipant(0)
    topic = Topic(domain_participant, topic_name, Vehicle, qos=None)
    publisher = Publisher(domain_participant)
    writer = DataWriter(publisher, topic)

    random_data_buffer = os.urandom(PAYLOAD_BYTES)
    vehicle = Vehicle(name=topic_name, x=200, y=200, data=random_data_buffer)

    while True:
        writer.write(vehicle)
        time.sleep(random.random() * 0.3)

# Subscribes to Vehicle messages and checks that the topic name from the publisher stored at Vehicle.name field is the expected one.
class MyListener(Listener):
    def __init__(self, topic_name):
        super().__init__()
        self.expected_topic = topic_name

    def on_data_available(self, reader: DataReader):
        # Read sample
        sample = reader.take()[0]
        # Skip invalid samples
        if sample is None or isinstance(sample, InvalidSample):
            print("Invalid sample")
            return
        
        if self.expected_topic != sample.name:
            print(f"[!!!] Unexpected topic name [!!!]: {sample.name}, expected: {self.expected_topic}")
            return

        print(f"Received message from topic: {sample.name}")

def vehicle_subscriber(topic_name):
    listener = MyListener(topic_name)

    domain_participant = DomainParticipant(0)
    topic = Topic(domain_participant, topic_name, Vehicle, qos=None)
    subscriber = Subscriber(domain_participant)
    reader = DataReader(domain_participant, topic, listener=listener)

    print("Wait for data...")
    while True:
        time.sleep(1.0)

# Start 2x publishers with different topic names
print("-----------------------------")
print("Publishing to topics:")
print(" - topic/vehicle1")
print(" - topic/vehicle2")
print("Subscribing to topic: topic/vehicle1")
print("-----------------------------")

thread_pub1 = threading.Thread(target=vehicle_publisher, args=("topic/vehicle1",))
thread_pub2 = threading.Thread(target=vehicle_publisher, args=("topic/vehicle2",))

# Subscribe to first publisher topic ('topic/vehicle1')
thread_sub = threading.Thread(target=vehicle_subscriber, args=("topic/vehicle1",))

# Start subscriber
thread_sub.start()

# Start publishers
time.sleep(0.2)
thread_pub1.start()
time.sleep(0.2)
thread_pub2.start()

# Run forever
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping publishers")
