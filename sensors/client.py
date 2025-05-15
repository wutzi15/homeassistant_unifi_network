from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class UniFiClientSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, client_id):
        super().__init__(coordinator)
        self._client_id = client_id

    @property
    def name(self):
        client = self.client
        return (
            f"Client {client.get('name') or client.get('ipAddress') or self._client_id}"
        )

    @property
    def unique_id(self):
        return f"unifi_client_{self._client_id}"

    @property
    def state(self):
        return self.client.get("ipAddress")

    @property
    def client(self):
        return self.coordinator.data.get(self._client_id, {})

    @property
    def extra_state_attributes(self):
        c = self.client
        return {
            "id": c.get("id"),
            "name": c.get("name"),
            "connected_at": c.get("connectedAt"),
            "ip_address": c.get("ipAddress"),
            "access_type": c.get("access", {}).get("type"),
        }
