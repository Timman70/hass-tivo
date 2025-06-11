import asyncio
import telnetlib3
import logging
import os
import yaml

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PORT = 31339

# Created by timcloud

CONTROL_COMMANDS = {
    "Guide": "IRCODE GUIDE",
    "Record": "IRCODE RECORD",
    "Play": "IRCODE PLAY",
    "Pause": "IRCODE PAUSE",
    "Channel Up": "IRCODE CHANNELUP",
    "Channel Down": "IRCODE CHANNELDOWN",
    "Clear": "IRCODE CLEAR",
    "Standby": "IRCODE STANDBY",
    "Select": "IRCODE SELECT",
    "Central": "IRCODE TIVO",
    "Up": "IRCODE UP",
    "Down": "IRCODE DOWN",
    "Left": "IRCODE LEFT",
    "Right": "IRCODE RIGHT",
    "Live TV": "IRCODE LIVETV",
    "My Shows": "IRCODE NOWSHOWING",
    "Stop": "IRCODE STOP"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    host = entry.data.get("host")
    favorites_path = os.path.join(os.path.dirname(__file__), "favorites.yaml")
    if not os.path.exists(favorites_path):
        _LOGGER.warning("No favorites.yaml file found.")
        return

    import functools
    def load_favorites(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)
    favorites = await hass.async_add_executor_job(functools.partial(load_favorites, favorites_path))

    switches = []
    for channel, data in favorites.items():
        if isinstance(data, dict):
            name = data.get("name", channel)
            picture = data.get("icon", None)
        else:
            name = data
            picture = None
        switches.append(TiVoFavoriteChannelSwitch(host, channel, name, picture))

    for name, command in CONTROL_COMMANDS.items():
        switches.append(TiVoCommandSwitch(host, name, command))

    async_add_entities(switches)

class TiVoFavoriteChannelSwitch(SwitchEntity):
    def __init__(self, host, channel, name, entity_picture):
        self._host = host
        self._channel = str(channel)
        self._name = f"TiVo {name}"
        self._is_on = False
        self._attr_unique_id = f"tivo_switch_{name.lower().replace(' ', '_')}"
        self._attr_name = self._name
        self._attr_entity_picture = entity_picture if entity_picture else None

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()

        try:
            reader, writer = await telnetlib3.open_connection(self._host, PORT)
            for digit in self._channel:
                command = "IRCODE NUM" + digit + "\r"
                writer.write(command)
                await writer.drain()
                await asyncio.sleep(0.03)
            writer.close()
        except Exception as e:
            _LOGGER.error("Persistent connection failed: %s", e)

        await asyncio.sleep(2)
        self._is_on = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

class TiVoCommandSwitch(SwitchEntity):
    def __init__(self, host, name, command):
        self._host = host
        self._command = command
        self._name = f"TiVo {name}"
        self._is_on = False
        self._attr_unique_id = f"tivo_command_{name.lower().replace(' ', '_')}"
        self._attr_name = self._name

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()
        await self._send_command(self._host, PORT, self._command + "\r")
        await asyncio.sleep(1)
        self._is_on = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

    async def _send_command(self, ip, port, command):
        try:
            reader, writer = await telnetlib3.open_connection(ip, port)
            writer.write(command)
            await writer.drain()
            writer.close()
        except Exception as e:
            _LOGGER.error("Command switch failed: %s", e)
