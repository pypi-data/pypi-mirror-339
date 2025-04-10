#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from contextlib import contextmanager, suppress
from dataclasses import Field, dataclass, field, fields, replace
from enum import Enum
from functools import cache
from typing import Any, Iterator, Self

__description__ = """
Generate consistent Wireguard configurations.

wg-confgen stores data about all clients in a JSON file (by default: wg0.json in
current directory) and generates consistent Wireguard configs per client. You
can edit this JSON by hand or use built-in `wg-confgen modify` subcommand. It
contains sensitive information (clients' private keys) so it should be stored
securely, similar to ordinary Wireguard configuration files.""".strip()

MODIFY_DESCRIPTION = """
Add clients and modify their settings. Many modifications at once are allowed.

Syntax:
    changes   := <parameter> [mod] <value...>
    parameter := any Wireguard parameter (see: wg(8), wg-quick(8))
    mod       := "set" | "add" | "remove"
    value     := literal value | "unset" | "default" | "generate"

For example:
    wg-confgen modify my-client
        PrivateKey generate
        PersistentKeepalive 25
        AllowedIPs add 192.168.1.0/24 10.0.0.{id}/32
        DNS remove 8.8.8.8

    wg-confgen modify defaults
        PresharedKey generate
        Address 10.8.0.{id}/24
""".strip()

SHOW_DESCRIPTION = """Generate Wireguard configuration for a given client."""

PEERS_DESCRIPTION = """
Quickly add or remove a client as a peer to many other clients.
""".strip()

REMOVE_DESCRIPTION = """
Remove clients. This will also remove them from Peers of remaining clients.
""".strip()

VARIABLE_DESCRIPTION = """
Set custom variables which can be interpolated in clients as {var.<variable>}.

wg-congen-variable accepts a list `<variable> <value>` pairs. <value> can be
either a literal value for variable or a special value "unset" which removes it
from the list.

For example:
    wg-confgen variable
        net 10.8.0
        mask 24
        somevar unset
"""


WG_PATH = None


class ClientError(Exception):
    def __init__(self, name, msg):
        self.client = name
        self.msg = msg


class _Sentinel:
    def __bool__(self):
        return False


class _Default(_Sentinel):
    def __repr__(self):
        return "GETDEFAULT"


class _Missing(_Sentinel):
    def __repr__(self):
        return "MISSING"


class _Generate(_Sentinel):
    def __repr__(self):
        return "GENERATE"


GETDEFAULT = _Default()
MISSING = _Missing()
GENERATE = _Generate()


def eprint(*a, **kw):
    kw["file"] = sys.stderr
    print(*a, **kw)


def wgfield(name: str, **kwargs):
    kwargs["metadata"] = {"wgparam": name}
    return field(**kwargs)


def index_wgfields(cls):
    cls.__wg_params__ = {}
    for f in fields(cls):
        try:
            if issubclass(f.type, Wg):
                cls.__wg_params__[f.name] = f
        except TypeError:
            pass

    return cls


def wg_attr(cls, name: str) -> Field:
    return cls.__wg_params__.get(name)


def wg_iter_params(cls) -> Iterator[tuple[str, Field]]:
    for attrname, f in cls.__wg_params__.items():
        yield (attrname, f)


def wg_attrname(cls, name: str) -> str | None:
    attr = wg_attr(cls, name)
    if not attr:
        return None
    return attr.name


class WgSetNoCoerce:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return repr(self._value)

    @property
    def value(self):
        return self._value


class WgFactorySetNoCoerce(WgSetNoCoerce):
    def __init__(self, factory):
        self._factory = factory
        super().__init__(MISSING)

    def __repr__(self):
        return f"WgFactory(factory={repr(self._factory)})"

    @property
    def value(self):
        if self._value is MISSING:
            self._value = self._factory()
        return self._value


