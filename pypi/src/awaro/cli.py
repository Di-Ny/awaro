"""awaro — companion CLI of the Awaro LoRaWAN gateway (https://awaro.fr).

Subcommands:
    awaro find                     discover gateways (LAN sweep + USB ports)
    awaro status <host>            readable health report of one gateway
    awaro log --port <serial>      live decoded frames in the terminal
    awaro bridge --port <serial>   USB -> MQTT + Home Assistant discovery
                                   (implementation: lorawan2mqtt.usb_bridge)

`awaro --port ...` without a subcommand keeps the 0.0.2 behaviour (bridge).
"""
import argparse
import concurrent.futures
import datetime
import json
import socket
import sys
import urllib.request

PREFIX = "@LNS "


# ---------------------------------------------------------------- find ----

def _local_net():
    """Local /24 prefix, via the interface that routes to the internet."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip.rsplit(".", 1)[0]


def _probe(ip, timeout=1.0):
    try:
        with urllib.request.urlopen("http://%s/status" % ip, timeout=timeout) as r:
            d = json.load(r)
        sysd = d.get("sys") or {}
        if "fw" in sysd and "hw" in sysd:
            return ip, d
    except Exception:
        pass
    return ip, None


def cmd_find(args):
    net = args.net or _local_net()
    print("Scanning %s.0/24 for Awaro gateways..." % net)
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as ex:
        for ip, d in ex.map(_probe, ["%s.%d" % (net, i) for i in range(1, 255)]):
            if d:
                found.append((ip, d))
    if not found:
        print("  none found on the network.")
    for ip, d in sorted(found, key=lambda x: int(x[0].rsplit(".", 1)[1])):
        s, lns = d.get("sys", {}), d.get("lns", {})
        print("  %-15s fw %-8s hw %-9s up %sh  %d sensor(s)  http://%s/"
              % (ip, s.get("fw", "?"), s.get("hw", "?"),
                 round((s.get("uptime") or 0) / 3600, 1),
                 lns.get("devices") or 0, ip))

    try:
        from serial.tools import list_ports
    except ImportError:
        return
    usb = [p for p in list_ports.comports()
           if (p.vid, p.pid) in [(0x1A86, 0x7523), (0x10C4, 0xEA60)]]
    if usb:
        print("USB serial ports that may be a gateway (CH340/CP210x):")
        for p in usb:
            print("  %-8s %s" % (p.device, p.description))
        print("  -> awaro log --port <port>   or   awaro bridge --port <port>")


# -------------------------------------------------------------- status ----

def cmd_status(args):
    url = "http://%s/status" % args.host
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("HTTP %d on %s (web password set? open %s in a browser)"
                 % (e.code, url, "http://%s/" % args.host))
    except Exception as e:
        sys.exit("gateway unreachable at %s (%s)" % (url, e))
    s, lns, net, ns = (d.get(k, {}) for k in ("sys", "lns", "net", "ns"))
    up = s.get("uptime") or 0
    print("Awaro gateway @ %s" % args.host)
    print("  firmware   : %s  (hardware %s)" % (s.get("fw"), s.get("hw")))
    print("  uptime     : %dd %02dh %02dm" % (up // 86400, up % 86400 // 3600,
                                              up % 3600 // 60))
    print("  network    : %s  (%s, RSSI %s dBm)" % (net.get("ip"),
                                                    net.get("ssid"), net.get("rssi")))
    print("  LoRaWAN    : %s mode, %s sensor(s) declared"
          % ("local server" if lns.get("mode") == "local" else "forward",
             lns.get("devices")))
    print("  NS uplink  : %s:%s  (%s)" % (ns.get("host"), ns.get("port"),
                                          "ready" if ns.get("ready") else "not ready"))
    print("  memory     : %s B free heap" % s.get("heap"))


# ----------------------------------------------------------------- log ----

def _fmt_fields(fields):
    out = []
    for name, fv in (fields or {}).items():
        v, u = fv.get("v"), fv.get("u") or ""
        out.append("%s=%s%s" % (name, v, u))
    return "  ".join(out)


def cmd_log(args):
    try:
        import serial
    except ImportError:
        sys.exit("pyserial missing (pip install pyserial)")
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = args.port, args.baud, 0.5
    s.rts = False          # do not reset the gateway on open
    s.dtr = False
    s.open()
    print("Listening on %s (Ctrl+C to stop) — one line per LoRaWAN event..."
          % args.port)
    buf = b""
    try:
        while True:
            buf += s.read(4096)
            while b"\n" in buf:
                raw, buf = buf.split(b"\n", 1)
                line = raw.decode("utf-8", errors="replace").strip()
                if not line.startswith(PREFIX):
                    if args.verbose and line:
                        print("    | " + line)
                    continue
                try:
                    ev = json.loads(line[len(PREFIX):])
                except ValueError:
                    continue
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                head = "%s  %-4s %-12s" % (ts, ev.get("type", "?"),
                                           ev.get("name") or ev.get("deveui", ""))
                if ev.get("type") == "up":
                    print("%s SF%-2s RSSI %s  %s"
                          % (head, ev.get("sf", "?"), ev.get("rssi", "?"),
                             _fmt_fields(ev.get("fields"))
                             or "raw " + (ev.get("data") or "")[:32]))
                else:
                    print(head)
    except KeyboardInterrupt:
        print("\nbye.")
    finally:
        s.close()


# -------------------------------------------------------------- bridge ----

def cmd_bridge(argv):
    from lorawan2mqtt.usb_bridge import main as bridge_main
    sys.argv = ["awaro bridge"] + argv
    bridge_main()


# ---------------------------------------------------------------- main ----

def main():
    argv = sys.argv[1:]
    # 0.0.2 compatibility: `awaro --port ...` (no subcommand) = bridge.
    if argv and argv[0].startswith("-") and argv[0] not in ("-h", "--help"):
        return cmd_bridge(argv)
    if argv and argv[0] == "bridge":
        return cmd_bridge(argv[1:])

    ap = argparse.ArgumentParser(
        prog="awaro", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("find", help="discover gateways (LAN + USB)")
    p.add_argument("--net", help="network prefix to scan (default: local /24)")
    p = sub.add_parser("status", help="health report of one gateway")
    p.add_argument("host", help="IP or hostname (e.g. 192.168.1.68 or awaro-xxxx.local)")
    p = sub.add_parser("log", help="live decoded frames from the USB port")
    p.add_argument("--port", required=True)
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("-v", "--verbose", action="store_true",
                   help="also show non-event serial lines")
    sub.add_parser("bridge", help="USB -> MQTT + HA discovery (see --help)")
    args = ap.parse_args(argv)
    if args.cmd == "find":
        return cmd_find(args)
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "log":
        return cmd_log(args)
    ap.print_help()


if __name__ == "__main__":
    main()
