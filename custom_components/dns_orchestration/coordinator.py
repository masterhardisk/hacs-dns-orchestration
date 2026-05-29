import aiohttp
from aiohttp import ClientTimeout
from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)


class DNSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, base_url: str, scan_interval: int):
        self.base_url = base_url
        self.session = aiohttp.ClientSession(
            timeout=ClientTimeout(total=10)
        )

        super().__init__(
            hass,
            logger=_LOGGER,
            name="dns_orchestration_coordinator",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        url = f"{self.base_url}/system/ip"

        try:
            async with self.session.get(url) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise UpdateFailed(
                        f"Bad response {resp.status}: {text}"
                    )

                data = await resp.json()

                if not isinstance(data, dict):
                    raise UpdateFailed("Invalid response format")

                if "current_ip" not in data:
                    raise UpdateFailed("Missing current_ip in response")

                return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Client error: {err}")

        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")