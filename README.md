# Awaro

**A plug-and-play LoRaWAN gateway with everything on board.**

8-channel LoRaWAN gateway (ESP32-S3 + Semtech SX1302) with a **local network server**
built in: sensors join directly on the box, payloads are decoded on the box, and clean
data comes out over **MQTT, HTTP webhooks, Home Assistant / Domoticz auto-discovery**
or ThingsBoard — no external server, no cloud required.

🦜 Product page: [awaro.fr](https://awaro.fr)

## What's in this repository

| Directory | Content | License |
|---|---|---|
| [`hardware/`](hardware/) | Schematics (PDF), board images, 3D envelope (STEP) for enclosure integration, mounting / drilling template | CC BY-NC-SA 4.0 |
| [`docs/`](docs/) | User documentation | CC BY-NC-SA 4.0 |
| [`examples/`](examples/) | Integration examples: MQTT / webhook payloads, Home Assistant, Node-RED | MIT |
| [`CHANGELOG.md`](CHANGELOG.md) | Firmware release notes | — |

The gateway **firmware is proprietary** and not part of this repository.
Payload decoders are shared through the open
[lorawan2mqtt codec database](https://github.com/Di-Ny/lorawan2mqtt) (MIT) — codecs
import directly into the gateway's web interface, and contributions benefit every user.

## Licenses

- **Hardware plans & documentation** — [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/):
  share and adapt with attribution, **non-commercial use only**, derivatives under the
  same license. For commercial licensing, contact us via [awaro.fr](https://awaro.fr).
- **Examples** — [MIT](examples/LICENSE): use them anywhere, including commercially.
- **Awaro** name, logo and mascot are trademarks and are **not** covered by any of the
  licenses above.
