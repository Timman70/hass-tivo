
from homeassistant.components.button import ButtonEntity
import logging
import telnetlib3
import asyncio

_LOGGER = logging.getLogger(__name__)
PORT = 31339

async def async_setup_entry(hass, config_entry, async_add_entities):
    name = config_entry.data["name"]
    host = config_entry.data["host"]
    favorites = config_entry.options.get("favorites", config_entry.data.get("favorites", []))

    entities = []
    for fav in favorites:
        label = fav.get("label")
        channel = fav.get("channel")
        if label and channel:
            entities.append(TivoFavoriteButton(name, host, label, channel))

    async_add_entities(entities)

class TivoFavoriteButton(ButtonEntity):
    def __init__(self, device_name, host, label, channel):
        self._attr_name = f"{device_name} - {label}"
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
