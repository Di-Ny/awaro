"""Companion command for the Awaro LoRaWAN gateway — https://awaro.fr.

`awaro --port <serial> --mqtt-host <broker>` plugs an Awaro gateway into
MQTT / Home Assistant over USB ("dongle" mode). The implementation lives in
the open-source lorawan2mqtt project, installed as a dependency:
https://github.com/lorawan2mqtt/lorawan2mqtt.
"""

__version__ = "0.0.2"


def main():
    from lorawan2mqtt.usb_bridge import main as bridge_main
    bridge_main()
