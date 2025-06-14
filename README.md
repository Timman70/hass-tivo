# Hass-TiVo Integration

A custom Home Assistant integration to control TiVo devices via telnet, with support for customizable favorite channel buttons.

## 🚀 Features

- Control your TiVo using button entities in Home Assistant
- Define up to 20 favorite channels
- Clean integration with the Home Assistant UI

## 📦 Installation

1. Download the latest [release ZIP]([https://github.com/Timman70/hass-tivo/releases](https://github.com/Timman70/hass-tivo/blob/main/tivo_v0.1.zip) or clone this repo into your Home Assistant `custom_components` directory:

```bash
cd config/custom_components
git clone https://github.com/Timman70/hass-tivo
```

2. Restart Home Assistant.

3. Go to **Settings → Devices & Services → Add Integration**, search for **TiVo**, and configure your device:
   - Enter the device name and IP address
   - Set up to 20 favorite channels by name and channel number

## 🔘 Button Entities

Each favorite channel is exposed as a `button` entity like:

```
button.living_room_espn
button.master_bedroom_abc
```

You can use these in dashboards, scripts, or automations to tune to specific channels.

> **Note:** Entities now support unique IDs and can be renamed or disabled in the UI.

## 🧰 Requirements

- A TiVo device with network access and port `31339` open for telnet control
- Home Assistant 2023.5+ recommended

## 📎 Example Automation

```yaml
alias: Watch ESPN
trigger:
  - platform: state
    entity_id: input_boolean.watch_espn
    to: "on"
action:
  - service: button.press
    target:
      entity_id: button.living_room_espn
```

## 👨‍💻 Author

Maintained by [Timman70](https://github.com/Timman70)
