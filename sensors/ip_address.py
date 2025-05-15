from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import logging

_LOGGER = logging.getLogger(__name__)


class UniFiIpAddressSensor(CoordinatorEntity, SensorEntity):
    """Representation of a UniFi connected at sensor."""

    def __init__(self, coordinator, client_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._client_id = client_id

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self.coordinator.data[self._client_id].get("name", "Unknown")
        return f"{name} IP Address"

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"unifi_client_{self._client_id}_ip_address"

    @property
    def state(self):
        """Return the state of the sensor."""
        try:
            return self.coordinator.data[self._client_id].get("ipAddress", "Unknown")
        except Exception as e:
            _LOGGER.error(
                "Error fetching IP Address for client %s: %s", self._client_id, e
            )
            return "Unknown"
