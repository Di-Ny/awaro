"""Companion CLI of the Awaro LoRaWAN gateway — https://awaro.fr.

`awaro find` discovers gateways, `awaro status` reports their health,
`awaro backup`/`awaro restore` save and push back their configuration,
`awaro update` checks/installs firmware,
`awaro log --port ...` shows live decoded frames, `awaro bridge --port ...`
turns the gateway into a USB dongle for MQTT / Home Assistant (implementation
in the open-source lorawan2mqtt project, installed as a dependency).
"""

__version__ = "0.2.1"

from .cli import main  # noqa: F401  (console-script entry point)
