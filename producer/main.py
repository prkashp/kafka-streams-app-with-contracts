import datetime
import json
import os
from time import sleep
import logging
from faker import Faker
from kafka import KafkaProducer
from kafka.admin import NewTopic, KafkaAdminClient
from pydantic import BaseModel
from schema_registry.client import SchemaRegistryClient
from register_schema import register
from register_schema import client
# BOOTSTRAP_SERVERS = (
#     "kafka:9092" if os.getenv("RUNTIME_ENVIRONMENT") == "DOCKER" else "localhost:9092"
# )
BOOTSTRAP_SERVERS = "broker:9092" 

TOPIC = "USERS"

class User(BaseModel):
    ts: str
    name: str
    country: str
    # age: int
    date_of_birth: str


def create_topic_if_not_exists():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS, api_version=(3,7))
        # logging.info("Admin client created : ",admin_client)
        print(admin_client)
    except Exception as e:
        # logging.error("Error: ",e)
        return(e,BOOTSTRAP_SERVERS)
    if TOPIC not in admin_client.list_topics():
        admin_client.create_topics(
            [NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)]
        )
        print("Topic Created")


def push_messages():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        api_version=(0,10)
    )
    fake = Faker()

    # client = SchemaRegistryClient(url="http://schema-registry:8081")

    for i in range(10):
        data = User(
            ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            name=fake.name(),
            country=fake.country(),
            date_of_birth=str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=100)),
            # age=fake.random_int(min=0, max=100),
        )
        # Get the latest schema from the registry and serialize the message with it
        # try:
        #     compatibility = client.test_compatibility("USERS-value", data.schema_json(), schema_type="JSON")
        # except Exception as e:
        #     return (data, e, client)
        # if not compatibility:
        #     raise Exception("Schema is not compatible with the latest version")

        producer.send(topic=TOPIC, key=str(i).encode("utf-8"), value=json.dumps(data.dict()).encode("utf-8"))
        print(f"Sent message {i} -> {data}")
        sleep(2)


if __name__ == "__main__":
    registry_id = register()
    print(registry_id)
    create_topic_if_not_exists()
    push_messages()
