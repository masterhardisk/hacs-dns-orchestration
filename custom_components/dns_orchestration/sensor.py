from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN
from .coordinator import DNSCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator: DNSCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        DNSPublicIPSensor(coordinator),
    ])


class DNSPublicIPSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DNSCoordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator

    @property
    def name(self):
        return "DNS Public IP"

    @property
    def unique_id(self):
        return "dns_public_ip"

    @property
    def state(self):
        data = self.coordinator.data or {}
        return data.get("current_ip")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
            "last_change": data.get("last_change"),
            "last_change_relative": data.get("last_change_relative"),
        }