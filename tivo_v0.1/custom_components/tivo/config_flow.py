import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Prevent duplicate IP addresses
            for entry in self._async_current_entries():
                if entry.data.get("host") == user_input["host"]:
                    return self.async_abort(reason="already_configured")

            favorites = []
            for i in range(1, 21):
                label = user_input.get(f"fav_label_{i}", "").strip()
                channel = user_input.get(f"fav_channel_{i}", "").strip()
                if label and channel:
                    favorites.append({"label": label, "channel": channel})

            return self.async_create_entry(
                title=user_input["name"],
                data={
                    "name": user_input["name"],
                    "host": user_input["host"]
                },
                options={
                    "favorites": favorites
                }
            )

        schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("host"): str,
            # Users can customize these favorite channel names and numbers during setup
# Each label (name) and channel number will be shown as a button
vol.Optional("fav_label_1", default="Channel1"): str,
            vol.Optional("fav_channel_1", default="101"): str,
            vol.Optional("fav_label_2", default="Channel2"): str,
            vol.Optional("fav_channel_2", default="102"): str,
            vol.Optional("fav_label_3", default="Channel3"): str,
            vol.Optional("fav_channel_3", default="103"): str,
            vol.Optional("fav_label_4", default="Channel4"): str,
            vol.Optional("fav_channel_4", default="104"): str,
            vol.Optional("fav_label_5", default="Channel5"): str,
            vol.Optional("fav_channel_5", default="105"): str,
            vol.Optional("fav_label_6", default="Channel6"): str,
            vol.Optional("fav_channel_6", default="106"): str,
            vol.Optional("fav_label_7", default="Channel7"): str,
            vol.Optional("fav_channel_7", default="107"): str,
            vol.Optional("fav_label_8", default="Channel8"): str,
            vol.Optional("fav_channel_8", default="108"): str,
            vol.Optional("fav_label_9", default="Channel9"): str,
            vol.Optional("fav_channel_9", default="109"): str,
            vol.Optional("fav_label_10", default="Channel10"): str,
            vol.Optional("fav_channel_10", default="110"): str,
            vol.Optional("fav_label_11", default="Channel11"): str,
            vol.Optional("fav_channel_11", default="111"): str,
            vol.Optional("fav_label_12", default="Channel12"): str,
            vol.Optional("fav_channel_12", default="112"): str,
            vol.Optional("fav_label_13", default="Channel13"): str,
            vol.Optional("fav_channel_13", default="113"): str,
            vol.Optional("fav_label_14", default="Channel14"): str,
            vol.Optional("fav_channel_14", default="114"): str,
            vol.Optional("fav_label_15", default="Channel15"): str,
            vol.Optional("fav_channel_15", default="115"): str,
            vol.Optional("fav_label_16", default="Channel16"): str,
            vol.Optional("fav_channel_16", default="116"): str,
            vol.Optional("fav_label_17", default="Channel17"): str,
            vol.Optional("fav_channel_17", default="117"): str,
            vol.Optional("fav_label_18", default="Channel18"): str,
            vol.Optional("fav_channel_18", default="118"): str,
            vol.Optional("fav_label_19", default="Channel19"): str,
            vol.Optional("fav_channel_19", default="119"): str,
            vol.Optional("fav_label_20", default="Channel20"): str,
            vol.Optional("fav_channel_20", default="120"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)


    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        favorites = self.config_entry.options.get("favorites", self.config_entry.data.get("favorites", []))

        schema_dict = {}
        for i in range(1, 21):
            fav = favorites[i - 1] if i - 1 < len(favorites) else {}
            label = fav.get("label", f"Channel{i}")
            channel = fav.get("channel", f"{100 + i}")
            schema_dict[vol.Optional(f"fav_label_{i}", default=label)] = str
            schema_dict[vol.Optional(f"fav_channel_{i}", default=channel)] = str

        if user_input is not None:
            new_favorites = []
            for i in range(1, 21):
                label = user_input.get(f"fav_label_{i}", "").strip()
                channel = user_input.get(f"fav_channel_{i}", "").strip()
                if label and channel:
                    new_favorites.append({"label": label, "channel": channel})
            return self.async_create_entry(title="", data={"favorites": new_favorites})

        return self.async_show_form(step_id="init", data_schema=vol.Schema(schema_dict))
