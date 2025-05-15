from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE


class UniFiDeviceCPUSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", self._device_id)
        return f"{name} CPU Usage"

    @property
    def unique_id(self):
        return f"{self._device_id}_cpu"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("cpuUtilizationPct")
        )

    @property
    def native_unit_of_measurement(self):
        return PERCENTAGE

    @property
    def device_class(self):
        return "temperature"  # or leave None

    @property
    def state_class(self):
        return "measurement"

    @property
    def extra_state_attributes(self):
        return {
            "device_id": self._device_id,
        }
