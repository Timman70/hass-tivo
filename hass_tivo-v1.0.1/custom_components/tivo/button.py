import logging
import telnetlib3
import asyncio
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PORT = 31339

async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.debug("Setting up TiVo buttons from config entry")
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    favorites = config_entry.options.get("favorites", config_entry.data.get("favorites", []))
    name = config_entry.data["name"]
    host = config_entry.data["host"]

    entities = []
    for i, fav in enumerate(favorites):
        label = fav.get("label")
        channel = fav.get("channel")
        if label and channel:
            index = i + 1
            entities.append(TivoFavoriteButton(name, host, label, channel, index))
    async_add_entities(entities, update_before_add=False)

class TivoFavoriteButton(ButtonEntity):
    def __init__(self, device_name, host, label, channel, index):
        self._attr_name = f"{device_name} - {label}"  # friendly name shown in UI
        self._attr_unique_id = f"{device_name}_fav_{index}".lower()  # stays stable
        self._channel = channel
        self._host = host

    async def async_press(self) -> None:
        try:
            reader, writer = await telnetlib3.open_connection(self._host, PORT)
            for digit in str(self._channel):
                writer.write(f"IRCODE NUM{digit}\r")
                await asyncio.sleep(0.3)
            writer.write("IRCODE ENTER\r")
            await asyncio.sleep(0.3)
            writer.close()
            _LOGGER.info("Channel change sent to %s: %s", self._host, self._channel)
        except Exception as e:
            _LOGGER.error("Failed to send channel to TiVo at %s: %s", self._host, e)
