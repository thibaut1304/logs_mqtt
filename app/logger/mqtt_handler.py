import paho.mqtt.client as mqtt

class MQTTHandler:
	def __init__(self, config_mqtt, config_topics, log_writer):
		self.config_mqtt = config_mqtt
		self.config_topics = config_topics
		self.log_writer = log_writer
		self.client = mqtt.Client(transport="websockets")
		self.client.username_pw_set(self.config_mqtt["username"], self.config_mqtt["password"])
		self.client.on_message = self.on_message

	def update_config(self, new_config):
		self.config_mqtt = new_config["mqtt"]
		self.config_topics = new_config["topics"]

		self.client.loop_stop()
		self.client.disconnect()

		self.client = mqtt.Client(transport="websockets")
		self.client.username_pw_set(self.config_mqtt["username"], self.config_mqtt["password"])
		self.client.on_message = self.on_message
		self.connect_and_subscribe()

		for topic in self.config_topics:
			self.log_writer.get_logger(topic)

		print("📦 MQTTHandler: Config mise à jour.", flush=True)

	def on_message(self, client, userdata, msg):
		message = msg.payload.decode()
		print(f"[MQTT] {msg.topic}: {message}", flush=True)
		self.log_writer.write(msg.topic, message)


	def connect_and_subscribe(self):
		self.client.connect(self.config_mqtt["broker"], self.config_mqtt["port_ws"])
		print("Hello mqtt bien connect'e", flush=True)
		for topic in self.config_topics:
			self.client.subscribe(topic)
			print(f"📥 Subscribed to topic: {topic}", flush=True)
		self.client.loop_start()
