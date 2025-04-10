# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import json
import re

import pytest
from cmplib import Contains, DictFields, KeyEq, Not

from wg_confgen.wg_confgen import GETDEFAULT


def parse_config(lhs: str):
    config = {}

    section = None
    for line in lhs.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        m = re.match(r"^\[(\w+)\]", line)
        if m:
            section = m.group(1)
            config.setdefault(section, []).append({})
        else:
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()

            curr = config[section][-1]
            assert key not in curr, f"Repeated keys in config: {key}, section {section}"
            config[section][-1][key] = val

    return config


@pytest.fixture
def getconf(runsut):
    def get(*args, **kwargs):
        result = runsut(*args, **kwargs)
        assert result.returncode == 0
        return parse_config(result.stdout)

    return get


def test_show_all_interface_params(getconf, run_mock, d):
    d["clients"]["server"] = {
        "PrivateKey": "spk",
        "ListenPort": 123,
        "FwMark": "0x123",
        "Address": ["10.8.0.1/24", "10.8.0.2/24"],
        "DNS": ["10.8.0.5", "10.8.0.6"],
        "MTU": 1420,
        "Table": "off",
        "PreUp": "preup",
        "PostUp": "postup",
        "PreDown": "predown",
        "PostDown": "postdown",
        "SaveConfig": "true",
    }
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")
    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [
        {
            "PrivateKey": "spk",
            "ListenPort": "123",
            "FwMark": "0x123",
            "Address": "10.8.0.1/24, 10.8.0.2/24",
            "DNS": "10.8.0.5, 10.8.0.6",
            "MTU": "1420",
            "Table": "off",
            "PreUp": "preup",
            "PostUp": "postup",
            "PreDown": "predown",
            "PostDown": "postdown",
            "SaveConfig": "true",
        }
    ]


def test_show_all_peer_params(getconf, run_mock, d):
    d["clients"]["server"] = {"PrivateKey": "spk", "Peers": ["client"]}
    d["clients"]["client"] = {
        "PrivateKey": "cpk",
        "ListenPort": 12345,
        "PresharedKey": "cpsk",
        "AllowedIPs": ["10.8.0.2/32", "192.168.1.0/24"],
        "Endpoint": "example.com",
        "PersistentKeepalive": 25,
        "Peers": ["server"],
    }
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="generated-pubkey")
    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [{"PrivateKey": "spk"}]
    assert conf["Peer"] == [
        {
            "PublicKey": "generated-pubkey",
            "PresharedKey": "cpsk",
            "AllowedIPs": "10.8.0.2/32, 192.168.1.0/24",
            "Endpoint": "example.com:12345",
            "PersistentKeepalive": "25",
        }
    ]


@pytest.mark.parametrize(
    "endpoint, listenport, expected",
    [
        (None, None, Not(Contains("Endpoint"))),
        (None, 5111, Not(Contains("Endpoint"))),
        ("", None, Not(Contains("Endpoint"))),
        ("example.com", None, KeyEq("Endpoint", "example.com")),
        ("example.com", 0, KeyEq("Endpoint", "example.com")),
        ("example.com", 5111, KeyEq("Endpoint", "example.com:5111")),
        ("example.com:5111", None, KeyEq("Endpoint", "example.com:5111")),
        ("example.com:55222", 5111, KeyEq("Endpoint", "example.com:55222")),
        (GETDEFAULT, GETDEFAULT, Not(Contains("Endpoint"))),
        (GETDEFAULT, 5111, Not(Contains("Endpoint"))),
        ("example.com", GETDEFAULT, KeyEq("Endpoint", "example.com")),
    ],
)
def test_show_endpoint(getconf, run_mock, d, endpoint, listenport, expected):
    d["clients"]["server"] = {"PrivateKey": "spk", "Peers": ["client"]}
    d["clients"]["client"] = {"PrivateKey": "cpk"}
    if listenport is not GETDEFAULT:
        d["clients"]["client"]["ListenPort"] = listenport
    if endpoint is not GETDEFAULT:
        d["clients"]["client"]["Endpoint"] = endpoint

    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Peer"] == [expected]


