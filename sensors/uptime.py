from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiUptimeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} Uptime"

    @property
    def unique_id(self):
        return f"{self._device_id}_uptime"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("uptimeSec")
        )

    @property
    def native_unit_of_measurement(self):
        return "s"

    @property
    def state_class(self):
        return "total_increasing"
