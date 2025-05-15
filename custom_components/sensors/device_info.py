from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity


class UniFiDeviceSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        return f"UniFi Device {self.device_data.get('name', 'Unnamed')}"

    @property
    def unique_id(self):
        return self._device_id

    @property
    def state(self):
        return self.device_data.get("state", "unknown")

    @property
    def device_data(self):
        return self.coordinator.data.get(self._device_id, {})

    @property
    def extra_state_attributes(self):
        data = self.device_data
        stats = data.get("statistics", {})

        return {
            "model": data.get("model"),
            "mac_address": data.get("macAddress"),
            "ip_address": data.get("ipAddress"),
            "firmware": data.get("firmwareVersion"),
            "firmware_updatable": data.get("firmwareUpdatable"),
            "adopted_at": data.get("adoptedAt"),
            "provisioned_at": data.get("provisionedAt"),
            "configuration_id": data.get("configurationId"),
            "uplink_device_id": data.get("uplink", {}).get("deviceId"),
            "features": list(data.get("features", {}).keys()),
            "ports": data.get("interfaces", {}).get("ports", []),
            "radios": data.get("interfaces", {}).get("radios", []),
            # Stats
            "uptime_sec": stats.get("uptimeSec"),
            "last_heartbeat": stats.get("lastHeartbeatAt"),
            "next_heartbeat": stats.get("nextHeartbeatAt"),
            "cpu_utilization_pct": stats.get("cpuUtilizationPct"),
            "memory_utilization_pct": stats.get("memoryUtilizationPct"),
            "load_avg_1min": stats.get("loadAverage1Min"),
            "load_avg_5min": stats.get("loadAverage5Min"),
            "load_avg_15min": stats.get("loadAverage15Min"),
            "uplink_tx_bps": stats.get("uplink", {}).get("txRateBps"),
            "uplink_rx_bps": stats.get("uplink", {}).get("rxRateBps"),
            "radio_stats": stats.get("interfaces", {}).get("radios", []),
        }
