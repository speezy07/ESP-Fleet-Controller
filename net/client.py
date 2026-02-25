import requests
from typing import Optional, Dict

class ESPClient:
    def __init__(self, ip: str, api_key: Optional[str] = None, timeout: int = 5):
        self.base = f"http://{ip}"
        self.timeout = timeout
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})

    def _get(self, endpoint: str) -> Optional[Dict]:
        try:
            r = self.session.get(self.base + endpoint, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    def _post(self, endpoint: str, json_data: Dict) -> bool:
        try:
            r = self.session.post(self.base + endpoint, json=json_data, timeout=self.timeout)
            r.raise_for_status()
            return True
        except Exception:
            return False

    def get_info(self) -> Optional[Dict]:
        return self._get("/api/info")

    def get_health(self) -> Optional[Dict]:
        return self._get("/api/health")

    def get_status(self) -> Optional[Dict]:
        return self._get("/api/status")

    def locate(self, enable: bool, seconds: int) -> bool:
        return self._post("/api/locate", {"enable": enable, "seconds": seconds})

    def control(self, payload: Dict) -> bool:
        return self._post("/api/control", payload)


class MockESPClient:
    def __init__(self, ip: str):
        self.ip = ip
        self._counter = 0

    def get_info(self):
        return {"id": f"mock-{self.ip[-2:]}", "name": f"Mock Device {self.ip[-2:]}",
                "chip": "ESP32", "fw": "1.2.3", "mac": "00:11:22:33:44:55"}

    def get_health(self):
        self._counter += 1
        return {
            "uptime_s": 3600 * (self._counter % 24),
            "free_heap": 180000 - (self._counter % 1000),
            "rssi": -40 - (self._counter % 30),
            "battery_v": 3.7 + (self._counter % 10) / 10,
            "temp_c": 38 + (self._counter % 15)
        }

    def get_status(self):
        return {"online": True, "last_seen_epoch": 1700000000, "latency_ms": 12}

    def locate(self, enable: bool, seconds: int):
        return True

    def control(self, payload: Dict):
        return True