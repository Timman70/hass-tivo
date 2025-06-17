
from homeassistant.components.switch import SwitchEntity
import logging
import telnetlib3
import asyncio

_LOGGER = logging.getLogger(__name__)
PORT = 31339

TIVO_COMMANDS = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SELECT', 'TIVO', 'LIVETV', 'THUMBSUP', 'THUMBSDOWN', 'CHANNELUP', 'CHANNELDOWN', 'RECORD', 'DISPLAY', 'DIRECTV', 'NUM0', 'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5', 'NUM6', 'NUM7', 'NUM8', 'NUM9', 'ENTER', 'CLEAR', 'PLAY', 'PAUSE', 'SLOW', 'FORWARD', 'REVERSE', 'STANDBY', 'NOWSHOWING', 'REPLAY', 'ADVANCE', 'DELIMITER', 'GUIDE']

COMMAND_ICONS = {'UP': 'mdi:arrow-up-bold', 'DOWN': 'mdi:arrow-down-bold', 'LEFT': 'mdi:arrow-left-bold', 'RIGHT': 'mdi:arrow-right-bold', 'SELECT': 'mdi:check-bold', 'TIVO': 'mdi:television-classic', 'LIVETV': 'mdi:television-play', 'THUMBSUP': 'mdi:thumb-up', 'THUMBSDOWN': 'mdi:thumb-down', 'CHANNELUP': 'mdi:arrow-up-drop-circle', 'CHANNELDOWN': 'mdi:arrow-down-drop-circle', 'RECORD': 'mdi:record-circle', 'DISPLAY': 'mdi:monitor', 'DIRECTV': 'mdi:satellite-uplink', 'NUM0': 'mdi:numeric-0', 'NUM1': 'mdi:numeric-1', 'NUM2': 'mdi:numeric-2', 'NUM3': 'mdi:numeric-3', 'NUM4': 'mdi:numeric-4', 'NUM5': 'mdi:numeric-5', 'NUM6': 'mdi:numeric-6', 'NUM7': 'mdi:numeric-7', 'NUM8': 'mdi:numeric-8', 'NUM9': 'mdi:numeric-9', 'ENTER': 'mdi:keyboard-return', 'CLEAR': 'mdi:backspace', 'PLAY': 'mdi:play', 'PAUSE': 'mdi:pause', 'SLOW': 'mdi:play-speed', 'FORWARD': 'mdi:fast-forward', 'REVERSE': 'mdi:rewind', 'STANDBY': 'mdi:power-standby', 'NOWSHOWING': 'mdi:playlist-play', 'REPLAY': 'mdi:backup-restore', 'ADVANCE': 'mdi:skip-next', 'DELIMITER': 'mdi:code-string', 'GUIDE': 'mdi:television-guide'}

async def async_setup_entry(hass, config_entry, async_add_entities):
    name = config_entry.data["name"]
    host = config_entry.data["host"]
    entities = [TivoCommandSwitch(name, host, cmd) for cmd in TIVO_COMMANDS]
    async_add_entities(entities)

class TivoCommandSwitch(SwitchEntity):
    def __init__(self, device_name, host, command):
        self._attr_name = f"{device_name} - TiVo {command}"
        self._host = host
        self._command = command
        self._is_on = False
        self._attr_icon = COMMAND_ICONS.get(command, "mdi:remote")

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        try:
            reader, writer = await telnetlib3.open_connection(self._host, PORT)
            writer.write(f"IRCODE {self._command}\r")
            await asyncio.sleep(0.2)
            writer.close()
            _LOGGER.info("Sent IRCODE %s to TiVo at %s", self._command, self._host)
        except Exception as e:
            _LOGGER.error("Failed to send command %s to %s: %s", self._command, self._host, e)

    async def async_turn_off(self, **kwargs):
        self._is_on = False