class Wg:
    def __init__(
        self,
        default=MISSING,
        default_factory=MISSING,
        readonly=False,
        getter=None,
        setter=None,
    ):
        if default is not MISSING and default_factory is not MISSING:
            raise ValueError("cannot set both default and default_factory")

        self.default = default
        self.default_factory = default_factory
        self.readonly = readonly
        self.getter = getter
        self.setter = setter
        self._pubname = ""
        self._name = ""

    def __set_name__(self, owner, name):
        self._pubname = name
        self._name = "_" + name.lower()

    def __get__(self, obj, cls=None):
        if obj is None:
            if self.default is not MISSING:
                return WgSetNoCoerce(self.default)
            if self.default_factory is not MISSING:
                return WgFactorySetNoCoerce(self.default_factory)
            raise AttributeError("no default")

        getter = self.getter if self.getter else getattr
        return getter(obj, self._name, self.default)

    def __set__(self, obj, value):
        setter = self.setter if self.setter else setattr

        if isinstance(value, WgSetNoCoerce):
            return setter(obj, self._name, value.value)

        if value is None or value is GETDEFAULT or value is GENERATE:
            return setter(obj, self._name, value)

        try:
            return setter(obj, self._name, self.coerce(value))
        except Exception as e:
            name = getattr(obj, "name", "<unknown>")
            raise ClientError(name, str(e)) from e

    def __delete__(self, obj):
        setter = self.setter if self.setter else setattr

        default = None
        setter(obj, self._name, default)

    def coerce(self, value):
        return value


class StrWg(Wg):
    def coerce(self, value):
        if not isinstance(value, (str, int, float)):
            raise ValueError(f"{self._pubname} must be a single value, not {value}")
        return str(value)


class ListWg(Wg):
    def coerce(self, value):
        if value == "":
            value = []
        elif not isinstance(value, list):
            value = [value]
        return value


def get_endpoint(obj: "Client", attrname, default):
    endpoint = getattr(obj, attrname, default)
    if not isinstance(endpoint, str):
        return endpoint

    if ":" in endpoint:
        return endpoint
    if not isinstance(obj.ListenPort, str):
        return endpoint
    if obj.ListenPort:
        return f"{endpoint}:{obj.ListenPort}"
    return endpoint


def to_none(*args):
    def fn(obj: "Client", attrname, value):
        if value in args:
            setattr(obj, attrname, None)
        else:
            setattr(obj, attrname, value)

    return fn


def set_unique(obj: "Client", attrname, value):
    if isinstance(value, list):
        setattr(obj, attrname, list(dict.fromkeys(value)))
    else:
        setattr(obj, attrname, value)


def no_self_name(obj: "Client", attrname, default):
    value = getattr(obj, attrname, default)

    if isinstance(value, list):
        with suppress(ValueError):
            value.remove(obj.name)
    elif value == obj.name:
        value = ""

    return value


def set_key(obj: "Client", attrname, key):
    if key is GETDEFAULT:
        eprint("Keys have no default value: ignoring")
        return
    setattr(obj, attrname, key)


