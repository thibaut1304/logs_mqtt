import subprocess
import threading
import time
import os

class RsyncUploader:
	def __init__(self, local_dir, remote_path, interval_sec=3600):
		self.local_dir = local_dir
		self.remote_path = remote_path
		self.interval = interval_sec
		self.ssh_key_path = "/app/.ssh/id_rsa"
		if not os.path.exists(self.ssh_key_path):
			print(f"[Rsync] ❌ Clé SSH introuvable à {self.ssh_key_path}. Sync désactivé.", flush=True)
			self.enabled = False
		else:
			self.enabled = True
		self.thread = threading.Thread(target=self._loop, daemon=True)

		# Securité normalement inutile mais protege contre l'empillement de thread
		self.lock = threading.Lock()
		self.running = False

	def start(self):
		if not self.running:
			self.thread.start()
			self.running = True

	def _loop(self):
		while True:
			try:
				if self.enabled and self._check_ssh_connection():
					self.sync()
				else:
					print("❌ SSH connection failed or key not provided", flush=True)
			except Exception as e:
				print(f"⚠️ Rsync error: {e}", flush=True)

			time.sleep(self.interval)

	def _check_ssh_connection(self):
		user_host = self.remote_path.split(":", 1)[0]
		cmd = ["ssh", "-i", self.ssh_key_path, "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no", user_host, "echo OK"]
		try:
			result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
			return result.returncode == 0
		except Exception as e:
			print(f"🚫 SSH check failed: {e}", flush=True)
			return False

	def sync(self):
		cmd = [
			"rsync", "-avz", "--delete",
			"-e", f"ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no",
			self.local_dir + "/", self.remote_path
		]
		try:
			subprocess.run(cmd, check=True)
			print(f"✅ [Rsync] Sync completed", flush=True)
			print(f"⏳ [Rsync] Prochaine tentative dans {self.interval} sec", flush=True)
		except subprocess.CalledProcessError as e:
			print(f"❌ [Rsync] Failed: {e}", flush=True)
