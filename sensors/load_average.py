from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiLoadAverageSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id, key, label):
        super().__init__(coordinator)
        self._device_id = device_id
        self._key = key
        self._label = label

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} Load {self._label}"

    @property
    def unique_id(self):
        return f"{self._device_id}_load_{self._label}"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id].get("statistics", {}).get(self._key)
        )

    @property
    def state_class(self):
        return "measurement"
