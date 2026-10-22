from datetime import datetime
import json
import os

class WaterReading:
    def __init__(self, name: str, pH: float, temperature: float, ammonia: float, timestamp: str = None):
        self.timestamp = timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M")
        self.name = name
        self.pH = pH
        self.temperature = temperature
        self.ammonia = ammonia

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "name": self.name,
            "pH": self.pH,
            "temperature": self.temperature,
            "ammonia": self.ammonia,
        }


class ReadingManager:
    def __init__(self, username: str = None):
        self.readings = []
        self.username = username
        self.file_path = None

        base_dir = os.path.join(os.getcwd(), "users")
        os.makedirs(base_dir, exist_ok=True)

        if username:
            user_dir = os.path.join(base_dir, username)
            os.makedirs(user_dir, exist_ok=True)
            self.file_path = os.path.join(user_dir, "readings.json")
            self.load_readings()

    def add_reading(self, reading: WaterReading):
        self.readings.append(reading)
        self.save_readings()
        self.load_readings()

    def get_all(self):
        return [r.to_dict() for r in self.readings]

    def clear_readings(self):
        self.readings.clear()
        self.save_readings()

    def save_readings(self):
        if not self.file_path:
            return
        with open(self.file_path, "w") as f:
            json.dump([r.to_dict() for r in self.readings], f, indent=4)

    def load_readings(self):
        if not self.file_path or not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, "r") as f:
            data = json.load(f)
        
        self.readings = [WaterReading(d["name"], d["pH"], d["temperature"], d["ammonia"], d["timestamp"]) for d in data]