from logger.config_loader import load_config
from logger.mqtt_handler import MQTTHandler
from logger.log_writer import LogWriter
from logger.rsync_uploader import RsyncUploader
from logger.config_watcher import start_config_watcher
import time

mqtt = None

def reload_config():
	global mqtt
	try:
		new_config = load_config()
		mqtt.update_config(new_config)
		print("✅ Nouvelle config chargée avec succès.", flush=True)
	except Exception as e:
		print(f"⚠️ Erreur lors du rechargement de la config : {e}", flush=True)
		print("⚠️ Ancienne configuration conservée.", flush=True)

def main():
	config = load_config()
	log_writer = LogWriter(**config["logging"])
	global mqtt
	mqtt = MQTTHandler(config["mqtt"], config["topics"], log_writer)
	mqtt.connect_and_subscribe()

	start_config_watcher("conf/config.json", reload_config)

	if config.get("rsync", {}).get("enabled"):
		uploader = RsyncUploader(
			config["logging"]["base_dir"],
			config["rsync"]["remote_path"],
			config["rsync"]["interval_sec"]
		)
		uploader.start()

	print("Logger ready. Listening for messages...", flush=True)

	while True:
		time.sleep(1)


if __name__ == "__main__":
	main()
