# hass-tivo-telnet
Home Assistant custom component for TiVo Telnet control
# TiVo Telnet Integration

Control your TiVo (e.g. UHD51A, Bolt, Mini, etc.) over your local network using Telnet commands. Supports IR remote commands, channel favorites, and custom logos.

> Created by **timcloud**

---

## 📦 Features

- Control via Home Assistant switches
- Channel up/down, guide, pause, play, etc.
- Favorite channels as switches
- Channel logos via `entity_picture`
- Telnet-based — no official TiVo API required
- HACS-compatible

---

## ⚙️ Installation (HACS)

1. Copy or upload this folder to:  
   ```
   /config/custom_components/tivo/
   ```

2. OR add the GitHub repo as a custom HACS repository.

3. Restart Home Assistant.

4. Go to **Settings > Devices & Services > Add Integration**  
   Search for **TiVo Telnet**.

---

## 📡 Enabling TiVo Remote Network Control

You must enable **network remote control** on your TiVo:

1. On your TiVo remote:
   - Press: `TiVo → Settings → Network Settings → Remote Network Access`
   - Enable **Allow Network Remote Control**

2. Note your TiVo IP address. Use this during setup.

3. Port **31339** must be open on your local network.

---

## 🧠 Configuration

### 📁 `favorites.yaml` (in `custom_components/tivo/`)

Define your favorite channels and (optionally) custom icons:

```yaml
531:
  name: "ION"
  icon: "/local/ion.png"

204:
  name: "ESPN"
  icon: "/local/espn.png"
```

> Place images in `/config/www/`, then access via `/local/`.

---

## 🖼 Icon Support

Use any image file (PNG, JPG, SVG). Make sure the path looks like:

```yaml
icon: "/local/mychannel.png"
```

---

## 🛠 Supported Commands

Switches will be created for:

- Guide, Play, Pause, Stop
- Channel Up / Down
- Live TV, My Shows
- Arrows, Select, Clear, Tivo (central)

---

## 🙌 Credits

Created and maintained by **timcloud**  
Based on community feedback and real-world TiVo reverse-engineering.
