from .coordinator import UnifiCoordinator, UnifiClientCoordinator
from .unifi_api import UnifiAPI
from .const import CONF_HOST, CONF_API_KEY, CONF_SITE_ID
from homeassistant.helpers.entity import Entity


# Import sensor classes
from .sensors.device_info import UniFiDeviceSensor
from .sensors.cpu_usage import UniFiDeviceCPUSensor
from .sensors.memory_usage import UniFiMemoryUsageSensor
from .sensors.load_average import UniFiLoadAverageSensor
from .sensors.uptime import UniFiUptimeSensor
from .sensors.heartbeat import UniFiLastHeartbeatSensor, UniFiNextHeartbeatSensor
from .sensors.data_rate import UniFiTxRateSensor, UniFiRxRateSensor
from .sensors.radio import UniFiRadioRetrySensor
from .sensors.client import UniFiClientSensor
from .sensors.ip_address import UniFiIpAddressSensor
from .sensors.connected_at import UniFiConnectedAtSensor
from .sensors.access_type import UniFiAccessTypeSensor
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    host = config_entry.data[CONF_HOST]
    api_key = config_entry.data[CONF_API_KEY]
    site_id = config_entry.data[CONF_SITE_ID]

    api = UnifiAPI(host, api_key, hass)
    await api.async_initialize()

    coordinator = UnifiCoordinator(hass, api, site_id)
    await coordinator.async_config_entry_first_refresh()

    client_coordinator = UnifiClientCoordinator(hass, api, site_id)
    await client_coordinator.async_config_entry_first_refresh()

    entities = []
    for device_id in coordinator.data:
        entities.append(UniFiDeviceSensor(coordinator, device_id))
        entities.append(UniFiDeviceCPUSensor(coordinator, device_id))
        entities.append(UniFiMemoryUsageSensor(coordinator, device_id))
        entities.append(
            UniFiLoadAverageSensor(coordinator, device_id, "loadAverage1Min", "1m")
        )
        entities.append(
            UniFiLoadAverageSensor(coordinator, device_id, "loadAverage5Min", "5m")
        )
        entities.append(
            UniFiLoadAverageSensor(coordinator, device_id, "loadAverage15Min", "15m")
        )
        entities.append(UniFiUptimeSensor(coordinator, device_id))
        entities.append(UniFiLastHeartbeatSensor(coordinator, device_id))
        entities.append(UniFiNextHeartbeatSensor(coordinator, device_id))
        entities.append(UniFiTxRateSensor(coordinator, device_id))
        entities.append(UniFiRxRateSensor(coordinator, device_id))

        for freq in (2.4, 5, 6):
            entities.append(UniFiRadioRetrySensor(coordinator, device_id, freq))

    for client_id in client_coordinator.data:
        entities.append(UniFiClientSensor(client_coordinator, client_id))
        entities.append(UniFiIpAddressSensor(client_coordinator, client_id))
        entities.append(UniFiConnectedAtSensor(client_coordinator, client_id))
        entities.append(UniFiAccessTypeSensor(client_coordinator, client_id))

    async_add_entities(entities)


class UniFiSiteSensor(Entity):
    def __init__(self, site_id):
        self._site_id = site_id

    @property
    def name(self):
        return "UniFi Site Sensor"

    @property
    def state(self):
        return self._site_id
