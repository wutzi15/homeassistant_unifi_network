from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiAccessTypeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a UniFi access type sensor."""

    def __init__(self, coordinator, device_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self.coordinator.data[self._device_id].get("name", "Unknown")
        return f"{name} Access Type"

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self._device_id}_access_type"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._device_id].get("access", {}).get("type")
