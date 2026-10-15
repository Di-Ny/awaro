# Changelog

Gateway firmware — user-facing changes. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
The firmware itself is proprietary; this file documents what each update brings.

## [3.6.3]

- Wi-Fi: a box already in service no longer falls back to access-point mode on its own when its network disappears; it keeps retrying and reconnects as soon as the network is back (the automatic access point is now only for installation, or after a short press on the button).
- New backup Wi-Fi, for example a 4G dongle, used only when the main network has had no connection or no Internet for 3 minutes, with automatic return to the main one; the box picks the strongest access point and its integrations reconnect as soon as the network is back.
- Remote access: a network drop during a session no longer reboots the box.
- Built-in LoRaWAN server: data-rate adaptation no longer slows a sensor down for a single badly received frame and never asks for a data rate the radio plan forbids (on AU915, sensors sent to SF11 stayed silent until restarted).
- FurgoNode: the GSM RSSI is published as gsm_rssi and no longer overwrites the radio RSSI.
- Decoders: u24l type (3 swapped bytes) in the builder; a decoder too long for the page is refused with a message instead of being cut; importing a configuration counts the decoders it adds.

## [3.6.2]

- Built-in LoRaWAN server page: an integration address keeps the prefix you type (wss://, mqtts://, https://...).
- The mqtt:// or http:// shown in front of the Server field is now only a hint, which disappears as soon as a prefix is typed, and the edit button keeps the full address: a wss:// integration no longer falls back to mqtt:// (port 1883) when saved.
- A prefix typed with a capital letter (phone keyboard) is accepted.
- The FurgoSuperviseur help mentions wss:// for networks that block port 1883.

## [3.6.1]

- Wi-Fi: from the box access point, a dedicated button now tests the connection to an enterprise network (802.1X: PEAP, EAP-TTLS) before saving, and every failure is explained in plain words: network not found or not on 2.4 GHz, enterprise box to tick or untick, password rejected, credentials rejected by the authentication server, access point refusing the device or no IP address assigned (with the MAC address to give to the IT department).
- A network name or password with accents is no longer truncated when saved, and the anonymous identity or the certificate of an enterprise network are removed by emptying the field.
- An open Wi-Fi network (no password) is now saved by emptying the password field: the previous password used to be kept and the box then refused that network, although the test button succeeded.
- ThingsBoard: the box no longer knows any default server; the server address is entered together with the access token (Integrations page or workshop) and survives a factory reset, an existing link is left unchanged; remote debug mode stays inactive until its server is provided.
- Every reading sent to ThingsBoard carries the number of messages received from the sensor and the counter of replies sent to it.
- Built-in server: a network command frame (port 0) is never decoded as a reading anymore (false values, e.g. a battery at 7 %).

## [3.6.0]

- Radio regions: the configuration page offers the AU915 plan (Australia, Argentina, South America) next to EU868 / US915 / CN470, with a sub-band selector (block of 8 channels) that sets both radios by itself and shows the sensor numbering (1 to 8) alongside the ChirpStack one (0 to 7).
- The built-in LoRaWAN server now follows the selected plan: on US915 / AU915 the reply windows, the join answer (list of channels to use) and the data-rate steering stay on the channels the box listens to, so an AU915 sensor also works without an external server.
- Nothing changes on EU868.

## [3.5.10]

- Stability: Awaro Pro V3 and LT no longer reboot when the USB device they are plugged into goes to sleep (sleeping PC, power-saving hub): the USB console was spinning and tripped the watchdog.
- ThingsBoard: everything the box sends now goes through its supervision integration, which reconnects on its own even without sensors; a box provisioned the old way is converted automatically at first boot.
- A factory reset or a wipe of the settings storage keeps the ThingsBoard link and the remote access key.
- Statistics and box health are sent every 5 minutes by default, instead of every 30 seconds when the Stats setting was empty.
- Sensors: the Seeed SenseCAP S2120 weather station is now decoded like the vendor ChirpStack codec: pressure in Pa, measurement interval published, and a frame from another SenseCAP product no longer hides the reading that follows it.

## [3.5.9]

- ThingsBoard: the box information (installed version, addresses, network name, sensor count, free memory, last reboot cause) is kept up to date on the dashboard after an update again, including when the ThingsBoard integration shares the box connection: it stayed frozen on the previous version.
- The LoRaWAN server mode (built-in or relay) is reported on every path.

## [3.5.8]

- Hautense sensor (electric fence energizer): the batch of timestamped measurements the device sends after each status frame (firmware 1.4) is now decoded and forwarded to ThingsBoard in the same shape as the GSM version, with a summary (number of measurements, min/max voltage and energy) in the log and the integrations.
- The box keeps a copy of its configuration (WiFi, access, ThingsBoard token) and restores it automatically if its settings storage has to be reset during an update: no more box to reconfigure after an automatic update.
- The reason of the last reboot is reported to ThingsBoard (attribute and history) and shown in the box status.
- Configuration page: the Access point / Station choice is applied again on reboot.

## [3.5.7]

- Built-in LoRaWAN server: a command (downlink) sent by your automation within the second following a sensor message now leaves right away, in that message's receive window, instead of waiting for the next message.
- It is sent confirmed and automatically resent at the next message if the sensor did not acknowledge it.
- The downlink counter now survives a reboot of the box: a sensor no longer becomes deaf to commands after a restart.
- The recent packets list shows acknowledgements in both directions.
- The Stats (NS and integrations) setting now sets a single cadence for everything the box sends (statistics, ThingsBoard, integrations, data counters), 5 minutes by default.
- New Internet data-usage counters per purpose.
- Radio range: the reply to the join request of a distant sensor is sent on the fallback window at full power, the transmit power depends on the board, and data-rate adaptation now works both ways.
- Log of the last 200 frames on boards with PSRAM.
- ThingsBoard: device profile per sensor model.
- The Pass field of a webhook accepts a full HTTP header.
- Remote access: a weak radio link no longer cuts the page being viewed.
- Awaro LT: dimmer status LEDs.

## [3.5.6]

- Built-in LoRaWAN server page: the Test button on an integration now shows that it is working and waits for the real answer, instead of refreshing after two seconds and often showing the previous state.
- When a ThingsBoard or MQTT integration is rejected, the page now gives the real reason (token refused) instead of suggesting the server is unreachable.
- Also fixes connecting to secure MQTT servers (mqtts:// and wss://), which failed because their certificate was not recognised.

## [3.5.4]

- Important fix for enterprise WiFi networks: from the configuration page it had become impossible to TURN OFF WPA2-Enterprise mode (the box kept using it even with the checkbox cleared, and eventually fell back to access-point mode).
- The setting can be changed again.

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
