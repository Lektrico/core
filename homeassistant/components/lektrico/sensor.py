"""Support for Lektrico charging station sensors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_FRIENDLY_NAME,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    POWER_KILO_WATT,
    TEMP_CELSIUS,
    TIME_SECONDS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import LektricoDeviceDataUpdateCoordinator
from .const import DOMAIN


@dataclass
class LektricoSensorEntityDescription(SensorEntityDescription):
    """A class that describes the Lektrico sensor entities."""

    @classmethod
    def get_native_value(cls, data: Any) -> float | str | int | None:
        """Return None."""
        return None


@dataclass
class ChargerStateSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Charger State sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> str:
        """Get the charger_state."""
        return str(data.charger_state)


@dataclass
class ChargingTimeSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Charging Time sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> int:
        """Get the charging_time."""
        return int(data.charging_time)


@dataclass
class CurrentSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Current sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> float:
        """Get the current."""
        return float(data.current)


@dataclass
class InstantPowerSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Instant Power sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> float:
        """Get the instant_power."""
        return float(data.instant_power)


@dataclass
class SessionEnergySensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Session Energy sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> float:
        """Get the session_energy."""
        return float(data.session_energy)


@dataclass
class TemperatureSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Temperature sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> float:
        """Get the temperature."""
        return float(data.temperature)


@dataclass
class TotalChargedEnergySensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Total Charged Energy sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> int:
        """Get the total_charged_energy."""
        return int(data.total_charged_energy)


@dataclass
class VoltageSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Voltage sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> float:
        """Get the voltage."""
        return float(data.voltage)


@dataclass
class InstallCurrentSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Install Current sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> int:
        """Get the install_current."""
        return int(data.install_current)


@dataclass
class DynamicCurrentSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Dynamic Current sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> int:
        """Get the dynamic_current."""
        return int(data.dynamic_current)


@dataclass
class LedMaxBrightnessSensorEntityDescription(LektricoSensorEntityDescription):
    """A class that describes the Lektrico Led Max Brightness sensor entity."""

    @classmethod
    def get_native_value(cls, data: Any) -> int:
        """Get the led_max_brightness."""
        return int(data.led_max_brightness)


SENSORS: tuple[LektricoSensorEntityDescription, ...] = (
    ChargerStateSensorEntityDescription(
        key="charger_state",
        name="Charger state",
    ),
    ChargingTimeSensorEntityDescription(
        key="charging_time",
        name="Charging time",
        native_unit_of_measurement=TIME_SECONDS,
    ),
    CurrentSensorEntityDescription(
        key="current",
        name="Current",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
    ),
    InstantPowerSensorEntityDescription(
        key="instant_power",
        name="Instant power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=POWER_KILO_WATT,
    ),
    SessionEnergySensorEntityDescription(
        key="session_energy",
        name="Session energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    TemperatureSensorEntityDescription(
        key="temperature",
        name="Temperature",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    TotalChargedEnergySensorEntityDescription(
        key="total_charged_energy",
        name="Total charged energy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    VoltageSensorEntityDescription(
        key="voltage",
        name="Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
    InstallCurrentSensorEntityDescription(
        key="install_current",
        name="Install current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lektrico charger based on a config entry."""
    coordinator: LektricoDeviceDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        LektricoSensor(
            description,
            coordinator,
            entry.data[CONF_FRIENDLY_NAME],
        )
        for description in SENSORS
    )


class LektricoSensor(CoordinatorEntity, SensorEntity):
    """The entity class for Lektrico charging stations sensors."""

    entity_description: LektricoSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        description: LektricoSensorEntityDescription,
        coordinator: LektricoDeviceDataUpdateCoordinator,
        friendly_name: str,
    ) -> None:
        """Initialize Lektrico charger."""
        super().__init__(coordinator)
        self.entity_description = description

        self._attr_unique_id = f"{coordinator.serial_number}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.serial_number)},
            model=f"1P7K {coordinator.serial_number} rev.{coordinator.board_revision}",
            name=friendly_name,
            manufacturer="Lektrico",
            sw_version=coordinator.data.fw_version,
        )

    @property
    def native_value(self) -> float | str | int | None:
        """Return the state of the sensor."""
        return self.entity_description.get_native_value(self.coordinator.data)
