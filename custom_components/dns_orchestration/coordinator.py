from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.helpers.dispatcher import async_dispatcher_send
import logging
from datetime import timedelta
import aiohttp

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
        ip_url = f"{self.base_url}/api/system/ip"
        records_url = f"{self.base_url}/api/records"

        timeout = aiohttp.ClientTimeout(total=10)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:

                # -------------------------
                # IP
                # -------------------------
                async with session.get(ip_url) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        raise UpdateFailed(f"Bad IP response {resp.status}: {text}")

                    ip_data = await resp.json()

                    if not isinstance(ip_data, dict):
                        raise UpdateFailed("Invalid IP response format")

                    ip = ip_data.get("current_ip")
                    if not ip:
                        raise UpdateFailed("Missing current_ip in response")

                # -------------------------
                # RECORDS
                # -------------------------
                async with session.get(records_url) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        raise UpdateFailed(f"Bad records response {resp.status}: {text}")

                    records = await resp.json()

                    if not isinstance(records, list):
                        raise UpdateFailed("Invalid records response format")

                # -------------------------
                # IP CHANGE DETECTION
                # -------------------------
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
                            "raw": ip_data,
                        },
                    )

                self._last_ip = ip

                # -------------------------
                # RECORDS METRICS
                # -------------------------
                total = len(records)

                ok = sum(
                    1 for r in records
                    if r.get("status") in ("ok", "up_to_date")
                )

                pending = sum(
                    1 for r in records
                    if r.get("status") == "pending"
                )

                error = sum(
                    1 for r in records
                    if r.get("status") == "error"
                )

                # -------------------------
                # RETURN DATA (STATE)
                # -------------------------
                return {
                    # IP
                    "current_ip": ip,
                    "last_change": ip_data.get("last_change"),
                    "last_change_relative": ip_data.get("last_change_relative"),

                    # RECORDS
                    "records_total": total,
                    "records_ok": ok,
                    "records_pending": pending,
                    "records_error": error,
                }

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Client error: {err}")

        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")