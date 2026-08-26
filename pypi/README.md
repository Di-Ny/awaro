# awaro

Companion package of **Awaro**, an autonomous LoRaWAN gateway (hardware
product) — see <https://awaro.fr>.

```bash
pip install awaro
awaro --port /dev/ttyUSB0 --mqtt-host 127.0.0.1
```

Plug the gateway into any machine over USB: it streams every decoded sensor
frame as JSON lines, and the `awaro` command republishes them as MQTT +
Home Assistant discovery entities — zero cloud, zero WiFi, zero codec
configuration ("the Zigbee dongle of LoRaWAN", firmware 3.4.0+).

The implementation lives in the open-source
[lorawan2mqtt](https://github.com/lorawan2mqtt/lorawan2mqtt) project
(community codec database + bridges), installed as a dependency.
