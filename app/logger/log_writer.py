import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class LogWriter:
	def __init__(self, base_dir, max_bytes=1000000, backup_count=5):
		self.base_dir = base_dir
		self.max_bytes = max_bytes
		self.backup_count = backup_count
		os.makedirs(base_dir, exist_ok=True)
		self.handlers = {}

	def get_logger(self, topic):
		name = topic.split("/", 1)[-1]
		log_dir = os.path.join(self.base_dir, name)
		os.makedirs(log_dir, exist_ok=True)
		log_path = os.path.join(log_dir, f"{name}.log")
		print(f"Creating log file at: {log_path}", flush=True)

		if name not in self.handlers:
			handler = RotatingFileHandler(log_path, maxBytes=self.max_bytes, backupCount=self.backup_count)
			formatter = logging.Formatter('%(asctime)s - %(message)s')
			handler.setFormatter(formatter)

			logger = logging.getLogger(f"mqtt_logger.{name}")
			logger.setLevel(logging.INFO)
			logger.addHandler(handler)
			logger.propagate = False
			self.handlers[name] = logger

		return self.handlers[name]


	def write(self, topic, message):
		logger = self.get_logger(topic)
		print(f"📩 Écriture dans le log pour {topic} : {message}", flush=True)
		logger.info(message)
		for handler in logger.handlers:
			handler.flush()

