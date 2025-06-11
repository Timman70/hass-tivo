import asyncio
import telnetlib3
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PORT = 31339

COMMANDS = {
    "Guide": "IRCODE GUIDE\r",
    "Menu": "IRCODE TIVO\r",
    "Channel Up": "IRCODE CHANNELUP\r",
    "Channel Down": "IRCODE CHANNELDOWN\r"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    host = entry.data.get("host")
    channels = [str(i) for i in range(10)]  # Hardcoded 0-9 channels
    entities = [TiVoCommandButton(host, name, cmd) for name, cmd in COMMANDS.items()]
    entities.append(TiVoChannelSelect(host, channels))
    async_add_entities(entities)

class TiVoCommandButton(ButtonEntity):
    def __init__(self, host, name, command):
        self._host = host
        self._name = f"TiVo {name}"
        self._command = command
        self._attr_name = self._name
        self._attr_unique_id = f"tivo_button_{name.replace(' ', '_').lower()}_{host.replace('.', '_')}"

    async def async_press(self) -> None:
        await self._send_command(self._host, PORT, self._command)

    async def _send_command(self, ip, port, command):
        try:
            _LOGGER.info("Sending command to TiVo: %s", command.strip())
            reader, writer = await telnetlib3.open_connection(ip, port)
            writer.write(command)
            await writer.drain()
            await asyncio.sleep(1)
            writer.close()
        except Exception as e:
            _LOGGER.error("Error sending command to TiVo: %s", e)

class TiVoChannelSelect(SelectEntity):
    def __init__(self, host, channels):
        self._host = host
        self._channels = channels
        self._attr_options = channels
        self._attr_current_option = channels[0]
        self._attr_name = "TiVo Channel Selector"
        self._attr_unique_id = f"tivo_channel_select_{host.replace('.', '_')}"

    async def async_select_option(self, option: str):
        if option not in self._channels:
            _LOGGER.warning("Invalid channel selected: %s", option)
            return
        for digit in option:
            await self._send_command(self._host, PORT, f"IRCODE NUM{digit}\r")
            await asyncio.sleep(0.5)

    async def _send_command(self, ip, port, command):
        try:
            reader, writer = await telnetlib3.open_connection(ip, port)
            writer.write(command)
            await writer.drain()
            writer.close()
        except Exception as e:
            _LOGGER.error("Channel change failed: %s", e)
