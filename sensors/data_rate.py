from homeassistant.components.sensor import SensorEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiTxRateSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} TX Rate"

    @property
    def unique_id(self):
        return f"{self._device_id}_tx_rate"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("uplink", {})
            .get("txRateBps")
        )

    @property
    def native_unit_of_measurement(self):
        return "bps"

    @property
    def state_class(self):
        return "measurement"


class UniFiRxRateSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} RX Rate"

    @property
    def unique_id(self):
        return f"{self._device_id}_rx_rate"

    @property
    def state(self):
        return (
            self.coordinator.data[self._device_id]
            .get("statistics", {})
            .get("uplink", {})
            .get("rxRateBps")
        )

    @property
    def native_unit_of_measurement(self):
        return "bps"

    @property
    def state_class(self):
        return "measurement"