@index_wgfields
@dataclass
class Client:
    id: int
    _name: str

    PrivateKey: StrWg = StrWg(default=GENERATE, setter=set_key)
    PublicKey: StrWg = StrWg(default=GENERATE, setter=set_key)
    PresharedKey: StrWg = StrWg(default=GETDEFAULT, setter=set_key)

    Address: ListWg = ListWg(default=GETDEFAULT)
    Endpoint: StrWg = StrWg(default=GETDEFAULT, getter=get_endpoint)
    ListenPort: StrWg = StrWg(default=GETDEFAULT, setter=to_none("0"))
    Peers: ListWg = ListWg(default=GETDEFAULT, setter=set_unique, getter=no_self_name)
    MTU: StrWg = StrWg(default=GETDEFAULT, setter=to_none("0"))
    PersistentKeepalive: StrWg = StrWg(default=GETDEFAULT, setter=to_none("0", "off"))
    AllowedIPs: ListWg = ListWg(default=GETDEFAULT)
    DNS: ListWg = ListWg(default=GETDEFAULT)
    FwMark: StrWg = StrWg(default=GETDEFAULT, setter=to_none("0", "off"))
    Table: StrWg = StrWg(default=GETDEFAULT)
    PreUp: ListWg = ListWg(default=GETDEFAULT)
    PostUp: ListWg = ListWg(default=GETDEFAULT)
    PreDown: ListWg = ListWg(default=GETDEFAULT)
    PostDown: ListWg = ListWg(default=GETDEFAULT)
    SaveConfig: StrWg = StrWg(default=GETDEFAULT)

    var: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, *args, dct: dict[str, Any], **kwargs) -> Self:
        for key, val in dct.items():
            if val == "__GENERATE__":
                val = GENERATE
            if attrname := wg_attrname(cls, key):
                kwargs.setdefault(attrname, val)

        kwargs.pop("PublicKey", None)
        return cls(*args, **kwargs)

    def to_dict(self, null=True, default=True, generate=True) -> dict[str, Any]:
        d = {}
        for param, _ in wg_iter_params(Client):
            if param == "PublicKey":
                continue

            value = getattr(self, param)
            if value is GETDEFAULT and default is False:
                continue
            if value is None and null is False:
                continue
            if value in ("", []):
                continue
            if value is GENERATE:
                value = self.genkey(param) if generate else "__GENERATE__"

            d[param] = value
        return d

    def genkey(self, keyname):
        current = getattr(self, keyname)
        if current is not GENERATE:
            return current

        if keyname == "PrivateKey":
            return run(WG_PATH, "genkey").strip()
        elif keyname == "PublicKey":
            if not self.PrivateKey:
                raise ClientError(self.name, "missing PrivateKey")
            try:
                return run(WG_PATH, "pubkey", _input=self.PrivateKey).strip()
            except Exception as e:
                raise ClientError(
                    self.name, "cannot generate PublicKey (invalid PrivateKey)"
                ) from e
        elif keyname == "PresharedKey":
            return run(WG_PATH, "genpsk").strip()

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name

    def section(self, section_name: str) -> list[str]:
        assert section_name in ("Interface", "Peer")
        if section_name == "Interface":
            params = [
                "PrivateKey",
                "Address",
                "ListenPort",
                "MTU",
                "DNS",
                "Table",
                "FwMark",
                "PreUp",
                "PostUp",
                "PreDown",
                "PostDown",
                "SaveConfig",
            ]
        elif section_name == "Peer":
            params = [
                "PublicKey",
                "PresharedKey",
                "Endpoint",
                "AllowedIPs",
                "PersistentKeepalive",
            ]
        else:
            raise ValueError(f"Unknown section: {section_name}")

        return self._section(section_name, *params)

    def replace_defaults(self, default_options: "Client") -> "Client":
        changes = {}
        for _, field_ in wg_iter_params(type(self)):
            attrname = field_.name
            val = getattr(self, attrname)
            if val is GETDEFAULT:
                changes[attrname] = getattr(default_options, attrname)

        return replace(self, **changes)

    def getconf(self, name: str) -> str | None:
        attrname = wg_attrname(type(self), name)
        if not attrname:
            return None

        val = getattr(self, attrname)

        # explicit None means that default was overriden
        if val is None:
            return None

        assert (
            val is not GETDEFAULT
        ), f"Defaults in '{self.name}' detected: use client.replace_defaults()"

        if val is GENERATE:
            val = self._format_value(self.genkey(attrname))
        elif isinstance(val, (list, tuple)):
            val = ", ".join(self._format_value(v) for v in val)
        elif isinstance(val, str):
            val = self._format_value(val)

        if val:
            return f"{name} = {val}"
        return None

    def _format_value(self, value):
        if isinstance(value, (list, tuple)):
            return ", ".join(str(self._format_value(v)) for v in value)
        if not isinstance(value, str):
            return value

        kwargs = {"id": self.id, "name": self.name, "var": self.var}

        try:
            return value.format(**kwargs)
        except KeyError as e:
            eprint(
                f"{self.name}: Invalid variables in configuration: {', '.join(e.args)}"
            )
            eprint(f"  note: Supported variables: {', '.join(kwargs.keys())}")
            sys.exit(1)

    def _section(self, section_name, *params):
        lines = [f"[{section_name}]"]
        for param in params:
            if line := self.getconf(param):
                lines.append(line)
        return lines


