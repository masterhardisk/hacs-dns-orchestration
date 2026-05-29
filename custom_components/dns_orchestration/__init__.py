from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .coordinator import DNSCoordinator

DOMAIN = "dns_orchestration"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    base_url = entry.data["base_url"].rstrip("/")
    scan_interval = entry.data.get("scan_interval", 30)

    coordinator = DNSCoordinator(hass, base_url, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok