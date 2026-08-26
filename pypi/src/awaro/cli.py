"""awaro — companion CLI of the Awaro LoRaWAN gateway (https://awaro.fr).

Subcommands:
    awaro find                     discover gateways (LAN sweep + USB ports)
    awaro status <host>            readable health report of one gateway
    awaro backup <host>            save the gateway configuration to a file
    awaro restore <host> <file>    push a backup file back to a gateway
    awaro update <host>            check/install firmware updates
    awaro log --port <serial>      live decoded frames in the terminal
    awaro bridge --port <serial>   USB -> MQTT + Home Assistant discovery
                                   (implementation: lorawan2mqtt.usb_bridge)

Gateways with a web password: add  -a user:password  to the network commands.
`awaro --port ...` without a subcommand keeps the 0.0.2 behaviour (bridge).
"""
import argparse
import base64
import concurrent.futures
import datetime
import json
import socket
import sys
import time
import urllib.error
import urllib.request

PREFIX = "@LNS "


def _request(host, path, auth=None, data=None, timeout=8):
    """GET (or POST when data is not None) http://host/path, JSON-decoded when
    possible. Raises SystemExit with a readable message on common failures."""
    req = urllib.request.Request("http://%s%s" % (host, path), data=data,
                                 method="POST" if data is not None else "GET")
    if auth:
        req.add_header("Authorization", "Basic " +
                       base64.b64encode(auth.encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("the gateway asks for its web password: retry with "
                     "-a user:password")
        sys.exit("HTTP %d on %s" % (e.code, path))
    except Exception as e:
        sys.exit("gateway unreachable at %s (%s)" % (host, e))
    try:
        return json.loads(body)
    except ValueError:
        return body


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
    d = _request(args.host, "/status", auth=args.auth)
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


# ------------------------------------------------------ backup/restore ----

def cmd_backup(args):
    cfg = _request(args.host, "/export" + ("?secrets=1" if args.secrets else ""),
                   auth=args.auth)
    lns = _request(args.host, "/lns/export", auth=args.auth)
    out = args.out or "awaro-backup-%s-%s.json" % (
        args.host.replace(".", "-"),
        datetime.date.today().isoformat())
    doc = {
        "backup": {"tool": "awaro", "date": datetime.datetime.now().isoformat(timespec="seconds"),
                   "source": args.host, "config_secrets": bool(args.secrets)},
        "config": cfg,
        "lns": lns,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    n_dev = len((lns or {}).get("devices") or [])
    n_hook = len((lns or {}).get("hooks") or [])
    print("Saved %s" % out)
    print("  config : %d field(s)%s" % (len(cfg or {}),
          " incl. secrets (WiFi password, tokens)" if args.secrets else
          " (no WiFi password/token: add --secrets for a full restore file)"))
    print("  LoRaWAN: %d sensor(s), %d integration(s), %d decode table(s)"
          % (n_dev, n_hook, len((lns or {}).get("codecs") or [])))
    print("  ⚠ this file contains the sensors' LoRaWAN keys — store it safely.")


def cmd_restore(args):
    with open(args.file, "r", encoding="utf-8") as f:
        doc = json.load(f)
    cfg, lns = doc.get("config"), doc.get("lns")
    # Also accept a raw /export or /lns/export file saved from the web page.
    if cfg is None and lns is None:
        if "devices" in doc or "hooks" in doc:
            lns = doc
        elif "wifi_ssid" in doc or "ns_host" in doc:
            cfg = doc
        else:
            sys.exit("unrecognized file (expected an `awaro backup` file or a "
                     "gwconfig.json / lns export)")
    if lns is not None and not args.config_only:
        r = _request(args.host, "/lns/import", auth=args.auth,
                     data=json.dumps(lns).encode(), timeout=20)
        print("LoRaWAN restore:", r if isinstance(r, dict) else "sent")
    if cfg is not None and not args.lns_only:
        r = _request(args.host, "/import", auth=args.auth,
                     data=json.dumps(cfg).encode(), timeout=20)
        print("Config restore :", r if isinstance(r, dict) else "sent")
        print("  (the gateway may reboot to apply the configuration)")


# -------------------------------------------------------------- update ----

def cmd_update(args):
    if args.unblock:
        _request(args.host, "/fw?action=unblock", auth=args.auth)
        print("anti-brick lock released.")
    before = _request(args.host, "/fw", auth=args.auth)
    _request(args.host, "/fw?action=check", auth=args.auth)
    fw = before
    for _ in range(15):          # the check is asynchronous since 3.4.0
        time.sleep(2)
        fw = _request(args.host, "/fw", auth=args.auth)
        if fw.get("checked") and fw.get("checked") != before.get("checked"):
            break
    print("Gateway %s — firmware %s (hardware %s)"
          % (args.host, fw.get("cur"), fw.get("hw")))
    print("  channel  : %s" % fw.get("url"))
    print("  published: %s" % (", ".join(fw.get("list") or []) or "?"))
    if fw.get("err"):
        print("  check error: %s" % fw["err"])
    avail = fw.get("avail") or ""
    print("  -> %s" % ("update available: %s" % avail if avail else "up to date."))

    if not args.install:
        if avail:
            print("     install it with: awaro update %s --install %s"
                  % (args.host, avail))
        return
    target = avail if args.install == "latest" else args.install
    if not target:
        print("nothing to install."); return
    r = _request(args.host, "/fw?action=install&v=" + target, auth=args.auth,
                 timeout=15)
    if not (isinstance(r, dict) and r.get("ok")):
        err = (r or {}).get("err") if isinstance(r, dict) else r
        sys.exit("install refused: %s%s" % (err,
                 "  (try: awaro update %s --unblock)" % args.host
                 if "bloqu" in str(err) else ""))
    print("installing %s: the gateway reboots, downloads and installs "
          "(1-3 min)..." % target)
    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(10)
        try:
            req = urllib.request.Request("http://%s/status" % args.host)
            with urllib.request.urlopen(req, timeout=4) as rr:
                cur = (json.load(rr).get("sys") or {}).get("fw")
            if cur == target:
                print("done: gateway is running %s." % cur)
                return
            print("  ... still on %s" % cur)
        except Exception:
            print("  ... rebooting")
    sys.exit("timeout: check the gateway page (anti-brick lock? see "
             "'awaro update %s')" % args.host)


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
    net_parent = argparse.ArgumentParser(add_help=False)
    net_parent.add_argument("-a", "--auth", metavar="USER:PASS",
                            help="web password of the gateway, if one is set")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("find", help="discover gateways (LAN + USB)")
    p.add_argument("--net", help="network prefix to scan (default: local /24)")
    p = sub.add_parser("status", parents=[net_parent],
                       help="health report of one gateway")
    p.add_argument("host", help="IP or hostname (e.g. 192.168.1.68 or awaro-xxxx.local)")
    p = sub.add_parser("backup", parents=[net_parent],
                       help="save the gateway configuration to a JSON file")
    p.add_argument("host")
    p.add_argument("-o", "--out", help="output file (default: awaro-backup-<host>-<date>.json)")
    p.add_argument("--secrets", action="store_true",
                   help="also include WiFi password and tokens in the config part")
    p = sub.add_parser("restore", parents=[net_parent],
                       help="push a backup file back to a gateway")
    p.add_argument("host")
    p.add_argument("file")
    p.add_argument("--lns-only", action="store_true",
                   help="restore only sensors/integrations/decode tables")
    p.add_argument("--config-only", action="store_true",
                   help="restore only the WiFi/NS configuration")
    p = sub.add_parser("update", parents=[net_parent],
                       help="check/install firmware updates")
    p.add_argument("host")
    p.add_argument("--install", metavar="VERSION",
                   help="install this version ('latest' = newest published)")
    p.add_argument("--unblock", action="store_true",
                   help="release the anti-brick lock first")
    p = sub.add_parser("log", help="live decoded frames from the USB port")
    p.add_argument("--port", required=True)
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("-v", "--verbose", action="store_true",
                   help="also show non-event serial lines")
    sub.add_parser("bridge", help="USB -> MQTT + HA discovery (see --help)")
    args = ap.parse_args(argv)
    dispatch = {"find": cmd_find, "status": cmd_status, "backup": cmd_backup,
                "restore": cmd_restore, "update": cmd_update, "log": cmd_log}
    if args.cmd in dispatch:
        return dispatch[args.cmd](args)
    ap.print_help()


if __name__ == "__main__":
    main()