class ActionType(Enum):
    set = "set"
    add = "add"
    remove = "remove"


@dataclass
class Change:
    param: str
    value: str | list[str] | None | _Default | _Generate | _Missing = MISSING
    type: ActionType = ActionType.set

    def validate(self) -> bool:
        return self.value is not MISSING

    def set_value(self, value: str):
        vlow = value.lower()

        # Handle "special snowflakes": disabling default ("unset") and setting
        # back parameter to default
        special = {
            "unset": None,
            "default": GETDEFAULT,
            "generate": GENERATE,
        }

        if vlow in special:
            self.value = special[vlow]
            return

        if self.value in (MISSING, None):
            self.value = value  # set first value
        else:
            if not isinstance(self.value, list):
                self.value = [self.value]
            self.value.append(value)

    def apply(self, obj):
        if self.value is MISSING:
            return

        if self.type is ActionType.set:
            setattr(obj, self.param, self.value)

        if self.type is ActionType.add:
            curr = getattr(obj, self.param, None)
            if curr is None or curr is GETDEFAULT:
                curr = []

            if not isinstance(curr, list):
                curr = [curr]

            if isinstance(self.value, list):
                curr.extend(self.value)
            else:
                curr.append(self.value)

            setattr(obj, self.param, curr)

        if self.type is ActionType.remove:
            curr = getattr(obj, self.param)
            values = self.value if isinstance(self.value, list) else [self.value]

            if curr and isinstance(curr, list):
                for value in values:
                    with suppress(ValueError):
                        curr.remove(value)
                if curr:
                    setattr(obj, self.param, curr)
                else:
                    delattr(obj, self.param)
            else:
                for value in values:
                    if curr == value:
                        delattr(obj, self.param)
                        break

    def apply_many(self, objs):
        for obj in objs:
            self.apply(obj)


