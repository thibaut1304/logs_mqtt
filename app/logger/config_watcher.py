from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class ConfigWatcher(FileSystemEventHandler):
	def __init__(self, path, on_change_callback):
		self._path = path
		self._on_change_callback = on_change_callback

	def on_modified(self, event):
		if event.src_path.endswith("config.json"):
			print("🌀 Fichier de configuration modifié. Rechargement...", flush=True)
			self._on_change_callback()

def start_config_watcher(path, on_change_callback):
	event_handler = ConfigWatcher(path, on_change_callback)
	observer = Observer()
	observer.schedule(event_handler, os.path.dirname(path), recursive=False)
	observer.daemon = True
	observer.start()
