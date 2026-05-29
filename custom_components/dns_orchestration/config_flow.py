import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "dns_orchestration"


class DNSOrchestrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            base_url = user_input["base_url"].rstrip("/")

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{base_url}/api/ha/state",
                        timeout=10,
                    ) as resp:
                        if resp.status != 200:
                            errors["base_url"] = "cannot_connect"
                        else:
                            data = await resp.json()
                            if not isinstance(data, dict):
                                errors["base_url"] = "invalid_response"
            except Exception:
                errors["base_url"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(
                    title="DNS Orchestration",
                    data={
                        "base_url": base_url,
                        "scan_interval": user_input.get("scan_interval", 30),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("base_url", default="http://localhost:8010"): str,
                    vol.Optional("scan_interval", default=30): int,
                }
            ),
            errors=errors,
        )