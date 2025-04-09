import json
import time
import requests
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from datetime import datetime


class KafkaConsumerUtility:
    def __init__(
        self,
        bootstrap_servers,
        topic,
        sasl_username,
        sasl_password,
        security_protocol='SASL_SSL',
        sasl_mechanism='PLAIN',
        mongodb_uri=None,
        mongodb_db_name=None,
        mongodb_collection_name=None
    ):
        if not all([bootstrap_servers, topic, sasl_username, sasl_password]):
            raise ValueError("pepsales_retry_lib: Missing one or more required Kafka consumer parameters")

        self.topic = topic
        self.mongodb_collection = None

        # MongoDB setup
        if mongodb_uri and mongodb_db_name and mongodb_collection_name:
            try:
                mongo_client = MongoClient(mongodb_uri)
                self.mongodb_collection = mongo_client[mongodb_db_name][mongodb_collection_name]
                # print(f"Connected to MongoDB collection: {mongodb_collection_name}")
            except Exception as e:
                print(f"pepsales_retry_lib: Failed to connect to MongoDB: {e}")

        # Kafka consumer setup
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            # auto_offset_reset='earliest',
            enable_auto_commit=True,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_username,
            sasl_plain_password=sasl_password,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        # Kafka producer setup
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_username,
            sasl_plain_password=sasl_password,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def consume_messages(self):
        # print("Listening for messages...")
        for message in self.consumer:
            # print(f"Received message: {message.value}")
            self.execute_request(message.value)

    def execute_request(self, message):
        try:
            request_data = message.get("request_data", {})
            retries = message.get("retries", 0)
            wait_time = message.get("wait_time", 2)
            on_success = message.get("on_success", None)
            on_failure = message.get("on_failure", None)

            # print(f"Executing API request with: {request_data}")
            response = requests.request(**request_data)

            if response.status_code == 200:
                if on_success:
                    requests.request(**on_success)
                    # print(f"Executing success callback: {on_success}")

                # print(f"API call successful: {response.status_code}")

                # Log success to MongoDB
                if self.mongodb_collection is not None:
                    try:
                        timestamp = datetime.utcnow().isoformat() + "Z"
                        self.mongodb_collection.insert_one({
                            "message": message,
                            "status": "success",
                            "response": response.json(),
                            "timestamp": timestamp
                        })
                        # print("Logged success to MongoDB.")
                    except Exception as mongo_error:
                        print(f"pepsales_retry_lib: Failed to log success to MongoDB: {mongo_error}")
            else:
                # print(f"API request failed with status: {response.status_code}")
                raise ValueError(f"pepsales_retry_lib: API request failed with status: {response.status_code}")

        except Exception as e:
            # print(f"API request failed with error: {e}")

            if retries > 0:
                message["retries"] -= 1
                # print(f"Retrying API request in {wait_time} seconds, remaining retries: {retries - 1}")
                time.sleep(wait_time)
                self.producer.send(self.topic, value=message)
                self.producer.flush()
            else:
                if on_failure:
                    requests.request(**on_failure)
                    # print(f"Executing failure callback: {on_failure}")

                # print("Retries exhausted. API request failed permanently.")

                # Log failure to MongoDB
                if self.mongodb_collection is not None:
                    try:
                        timestamp = datetime.utcnow().isoformat() + "Z"
                        self.mongodb_collection.insert_one({
                            "message": message,
                            "status": "failure",
                            "error": str(e),
                            "timestamp": timestamp
                        })
                        # print("Logged failure to MongoDB.")
                    except Exception as mongo_error:
                        print(f"pepsales_retry_lib: Failed to log failure to MongoDB: {mongo_error}")


# Example usage
if __name__ == '__main__':
    consumer = KafkaConsumerUtility()
    consumer.consume_messages()