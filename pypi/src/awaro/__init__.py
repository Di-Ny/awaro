"""Companion CLI of the Awaro LoRaWAN gateway — https://awaro.fr.

`awaro find` discovers gateways, `awaro status <host>` reports their health,
`awaro log --port ...` shows live decoded frames, `awaro bridge --port ...`
turns the gateway into a USB dongle for MQTT / Home Assistant (implementation
in the open-source lorawan2mqtt project, installed as a dependency).
"""

__version__ = "0.0.3"

from .cli import main  # noqa: F401  (console-script entry point)
