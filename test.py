import time
from paho.mqtt import client as mqtt

BROKER = "192.168.1.2"         # À adapter si besoin
PORT_WS = 9002               # Port WebSocket
USERNAME = ""            # À adapter
PASSWORD = ""        # À adapter
TOPIC = "debug/hello"

def main():
	client = mqtt.Client(transport="websockets")
	client.username_pw_set(USERNAME, PASSWORD)
	client.connect(BROKER, PORT_WS)
	client.loop_start()

	counter = 0
	try:
		while True:
			message = f"🔁 Message {counter}"
			client.publish(TOPIC, message)
			print(f"📤 Publié sur {TOPIC} : {message}", flush=True)
			counter += 1
			time.sleep(3)
	except KeyboardInterrupt:
		print("Ctrl + C")
	finally:
		client.loop_stop()
		client.disconnect()
		print("✅ Déconnecté proprement")

if __name__ == "__main__":
	main()
