import aiohttp
import async_timeout
import ssl
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class UnifiAPI:
    def __init__(self, host, api_key, hass: HomeAssistant):
        self._host = host
        self._api_key = api_key
        self._session = aiohttp.ClientSession()
        self._hass = hass
        self._ssl_context = None

    async def async_initialize(self):
        self._ssl_context = await self._hass.async_add_executor_job(
            self._create_ssl_context
        )

    def _create_ssl_context(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    async def get_sites(self):
        if not self._ssl_context:
            await self.async_initialize()

        url = f"https://{self._host}/proxy/network/integrations/v1/sites"
        headers = {
            "X-API-KEY": self._api_key,
            "Accept": "application/json",
        }

        try:
            async with async_timeout.timeout(10):
                async with self._session.get(
                    url, headers=headers, ssl=self._ssl_context
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to fetch sites: {resp.status}")
                    data = await resp.json()
                    _LOGGER.debug("Raw site data: %s", data)
                    return data.get("data", [])
        except Exception as e:
            _LOGGER.error("Error fetching sites: %s", e)
            return []

    async def get_devices_paginated(self, site_id, limit=100):
        all_devices = []
        offset = 0

        while True:
            url = f"https://{self._host}/proxy/network/integrations/v1/sites/{site_id}/devices"
            headers = {
                "X-API-KEY": self._api_key,
                "Accept": "application/json",
            }
            params = {
                "limit": limit,
                "offset": offset,
            }

            async with async_timeout.timeout(10):
                async with self._session.get(
                    url, headers=headers, params=params, ssl=self._ssl_context
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to fetch devices: {resp.status}")
                    data = await resp.json()
                    devices = data.get("data", [])
                    total_count = data.get("totalCount", 0)
                    all_devices.extend(devices)

                    if offset + limit >= total_count:
                        break
                    offset += limit

        return all_devices

    async def get_device_details(self, site_id: str, device_id: str) -> dict:
        url = f"https://{self._host}/proxy/network/integrations/v1/sites/{site_id}/devices/{device_id}"
        headers = {
            "X-API-KEY": self._api_key,
            "Accept": "application/json",
        }

        async with async_timeout.timeout(10):
            async with self._session.get(
                url, headers=headers, ssl=self._ssl_context
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Failed to fetch device {device_id}: {resp.status}"
                    )
                return await resp.json()

    async def get_device_statistics(self, site_id: str, device_id: str) -> dict:
        url = f"https://{self._host}/proxy/network/integrations/v1/sites/{site_id}/devices/{device_id}/statistics/latest"
        _LOGGER.debug("Fetching device statistics from %s", url)
        headers = {
            "X-API-KEY": self._api_key,
            "Accept": "application/json",
        }

        async with async_timeout.timeout(10):
            async with self._session.get(
                url, headers=headers, ssl=self._ssl_context
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Failed to fetch statistics for device {device_id}: {resp.status}"
                    )
                return await resp.json()

    async def get_clients_paginated(self, site_id, limit=100):
        clients = []
        offset = 0

        while True:
            url = f"https://{self._host}/proxy/network/integrations/v1/sites/{site_id}/clients"
            headers = {"X-API-KEY": self._api_key}
            params = {"limit": limit, "offset": offset}

            async with async_timeout.timeout(10):
                async with self._session.get(
                    url, headers=headers, params=params, ssl=self._ssl_context
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to fetch clients: {resp.status}")
                    data = await resp.json()
                    clients.extend(data.get("data", []))
                    if offset + limit >= data.get("totalCount", 0):
                        break
                    offset += limit

        return clients
