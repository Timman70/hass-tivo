# Hass-TiVo Integration

A custom Home Assistant integration to control TiVo devices via telnet, with support for customizable favorite channel buttons.

## 🚀 Features

- Control your TiVo using button and switch entities in Home Assistant
- Define up to 20 favorite channels
- Clean integration with the Home Assistant UI

## 📡 Enable TiVo Remote Control

Before using this integration, you must enable remote access on your TiVo:

1. On your TiVo remote, press the **TiVo** button  
2. Navigate to **Settings & Messages → Settings → Network → View Network Details**  
3. Ensure **Allow Network Remote Control** is set to **Yes**  
4. Note the IP address shown here for use during integration setup  

Once done, continue below:

## 📦 Installation

1. Download the latest release ZIP or clone this repo into your Home Assistant `custom_components` directory:

```bash
cd config/custom_components
git clone https://github.com/Timman70/hass-tivo
```

2. Restart Home Assistant

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

## 🧲 Switch Entities

Common TiVo commands (like UP, PLAY, GUIDE, etc.) are exposed as `switch` entities, such as:

```
switch.living_room_up
switch.living_room_guide
```

They send commands via telnet to your TiVo when toggled on.

## ✏️ Edit Channels Anytime

To change channel names or numbers after setup:

1. Go to **Settings > Devices & Services**
2. Find the **TiVo integration**
3. Click **⋯ > Configure**
4. Update your favorite channel labels and numbers
5. Click **Submit**

> After submitting, **click ⋯ > Reload** to apply the changes and update the entities in the UI.

Each channel is exposed as a **button entity** (e.g., `button.officetivo_hbo`) that sends the new channel number to the TiVo when pressed.

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