def test_show_peers(getconf, run_mock, d):
    d["clients"]["server"] = {"PrivateKey": "spk", "Peers": ["client1", "client2"]}
    d["clients"]["client1"] = {"PrivateKey": "c1pk", "Peers": ["server"]}
    d["clients"]["client2"] = {"PrivateKey": "c2pk", "Peers": ["server"]}

    run_mock.on_call("/usr/bin/wg", "pubkey", _input="spk", retval="spub")
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="c1pk", retval="c1pub")
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="c2pk", retval="c2pub")

    j = json.dumps(d)

    srv_conf = getconf("show", "server", input=j)
    assert srv_conf["Interface"] == [{"PrivateKey": "spk"}]
    assert srv_conf["Peer"] == [{"PublicKey": "c1pub"}, {"PublicKey": "c2pub"}]

    c1_conf = getconf("show", "client1", input=j)
    assert c1_conf["Interface"] == [{"PrivateKey": "c1pk"}]
    assert c1_conf["Peer"] == [{"PublicKey": "spub"}]

    c2_conf = getconf("show", "client2", input=j)
    assert c2_conf["Interface"] == [{"PrivateKey": "c2pk"}]
    assert c2_conf["Peer"] == [{"PublicKey": "spub"}]


@pytest.mark.parametrize(
    "param",
    [
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
    ],
)
def test_show_defaults_interface_inheritance(getconf, run_mock, d, param):
    run_mock.on_call("/usr/bin/wg", retval="key")

    d["clients"]["server"] = {"PrivateKey": "spk"}
    d["defaults"] = {param: "value"}

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [KeyEq(param, "value")]


@pytest.mark.parametrize(
    "param",
    ["Endpoint", "AllowedIPs", "PersistentKeepalive"],
)
def test_show_defaults_peer_inheritance(getconf, run_mock, d, param):
    run_mock.on_call("/usr/bin/wg", retval="key")

    d["clients"]["server"] = {
        "PrivateKey": "spk",
        "Peers": ["client"],
    }
    d["clients"]["client"] = {"PrivateKey": "cpk"}
    d["defaults"] = {param: "value"}

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Peer"] == [KeyEq(param, "value")]


def test_show_inherit_list_of_peers_but_not_self(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="spk", retval="spub")

    d["clients"]["server"] = {"PrivateKey": "spk" }
    d["clients"]["client1"] = {"PrivateKey": "c1pk"}
    d["clients"]["client2"] = {"PrivateKey": "c2pk"}
    d["defaults"] = {"Peers": ["server"]}

    conf_server = getconf("show", "server", input=json.dumps(d))
    assert conf_server == Not(Contains("Peer"))

    conf_c1 = getconf("show", "client1", input=json.dumps(d))
    assert conf_c1["Peer"] == [DictFields(PublicKey="spub")]

    conf_c2 = getconf("show", "client2", input=json.dumps(d))
    assert conf_c2["Peer"] == [DictFields(PublicKey="spub")]


# this test differs from test_show_inherit_list_of_peers_but_not_self by
# setting additional "client1" in defaults, which server should inherit
def test_show_inherit_all_peers_but_not_self(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="spk", retval="spub")
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="c1pk", retval="c1pub")

    d["clients"]["server"] = {"PrivateKey": "spk"}
    d["clients"]["client1"] = {"PrivateKey": "c1pk"}
    d["clients"]["client2"] = {"PrivateKey": "c2pk"}
    d["defaults"] = {"Peers": ["server", "client1"]}

    conf_server = getconf("show", "server", input=json.dumps(d))
    assert conf_server["Peer"] == [DictFields(PublicKey="c1pub")]

    conf_c1 = getconf("show", "client1", input=json.dumps(d))
    assert conf_c1["Peer"] == [DictFields(PublicKey="spub")]

    conf_c2 = getconf("show", "client2", input=json.dumps(d))
    assert conf_c2["Peer"] == [
        DictFields(PublicKey="spub"),
        DictFields(PublicKey="c1pub"),
    ]