class Variables(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@dataclass
class Config:
    clients: dict[str, Client] = field(default_factory=dict)
    default_client: Client = field(
        default_factory=lambda: Client(0, "", PrivateKey=None, PresharedKey=None)
    )
    variables: Variables = field(default_factory=Variables)

    def to_dict(self) -> dict[str, Any]:
        d = {}
        d["clients"] = {n: c.to_dict(default=False) for n, c in self.clients.items()}
        d["defaults"] = self.default_client.to_dict(null=False, generate=False)
        d["variables"] = self.variables

        return d


def parse_changes(tokens: list[str], params_map: dict[str, str]) -> list[Change]:
    """Generic parse of a list of parameter changes from a list of `tokens`, in
    a form of:

        <param> [change_type] <value>

    `params_map` denotes a mapping of strings which user might use to the
    actual attribute name used by program.
    """

    changes: list[Change] = []
    curr = None
    for token in tokens:
        token = token.strip()
        if not token:
            continue

        # New parameter detected
        if param := params_map.get(token.lower()):
            if curr and curr.validate():
                changes.append(curr)
            curr = Change(param)
            continue

        # User started without saying which parameter they intend to modify
        if curr is None:
            eprint(f"invalid parameter: {token}")
            sys.exit(1)

        # No parameter yet, so token is either a value or action type
        if curr.value is MISSING:
            try:
                curr.type = ActionType(token.lower())
                continue
            except ValueError:
                pass

        curr.set_value(token)

    if curr and curr.validate():
        changes.append(curr)

    return changes


def run(*args, **kwargs):
    cmd: list[str] = []
    cmd.extend(args)
    opts = {}

    for key, val in kwargs.items():
        dash = "--" if len(key) > 1 else "-"
        opt = f"{dash}{key.replace('_', '-')}"

        if key.startswith("_"):
            opts[key[1:]] = val
        elif val is True:
            cmd.append(opt)
        else:
            cmd.extend((opt, str(val)))

    return subprocess.run(
        cmd, text=True, check=True, capture_output=True, **opts
    ).stdout


def default_client(dct: dict[str, Any]) -> Client:
    dct.setdefault("PrivateKey", None)
    dct.setdefault("PublicKey", None)
    dct.setdefault("PresharedKey", None)

    client = Client.from_dict(0, "", dct=dct)

    for wgname in Client.__wg_params__:
        attrname = wg_attrname(Client, wgname)
        # "default" client can't get any more defaults, so when we detect a
        # GETDEFAULT, it means that there's no default set for it (and other clients
        # will receive None for that param, which will usually disable it)
        if getattr(client, attrname) is GETDEFAULT:
            setattr(client, attrname, None)

    return client


@contextmanager
def open_file(path: str, mode="r"):
    if path == "-":
        f = sys.stdin if not mode or "r" in mode else sys.stdout
    else:
        f = open(path, mode, encoding="utf8")

    try:
        yield f
    finally:
        if path != "-":
            f.close()


def load_config(path: str):
    try:
        with open_file(path) as f:
            config = json.load(f)
    except PermissionError:
        eprint(f"Permission denied: {path}")
        sys.exit(1)
    except FileNotFoundError:
        config = {}

    config.setdefault("clients", {})
    config.setdefault("defaults", {})
    config.setdefault("variables", {})

    ret = Config()
    ret.variables.update(config["variables"])
    for i, (client, client_config) in enumerate(config["clients"].items(), start=1):
        ret.clients[client] = Client.from_dict(
            i, client, var=ret.variables, dct=client_config
        )

    ret.default_client = default_client(config["defaults"])

    return ret


def mark_default_generates(config: Config):
    for attrname, _ in wg_iter_params(Client):
        value = getattr(config.default_client, attrname, None)
        if value is GENERATE:
            for client in config.clients.values():
                client_value = getattr(client, attrname)
                if client_value is GETDEFAULT:
                    setattr(client, attrname, GENERATE)


def atomic_write(path: str, text: str):
    if path == "-":
        with open_file(path, "w") as f:
            f.write(text)
            f.flush()
        return

    # not tempfile to avoid creation of temporary files in directories easily
    # accessible by all users
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def save_config(path: str, config: Config):
    mark_default_generates(config)
    text = json.dumps(config.to_dict(), indent=4)

    try:
        atomic_write(path, text)
    except PermissionError:
        eprint(f"Permission denied: {path}")
        sys.exit(1)
    except FileNotFoundError:
        config = {}


def subcommand_show(args: argparse.Namespace, config: Config):
    client = config.clients.get(args.client)
    if client is None:
        eprint(f"No such client: {args.client}")
        return 1

    defaults = config.default_client
    client = client.replace_defaults(defaults)

    lines = [f"# {client.name}"]
    lines.extend(client.section("Interface"))

    for peername in client.Peers or []:
        peer = config.clients.get(peername)
        if peer is None:
            eprint(f"No such client (used as peer): {peername}")
            return 1
        peer = peer.replace_defaults(config.default_client)

        lines.extend(["", f"# {peer.name}"])
        lines.extend(peer.section("Peer"))

    print("\n".join(lines))
    return 0


def subcommand_modify(args: argparse.Namespace, config: Config):
    params_map = {k.lower(): k for k, _ in wg_iter_params(Client)}
    changes = parse_changes(args.changes, params_map)

    if args.client in ("default", "defaults"):
        client = config.default_client
    else:
        client = config.clients.get(args.client)

    if client is None:
        if args.strict:
            eprint(f"No such client and strict mode prevents addition: {args.client}")
            return 1

        pk_changes = [ch for ch in changes if ch.param == "PrivateKey"]
        pk = pk_changes[-1] if pk_changes else run(WG_PATH, "genkey").strip()
        client = Client(len(config.clients) + 1, args.client, pk)
        config.clients[args.client] = client

    for ch in changes:
        ch.apply(client)

    save_config(args.config, config)
    return 0


def subcommand_peers(args: argparse.Namespace, config: Config):
    retcode = 0
    client = config.clients.get(args.client)
    if client is None:
        eprint("No such client: {args.client}")
        sys.exit(1)

    all_clients = [c for c in config.clients if c != client.name]
    action_type = ActionType.add if args.action.startswith("add") else ActionType.remove
    matches = set()

    for pattern in args.client_patterns:
        matches.update(fnmatch.filter(all_clients, pattern))

    if not matches:
        eprint("Client patterns didn't match any client!")
        retcode = 1

    for match in matches:
        change = Change("Peers", client.name, action_type)
        change.apply(config.clients[match])

    save_config(args.config, config)
    return retcode


def subcommand_remove_clients(args: argparse.Namespace, config: Config):
    retcode = 0
    for name in args.clients:
        try:
            del config.clients[name]
        except KeyError:
            eprint(f"No such client: {name}")
            retcode = 1

    change = Change("Peers", args.clients, ActionType.remove)
    change.apply_many(config.clients.values())

    save_config(args.config, config)

    return retcode


def subcommand_variable(args: argparse.Namespace, config: Config):
    retcode = 0
    i = 0
    while i < len(args.changes):
        variable = args.changes[i]

        try:
            value = args.changes[i + 1]
        except IndexError:
            eprint(f"Missing value for variable '{variable}'")
            retcode = 1
            break

        if value == "unset":
            try:
                del config.variables[variable]
            except KeyError:
                eprint(f"No such variable: '{variable}'")
                retcode = 1
        else:
            config.variables[variable] = value

        i += 2

    save_config(args.config, config)

    return retcode


def prepare_args(argv) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-c", "--config", default="wg0.json")
    parser.add_argument("--wg-path", default="/usr/bin/wg")

    subparsers = parser.add_subparsers(required=True)

    show = subparsers.add_parser(
        "show",
        description=SHOW_DESCRIPTION,
        help="Show configuration for client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    show.add_argument("client", help="client name")
    show.set_defaults(func=subcommand_show)

    modify = subparsers.add_parser(
        "modify",
        description=MODIFY_DESCRIPTION,
        help="Change client parameters parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    modify.add_argument("client", help="client name")
    modify.add_argument(
        "--strict",
        action="store_true",
        help="don't add new clients when they don't exist",
    )
    modify.add_argument("changes", nargs="*", help="parameter changes")
    modify.set_defaults(func=subcommand_modify)

    peers = subparsers.add_parser(
        "peers",
        description=PEERS_DESCRIPTION,
        help="Add or remove client to peers of other clients",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    peers.add_argument("client", help="name of client to be added or removed")
    peers.add_argument("action", choices=("addto", "removefrom"), help="add or remove")
    peers.add_argument(
        "client_patterns",
        nargs="+",
        help="globs of clients tho whom client will be added as a peer",
    )
    peers.set_defaults(func=subcommand_peers)

    remove = subparsers.add_parser(
        "remove",
        description=REMOVE_DESCRIPTION,
        help="Remove clients",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    remove.add_argument("clients", nargs="+", help="client names")
    remove.set_defaults(func=subcommand_remove_clients)

    variable = subparsers.add_parser(
        "variable",
        description=VARIABLE_DESCRIPTION,
        help="Manage variables",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    variable.add_argument(
        "changes",
        nargs="+",
        help="pairs of variable/value which should be set; using 'unset' for value removes a variable",
    )
    variable.set_defaults(func=subcommand_variable)

    return parser.parse_args(argv)


def run_confgen(argv):
    args = prepare_args(argv)
    global WG_PATH
    WG_PATH = args.wg_path

    config = load_config(args.config)

    return args.func(args, config)


def main():
    try:
        return run_confgen(sys.argv[1:])
    except ClientError as e:
        eprint(f"Error[{e.client}]: {e.msg}")
        return 1
    except Exception as e:
        eprint("Error:", str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
