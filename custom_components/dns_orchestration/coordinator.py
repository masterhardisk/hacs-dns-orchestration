import logging
from datetime import timedelta

import aiohttp

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.dispatcher import async_dispatcher_send

_LOGGER = logging.getLogger(__name__)

SIGNAL_IP_CHANGED = "dns_orchestration_ip_changed"


class DNSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, base_url: str, scan_interval: int):
        self.base_url = base_url.rstrip("/")
        self._last_ip = None

        super().__init__(
            hass,
            logger=_LOGGER,
            name="dns_orchestration_coordinator",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        url = f"{self.base_url}/api/system/ip"

        timeout = aiohttp.ClientTimeout(total=10)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:

                    if resp.status != 200:
                        text = await resp.text()
                        raise UpdateFailed(f"Bad response {resp.status}: {text}")

                    data = await resp.json()

                    if not isinstance(data, dict):
                        raise UpdateFailed("Invalid response format")

                    ip = data.get("current_ip")

                    if not ip:
                        raise UpdateFailed("Missing current_ip in response")

                    # 🔥 DETECCIÓN DE CAMBIO DE IP
                    if self._last_ip and self._last_ip != ip:
                        _LOGGER.info(
                            "DNS IP changed: %s -> %s",
                            self._last_ip,
                            ip,
                        )

                        async_dispatcher_send(
                            self.hass,
                            SIGNAL_IP_CHANGED,
                            {
                                "old_ip": self._last_ip,
                                "new_ip": ip,
                                "raw": data,
                            },
                        )

                    self._last_ip = ip

                    return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Client error: {err}")

        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")