# Changelog

Gateway firmware — user-facing changes. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
The firmware itself is proprietary; this file documents what each update brings.

## [3.5.3]

- Simpler Matter pairing: the gateway now draws its QR code right in its web page (Pairing button) - no more copying the code by hand.
- Each gateway now has its own pairing identifier and its own name, so several of them can live on the same network and be told apart in the app (Apple Home, Google Home...).
- The short address (awaro-XXXXXX.local) also answers from the very first power-up, while the box is still its own WiFi access point.
- On protected models, the sensor registry is encrypted like the rest of the memory.
- The configuration page opens noticeably faster (it is now compressed: about four times less data to download), and the gateway reboots in seconds instead of about thirty when supervision has not been configured yet.
- Finally, in home-automation apps the gateway now shows its real name (Awaro LT or Awaro Pro, by Furgo) instead of a generic one.

## [3.5.2]

- The gateway’s identity card on the supervisor (firmware version, IP address, WiFi network…) now refreshes regularly instead of only at connection time: after an update or a network change, the dashboard immediately reflects reality.

## [3.5.1]

- Memory overhaul, part two: another ~18 KB of internal memory freed on every model (concentrator verification buffer released after start-up, unused transmit queue removed), leaving more headroom for integrations and updates.

## [3.5.0]

- Major internal memory overhaul: the gateway keeps much more free memory while running, even with several integrations active at once — no more slowdowns or refused connections when everything is enabled.
- Two integrations pointing at the same MQTT server now share a single connection instead of opening two.
- Groundwork for the Matter bridge on compatible models: LoRaWAN sensors will be able to appear directly in Apple Home, Home Assistant or Google Home (activation to come).

## [3.4.4]

- The built-in server now adjusts sensor radio data rates on its own (ADR): a sensor stuck at a slow rate — for instance after a gateway power outage — is automatically brought back to its optimal rate within minutes, no action needed.
- The built-in server page now displays reliably even after days of uptime (blank-window issue fixed).
- Every click now gives visual feedback: a "Saved" confirmation and a busy animation on buttons (update check, WiFi scan, network tests).

## [3.4.1]

- More sensors recognised: the Dragino range grows (PS-LB pressure probe, plus the SN50v3 measurement modes that were still missing).
- Readings from these sensors now arrive decoded, with their units, with nothing to configure.

## [3.4.0]

- Many more sensors recognised: 36 built-in decoders covering Milesight (the whole range), Elsys, Seeed SenseCAP — including the 8-in-1 weather station —, Browan/Tabs, the MClimate Vicki radiator valve and some forty Dragino references (door, leak, distance, soil, pH, LiDAR, radar, tilt, pressure, I/O controller).
- Just pick the model from the sensor's list, with no configuration at all; the list is now grouped by brand.
- More reliable integrations: messages sent to integrations can no longer be truncated, every reading of a sensor now shows up in Home Assistant (some could remain invisible), and the packet log displays and exports all decoded values.
- Hardened security: the published software no longer contains any credential — the supervision key and the update password are per-gateway (installed at the workshop), and the update channel now supports per-device authentication (HTTP Digest, the password never travels in clear text).

## [3.3.11]

- Embedded LoRaWAN server: catch-up after an Internet outage — readings received during an outage are automatically re-delivered to the integrations (MQTT, webhook, ThingsBoard) once the network is back, with their original timestamps (requires history enabled on the sensor; PSRAM gateways).
- The Integrations screen now shows a sample of the message sent for the chosen type, and the status shows how many readings are pending catch-up.
- Unified supervision whichever channel is used, uptime shown in days/hours.

## [3.3.10]

- More reliable updates: every image is signed and verified by the gateway before installing, the download is lighter (works on memory-tight V1 gateways too) and the install happens at reboot, when memory is available.

## [3.3.7]

- Boot-mode choice made reliable: "Next boot: access point" is now always honoured, and a power cut in the first seconds of a boot can no longer make the box restart as a surprise access point (the WiFi fallback is only recorded at the moment it actually fires).

## [3.3.6]

