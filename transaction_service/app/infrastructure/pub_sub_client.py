import json
import logging

from google.cloud import pubsub_v1


class PubSubClient:
    def __init__(self, project_id, topic_name):
        self.project_id = project_id
        self.topic_name = topic_name

    def send_message(self, message):
        logging.info('Sending message to PubSUb')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id, self.topic_name)

        payload = json.dumps(message)
        logging.info(f'Message published : {payload}')
        payload = payload.encode('utf-8')

        publisher.publish(topic_path, payload)
