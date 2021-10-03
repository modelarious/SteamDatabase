



from time import sleep
from json import dumps
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8'))

def deserialize(val):
    return loads(val.decode('utf-8'))

from kafka import KafkaConsumer
from json import loads
consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     auto_commit_interval_ms=100,
     group_id='my-group',
     value_deserializer=deserialize
)

# for val in [{'hello': 'goodbydde'}]:
#     x = producer.send('test', value=val)
#     print(x.get(timeout=30)) # ensure send has succeeded

print("reading messages")
for message in consumer:
    print(message.value)

