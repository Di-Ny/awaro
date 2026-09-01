# Roadmap

What we are working on for upcoming firmware releases. This page announces
directions, not dates: features ship when they are ready, through the free
over-the-air updates. What has actually landed is in [CHANGELOG.md](CHANGELOG.md).

## In progress 🟠

### Matter support through a companion package

Expose your LoRaWAN sensors in **Apple Home, Google Home, Alexa and
SmartThings** through Matter, with a dedicated package (PyPI) running next to the gateway —
on the machine that already runs your home automation (Raspberry Pi, NAS,
mini-PC), alongside the existing `awaro` companion CLI. One bridge,
commissioned once with a single QR code; every
sensor declared on the gateway then appears automatically as a bridged Matter
device. The LoRaWAN pairing (DevEUI/AppKey) stays on the gateway's web page.
Built in the open around
[lorawan2mqtt](https://github.com/lorawan2mqtt/lorawan2mqtt).

### Persistent packet log on the built-in server

The decoded-frame log of the built-in network server currently lives in RAM: a
reboot or a power cut clears it. It is moving to the gateway's onboard flash
storage, so the frame history survives restarts.

## Planned 🔵

### Remote configuration of the built-in network server

Today, declaring a sensor on the gateway's built-in network server means
reaching its web page — so being on the same local network as the box. That is
fine for a site you can walk into, but not for a gateway on a 4G link or behind
a network you don't control, where the sensor fleet still has to grow.

We are working on configuring the built-in server remotely: adding, renaming
and removing sensors without being on site. This one will be **limited to Pro
gateways** and will most likely require a **subscription**, because it relies
on a hosted service we have to run and keep secure. Gateways will keep working
exactly as they do today without it — and forwarding to an external network
server (TTN, ChirpStack…), which already allows remote sensor provisioning,
stays available on every model, free of charge.

### Native Matter support

The longer-term goal: the gateway itself acts as the Matter bridge — no
companion package, no extra machine. Pair the box once with its QR code and
your LoRaWAN sensors show up in your Matter ecosystem directly.

---

Suggestions and use cases are welcome — open an
[issue](https://github.com/Di-Ny/awaro/issues).
