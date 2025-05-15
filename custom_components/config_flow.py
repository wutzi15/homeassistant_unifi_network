import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_HOST, CONF_API_KEY, CONF_SITE_ID, CONF_SITE_NAME
from .unifi_api import UnifiAPI
import logging

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_API_KEY): str,
    }
)


class UnifiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Unifi."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.host = user_input[CONF_HOST]
            self.api_key = user_input[CONF_API_KEY]

            api = UnifiAPI(host=self.host, api_key=self.api_key, hass=self.hass)
            sites = await api.get_sites()
            if not sites:
                errors["base"] = "cannot_connect"
            else:
                self.sites = sites
                return await self.async_step_site()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_site(self, user_input=None):
        errors = {}

        site_options = {site["id"]: site["name"] for site in self.sites}
        site_schema = vol.Schema({vol.Required(CONF_SITE_ID): vol.In(site_options)})

        if user_input is not None:
            site_id = user_input[CONF_SITE_ID]
            site_name = next(
                (s["name"] for s in self.sites if s["id"] == site_id), site_id
            )

            return self.async_create_entry(
                title=f"UniFi Site: {site_name}",
                data={
                    CONF_HOST: self.host,
                    CONF_API_KEY: self.api_key,
                    CONF_SITE_ID: site_id,
                    CONF_SITE_NAME: site_name,
                },
            )

        return self.async_show_form(
            step_id="site",
            data_schema=site_schema,
            errors=errors,
        )
