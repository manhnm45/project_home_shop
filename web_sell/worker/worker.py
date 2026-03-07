import json
import pika
import asyncio
from channels.layers import get_channel_layer
import rabbitmq
import yaml
import os
import django
import sys
# đường dẫn đến thư mục ngoài cùng (nơi chứa manage.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

print("BASE_DIR =", BASE_DIR)
print("sys.path =", sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_sell.settings")
django.setup() 
channel_layer = get_channel_layer()

def callback(body):
    data = {}
    # {"image_path": "./image_object_save/image_object_176348717933017_0.jpg", "timestamp": 176348717933017.75, "product_id": ["bot_chien_xurotate90 "]}
    data["image_path"] = body.get("image_path", "")
    data["timestamp"] = body.get("timestamp", "")
    data["product_id"] = body.get("product_id", [])
    data["cost"] = body.get("cost", "")
    asyncio.run(channel_layer.group_send(
        "ai_group",
        {"type": "ai_message", "data": data}
    ))


if __name__ == "__main__":
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    rabbitmq_host = config["rabbimq_host"]
    rabbitmq_port = config["rabbimq_port"]
    rabbitmq_username = config["rabbimq_username"]
    rabbitmq_password = config["rabbimq_password"]
    exchange = config["exchange"]
    vitualhost = config["vitualhost"]
    rabbitmq = rabbitmq.RabbitmqClient(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, vitualhost)        
    rabbitmq.connect()
    queue_name_get = "update_userui"
    channel = rabbitmq.init_queue(queue_name=queue_name_get, durable=True)
    rabbitmq.run_consummer(channel, queue_name_get, callback)