- Embedded LoRaWAN server, reworked Integrations screen: editing an integration now restores every field (username pre-filled, password shown as "set", server address without duplicated mqtt://), the ThingsBoard integration is now called FurgoSuperviseur, the Groups field explains itself on hover, and every on-the-fly change (decoder, class, history) is confirmed with a "Saved ✓" toast.
- Post-configuration reboot countdown shortened (5 s).

## [3.3.5]

- Refined ADR: the data-rate target is computed from the join's actual signal margin (a nearby sensor is brought back to SF7 even if it joined at SF12), and a manual command recalibrates a sensor on demand (lns adr / API action=adr).

## [3.3.4]

- More reliable ADR: the data-rate command is repeated (up to 4 times) until the sensor applies it, and its format is now compatible with LoRaWAN 1.0.2/1.0.3 sensors (Dragino…) that silently rejected the previous one.
- Recent-packets timestamps now show milliseconds.

## [3.3.3]

- Embedded LoRaWAN server: simplified ADR — at join time the box assigns the sensor the data rate proven by the join (with a safety margin): nearby sensors no longer stay stuck at SF12 (30× more airtime).
- Fixed the right-button (3 s) remote diagnostics: the press used to reboot the box instead of opening the tunnel.

## [3.3.2]

- Embedded LoRaWAN server: the SF (spreading factor) of every frame is now shown in Recent packets, exported in the CSV history and published to the integrations (webhook, MQTT, ThingsBoard, Home Assistant).
- The "NS stats period" setting is honoured again (it used to be clobbered by the 30 s default).

## [3.3.1]

- Embedded LoRaWAN server: more reliable join — devices coming from another network (e.g. ChirpStack) are accepted right away, a device that lost its anti-replay counter re-joins on its own within a minute, and the join reply leaves on the correct channel even with a device very close to the box.
- More reliable updates: version list remembered (no re-check needed after a reboot), failed installs resume automatically at next boot, automatic updates apply right at boot, Unblock button for the anti-brick protection.
- WiFi gauge recalibrated.

## [3.3.0]

- Hardened security: web interface hardened (sanitised inputs), improved LoRaWAN anti-replay, serial console protected by a code, quieter serial output by default.
- Vendor supervision is now opt-in: it only starts when a token is configured.
- Right button: a long press (3 s, LED-confirmed) toggles remote diagnostics; a short press switches to WiFi setup mode on release.

## [3.2.8]

- Built-in LoRaWAN server: per-sensor packet history — Off / 100 / 1000-row selector in the sensor table, CSV download, with a free-PSRAM check before enabling.
- Off by default; PSRAM gateways only.

## [3.2.7]

- V1 gateways: secure-connection memory handling fully reworked — checks and updates work normally again.

## [3.2.6]

- V1 gateways: first memory optimisation step.

## [3.2.5]

- During an update, the LEDs now show a calm, readable progress bar (no more fast blinking).

## [3.2.4]

- The embedded LoRaWAN server is now also visible in simplified setup mode.

## [3.2.3]

- Adjustable network-server report rate, reduced data usage, release notes shown here, local access name (awaro-xxxx.local) displayed, interface refinements.

## [3.2.2]

- New visual gauges for the gateway state (memory, storage, WiFi quality).

## [3.2.1]

- Per-sensor measurement history, viewable and downloadable (CSV file).
- Support for immediate-command actuators.
- More robust updates.

## [3.2.0]

- Modernised software base, paving the way for upcoming gateway models.
- Your sensors and settings are preserved.

## [3.1.2]

- Richer supervision for better remote monitoring of your gateway.

## [3.1.1]

- Fix: some readings (e.g. battery level) could fail to appear in Domoticz / Home Assistant.

## [3.1.0]

- Per-sensor measurement history and extended embedded-server capacity.

## [3.0.1]

- Improved performance and stability, more reliable updates.

## [3.0.0]

- Modernised software base.
- Your sensors and settings are preserved through the update.

## [1.5.12]

- Stability improvements for remote supervision.

## [1.5.9]

- Support for immediate-command actuators (valves, relays...).

## [1.5.8]

- Internal optimisations and more stable integrations.
