import aiohttp
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed


class DNSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, base_url: str, scan_interval: int):
        self.base_url = base_url

        super().__init__(
            hass,
            logger=None,
            name="dns_orchestration_coordinator",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        url = f"{self.base_url}/system/ip"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"Bad response: {resp.status}")

                    data = await resp.json()

                    # validación mínima
                    if "current_ip" not in data:
                        raise UpdateFailed("Invalid response: missing current_ip")

                    return data

        except Exception as err:
            raise UpdateFailed(f"Connection error: {err}")