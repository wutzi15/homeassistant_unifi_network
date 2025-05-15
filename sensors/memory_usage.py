from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiMemoryUsageSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} Memory Usage"

    @property
    def unique_id(self):
        return f"{self._device_id}_memory"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("memoryUtilizationPct")
        )

    @property
    def native_unit_of_measurement(self):
        return PERCENTAGE

    @property
    def state_class(self):
        return "measurement"
