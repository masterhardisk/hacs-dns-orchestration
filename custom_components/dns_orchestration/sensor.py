from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[entry.domain][entry.entry_id]

    entities = [
        DNSPublicIPSensor(coordinator),
        DNSLastChangeSensor(coordinator),
        DNSLastChangeAgeSensor(coordinator),
        DNSIPChangedRecentlyBinarySensor(coordinator),
    ]

    async_add_entities(entities)


class DNSPublicIPSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "DNS Public IP"
    _attr_unique_id = "dns_public_ip"

    @property
    def state(self):
        return self.coordinator.data.get("current_ip")


class DNSLastChangeSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "DNS Last Change"
    _attr_unique_id = "dns_last_change"

    @property
    def state(self):
        return self.coordinator.data.get("last_change")


class DNSLastChangeAgeSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "DNS Last Change Age"
    _attr_unique_id = "dns_last_change_age"

    @property
    def state(self):
        return self.coordinator.data.get("last_change_relative")


class DNSIPChangedRecentlyBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "DNS IP Changed Recently"
    _attr_unique_id = "dns_ip_changed_recently"

    @property
    def is_on(self):
        value = self.coordinator.data.get("last_change_relative", 999999)
        return value < 3600