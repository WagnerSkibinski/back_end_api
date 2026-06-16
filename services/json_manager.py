import json
import os
from threading import Lock
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
_lock = Lock()


def _file_path(filename):
	return os.path.join(DATABASE_DIR, filename)


def load_data(filename):
	path = _file_path(filename)
	if not os.path.exists(path):
		return []

	with open(path, "r", encoding="utf-8") as file:
		content = file.read().strip()
		if not content:
			return []
		return json.loads(content)


def save_data(filename, data):
	path = _file_path(filename)
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with _lock:
		with open(path, "w", encoding="utf-8") as file:
			json.dump(data, file, ensure_ascii=False, indent=4)


def next_id(records):
	if not records:
		return 1
	return max(item.get("id", 0) for item in records) + 1


def append_log(action, resource, details=None):
	logs = load_data("logs.json")
	log_item = {
     
		"id": next_id(logs),
		"timestamp": datetime.utcnow().isoformat(),
		"action": action,
		"resource": resource,
		"details": details or {},
	}
	logs.append(log_item)
	save_data("logs.json", logs)
