# Integration examples

License: [MIT](LICENSE) — use freely, including commercially.

Coming here:

- `payloads/` — sample JSON messages as published by the gateway (MQTT uplink,
  HTTP webhook, decoded fields, replay frames)
- `home-assistant/` — MQTT Auto Discovery walkthrough (works with Home Assistant
  and Domoticz)
- `node-red/` — example flows consuming the gateway's MQTT output

Payload decoders live in the community
[lorawan2mqtt codec database](https://github.com/Di-Ny/lorawan2mqtt) and import
directly into the gateway (Decoders tab → *Import a file*).
