# awaro

Companion CLI of **Awaro**, an autonomous LoRaWAN gateway (hardware
product) — see <https://awaro.fr>.

```bash
pip install awaro

awaro find                      # discover gateways (LAN sweep + USB ports)
awaro status 192.168.1.68       # readable health report of one gateway
awaro log --port /dev/ttyUSB0   # live decoded sensor frames in the terminal
awaro bridge --port /dev/ttyUSB0 --mqtt-host 127.0.0.1
                                # USB "dongle" mode: MQTT + HA discovery
```

`awaro log` and `awaro bridge` read the gateway's USB serial stream: every
LoRaWAN frame arrives **already decoded** by the gateway (firmware 3.4.0+) —
named values, units, Home Assistant device classes — zero cloud, zero WiFi,
zero codec configuration on the host:

```
12:23:08  up   FGLR_02   SF12 RSSI -84  bat=3.87V  sht45_temp=24.33°C  sht45_hum=70.87%
```

The bridge implementation lives in the open-source
[lorawan2mqtt](https://github.com/lorawan2mqtt/lorawan2mqtt) project
(community codec database + bridges), installed as a dependency.