def test_show_overwrite_defaults(getconf, run_mock, d):
    d["clients"]["server"] = {
        "PrivateKey": "spk",
        "DNS": None,
        "Address": "192.168.1.1/24",
    }
    d["defaults"] = {"Address": "10.100.100.1/24", "DNS": "10.1.1.1"}
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [
        Not(Contains("DNS")) & KeyEq("Address", "192.168.1.1/24")
    ]


def test_show_interpolate(getconf, run_mock, d):
    d["clients"]["server"] = {
        "PrivateKey": "spk",
        "DNS": "{name}-dns.example.com",
        "AllowedIPs": "10.100.100.{id}/32",
        "Peers": ["client"],
    }
    d["clients"]["client"] = {
        "PrivateKey": "cpk",
        "AllowedIPs": "10.100.100.{id}/32",
        "Peers": ["server"],
    }
    d["defaults"] = {"Address": "10.100.100.{id}/24", "DNS": "{name}.example.com"}
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    j = json.dumps(d)

    server_conf = getconf("show", "server", input=j)
    assert server_conf["Interface"] == [
        DictFields(Address="10.100.100.1/24", DNS="server-dns.example.com")
    ]
    assert server_conf["Peer"] == [DictFields(AllowedIPs="10.100.100.2/32")]

    client_conf = getconf("show", "client", input=j)
    assert client_conf["Interface"] == [
        DictFields(Address="10.100.100.2/24", DNS="client.example.com")
    ]
    assert client_conf["Peer"] == [DictFields(AllowedIPs="10.100.100.1/32")]


def test_show_user_variables(getconf, run_mock, d):
    d["clients"]["server"] = {
        "PrivateKey": "spk",
        "DNS": "dns.{var.domain}",
    }
    d["defaults"] = {"Address": "{var.net}.{id}/24"}
    d["variables"] = {"net": "10.8.0", "domain": "example.com"}
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [
        DictFields(Address="10.8.0.1/24", DNS="dns.example.com")
    ]


@pytest.mark.parametrize("value", [None, [], ""])
def test_show_disable_list_defaults(getconf, run_mock, d, list_param, value):
    d["clients"]["server"] = {
        "PrivateKey": "spk",
        list_param: value,
    }
    d["defaults"] = {list_param: "some-default"}
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [Not(Contains(list_param)) & Contains("PrivateKey")]


@pytest.mark.parametrize("value", [None, ""])
def test_show_disable_single_defaults(getconf, run_mock, d, single_param, value):
    d["clients"]["server"] = {
        single_param: value,
    }
    d["defaults"] = {single_param: "some-default"}
    run_mock.on_call("/usr/bin/wg", retval="key")

    conf = getconf("show", "server", input=json.dumps(d))
    assert conf["Interface"] == [Not(Contains(single_param))]


def test_show_use_generate(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="spk", retval="spub")
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="cpk", retval="cpub")
    run_mock.on_call("/usr/bin/wg", "genpsk", retval=["psk1", "psk2"])

    d["clients"]["server"] = {"PrivateKey": "spk", "Peers": ["client"]}
    d["clients"]["client"] = {"PrivateKey": "cpk", "Peers": ["server"]}
    d["defaults"] = {"PresharedKey": "__GENERATE__"}

    client_conf = getconf("show", "client", input=json.dumps(d))
    assert client_conf["Peer"] == [DictFields(PublicKey="spub", PresharedKey="psk1")]

    server_conf = getconf("show", "server", input=json.dumps(d))
    assert server_conf["Peer"] == [DictFields(PublicKey="cpub", PresharedKey="psk2")]
