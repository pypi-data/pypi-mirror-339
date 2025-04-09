from kafka import KafkaProducer
import json

class KafkaProducerUtility:
    def __init__(self, 
                bootstrap_servers, 
                topic, 
                sasl_username,
                sasl_password,
                security_protocol='SASL_SSL',
                sasl_mechanism='PLAIN'
            ):
        if not all([bootstrap_servers, topic, sasl_username, sasl_password]):
            raise ValueError("Missing one or more required Kafka producer parameters")

        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_username,
            sasl_plain_password=sasl_password,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_request(self, request_data, retries=3, wait_time=2, on_success=None, on_failure=None):
        """
        `request_data` should be a dictionary compatible with `requests.request(**request_data)`
        `wait_time` is the delay between retries in seconds
        """
        message = {
            "request_data": request_data,
            "retries": retries,
            "wait_time": wait_time,
            "on_success": on_success,
            "on_failure": on_failure
        }

        self.producer.send(self.topic, value=message)
        self.producer.flush()
        return {"status": "Message sent"}



# Example usage
if __name__ == '__main__':
    producer = KafkaProducerUtility()

