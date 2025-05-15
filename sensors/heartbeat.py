from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiLastHeartbeatSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} Last Heartbeat"

    @property
    def unique_id(self):
        return f"{self._device_id}_last_heartbeat"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("lastHeartbeatAt")
        )


class UniFiNextHeartbeatSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} Next Heartbeat"

    @property
    def unique_id(self):
        return f"{self._device_id}_next_heartbeat"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("nextHeartbeatAt")
        )
