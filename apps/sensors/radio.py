from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    PERCENTAGE,
)


class UniFiRadioRetrySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id, frequency):
        super().__init__(coordinator)
        self._device_id = device_id
        self._frequency = frequency

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} {self._frequency}GHz TX Retries"

    @property
    def unique_id(self):
        return f"{self._device_id}_retries_{self._frequency}GHz"

    @property
    def state(self):
        radios = (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("interfaces", {})
            .get("radios", [])
        )
        for radio in radios:
            if str(radio.get("frequencyGHz")) == str(self._frequency):
                return radio.get("txRetriesPct")
        return None

    @property
    def native_unit_of_measurement(self):
        return PERCENTAGE

    @property
    def state_class(self):
        return "measurement"

    @property
    def device_class(self):
        return None
