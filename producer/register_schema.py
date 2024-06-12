import datetime
import logging
from pydantic import BaseModel
from schema_registry.client import SchemaRegistryClient


SCHEMA_REGISTRY_URL="http://schema-registry:8081"

client = SchemaRegistryClient(url=SCHEMA_REGISTRY_URL)


class User(BaseModel):
    ts: datetime.datetime
    name: str
    country: str
    age: int

def register():
    try:
        schema_id = client.register("USERS-key", User.schema_json(), schema_type="JSON")
        return schema_id
        # logging.info("Schema registed: ",schema_id)
    except Exception as e:
        # logging.error("Error :",e)
        return (e)