from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging

_LOGGER = logging.getLogger(__name__)


class UnifiCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api, site_id, update_interval=timedelta(seconds=10)):
        super().__init__(
            hass,
            _LOGGER,
            name="UniFi Device Coordinator",
            update_interval=update_interval,
        )
        self.api = api
        self.site_id = site_id

    async def _async_update_data(self):
        try:
            devices = await self.api.get_devices_paginated(self.site_id)
            full_devices = {}

            for dev in devices:
                dev_id = dev.get("id")
                if not dev_id:
                    continue

                try:
                    details = await self.api.get_device_details(self.site_id, dev_id)
                    stats = await self.api.get_device_statistics(self.site_id, dev_id)

                    combined = {**details, "statistics": stats}
                    full_devices[dev_id] = combined
                except Exception as e:
                    _LOGGER.warning("Failed to fetch device data for %s: %s", dev_id, e)

            # # fetch client data
            # clients = await self.api.get_clients_paginated(self.site_id)
            # for client in clients:
            #     client_id = client.get("id")
            #     _LOGGER.debug("Client ID: %s", client_id)
            return full_devices
        except Exception as e:
            raise UpdateFailed(f"Error fetching UniFi device data: {e}")


class UnifiClientCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, api, site_id, update_interval=timedelta(seconds=10)):
        super().__init__(
            hass,
            _LOGGER,
            name="UniFi Client Coordinator",
            update_interval=update_interval,
        )
        self.api = api
        self.site_id = site_id

    async def _async_update_data(self):
        """Fetch client data from the API."""

        clients = await self.api.get_clients_paginated(self.site_id)
        return {client["id"]: client for client in clients}
