# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import json

import pytest
from cmplib import Contains, DictFields, KeyEq, Not, Or

from wg_confgen.wg_confgen import ClientError


def test_modify_creates_clients(getconf, run_mock):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")
    conf = getconf("modify", "server", input="{}")
    assert conf["clients"] == {"server": {"PrivateKey": "pk"}}


def test_modify_strict(runsut, run_mock):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")
    result = runsut("modify", "--strict", "server", input="{}")
    assert result.returncode == 1


def test_modify_set_list_params(getconf, run_mock, d, list_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {list_param: "value"}
    conf = getconf("modify", "server", list_param, "other-value", input=json.dumps(d))
    assert conf["clients"] == {"server": KeyEq(list_param, ["other-value"])}


def test_modify_set_list_many_params(getconf, run_mock, d, list_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {list_param: "value"}
    conf = getconf("modify", "server", list_param, "val1", "val2", input=json.dumps(d))
    assert conf["clients"] == {"server": KeyEq(list_param, ["val1", "val2"])}


def test_modify_add_list_many_params(getconf, run_mock, d, list_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {list_param: "value"}
    conf = getconf(
        "modify", "server", list_param, "add", "val1", "val2", input=json.dumps(d)
    )
    assert conf["clients"] == {"server": KeyEq(list_param, ["value", "val1", "val2"])}


def test_modify_remove_list_many_params(getconf, run_mock, d, list_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {list_param: ["val1", "val2", "val3"]}
    conf = getconf(
        "modify", "server", list_param, "remove", "val1", "val3", input=json.dumps(d)
    )
    assert conf["clients"] == {"server": KeyEq(list_param, ["val2"])}


def test_modify_remove_single_many_params(getconf, run_mock, d, single_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}
    d["clients"]["server"][single_param] = "value"

    conf = getconf(
        "modify",
        "server",
        single_param,
        "remove",
        "val1",
        "value",
        "val2",
        input=json.dumps(d),
    )

    assert conf["clients"] == {"server": KeyEq(single_param, None)}


def test_modify_remove_single_many_params_miss(getconf, run_mock, d, single_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}
    d["clients"]["server"][single_param] = "value"

    conf = getconf(
        "modify", "server", single_param, "remove", "val1", "val2", input=json.dumps(d)
    )

    assert conf["clients"] == {"server": KeyEq(single_param, "value")}


def test_modify_set_single_params(getconf, run_mock, d, single_param):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {single_param: "value"}
    conf = getconf("modify", "server", single_param, "other-value", input=json.dumps(d))
    assert conf["clients"] == {"server": KeyEq(single_param, "other-value")}


@pytest.mark.parametrize("value", ["value", ["value"]])
def test_modify_remove_then_add_list(getconf, run_mock, d, list_param, value):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {list_param: value}
    conf = getconf(
        "modify", "server", list_param, "remove", "value", input=json.dumps(d)
    )

    assert conf["clients"] == {"server": KeyEq(list_param, None)}

    conf = getconf(
        "modify", "server", list_param, "add", "value", input=json.dumps(conf)
    )

    assert conf["clients"] == {"server": KeyEq(list_param, ["value"])}


def test_modify_remove_single(getconf, run_mock, d, single_param):
    run_mock.on_call("/usr/bin/wg", retval="key")

    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}
    d["clients"]["server"][single_param] = "value"

    conf = getconf(
        "modify", "server", single_param, "remove", "value", input=json.dumps(d)
    )

    assert conf["clients"] == {"server": KeyEq(single_param, None)}


def test_modify_existing_clients(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    d["clients"]["server"] = {
        "Address": "192.168.1.1/24",
        "PersistentKeepalive": "10",
    }

    conf = getconf(
        "modify",
        "server",
        "address",
        "10.8.0.1/24",
        "persistentkeepalive",
        "25",
        input=json.dumps(d),
    )

    assert conf["clients"] == {
        "server": {
            "PrivateKey": "pk",
            "Address": ["10.8.0.1/24"],
            "PersistentKeepalive": "25",
        }
    }


def test_modify_unset(getconf, run_mock, d, wg_param):
    run_mock.on_call("/usr/bin/wg", retval="generated-key")

    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}

    d["clients"]["server"][wg_param] = "value"
    d["defaults"] = {wg_param: "default-value"}

    conf = getconf("modify", "server", wg_param, "unset", input=json.dumps(d))
    assert conf["clients"] == {"server": KeyEq(wg_param, None)}


def test_modify_use_default(getconf, run_mock, d, wg_param):
    run_mock.on_call("/usr/bin/wg", retval="generated-key")

    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}

    d["clients"]["server"][wg_param] = "value"
    d["defaults"] = {wg_param: "default-value"}

    conf = getconf("modify", "server", wg_param, "default", input=json.dumps(d))

    # Keys have no default, so they ignore this directive
    if wg_param in ("PrivateKey", "PresharedKey"):
        assert conf["clients"] == {"server": KeyEq(wg_param, "value")}
    else:
        assert conf["clients"] == {"server": Not(Contains(wg_param))}


def test_modify_set_generate(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genpsk", retval="generated-pskey")

    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}

    # sanity check
    conf_before = getconf("modify", "defaults", input=d)
    assert conf_before["clients"] == {"server": Not(Contains("PresharedKey"))}

    conf = getconf("modify", "defaults", "PresharedKey", "generate", input=d)
    assert conf["clients"] == {"server": KeyEq("PresharedKey", "generated-pskey")}


def test_modify_use_generate(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genpsk", retval="generated-pskey")

    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk"}

    # sanity check
    conf_before = getconf("modify", "defaults", input=d)
    assert conf_before["clients"] == {"server": Not(Contains("PresharedKey"))}

    d["defaults"] = {"PresharedKey": "__GENERATE__"}
    conf = getconf("modify", "server", input=d)
    assert conf["clients"] == {"server": KeyEq("PresharedKey", "generated-pskey")}


def test_modify_generate_is_replaced_by_new_keys(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="generated-pk")
    run_mock.on_call("/usr/bin/wg", "genpsk", retval="generated-pskey")

    # defaults to prevent auto-generation of PrivateKey
    d["clients"]["server"] = {"PrivateKey": "pk", "PresharedKey": "some-psk"}

    conf = getconf(
        "modify",
        "server",
        "presharedkey",
        "generate",
        "privatekey",
        "generate",
        input=d,
    )
    assert conf["clients"] == {
        "server": DictFields(PrivateKey="generated-pk", PresharedKey="generated-pskey")
    }


def test_modify_add_value(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    conf = getconf(
        "modify",
        "server",
        "address",
        "add",
        "10.8.0.1/24",
        "10.8.0.2/24",
        "dns",
        "add",
        "1.1.1.1",
        input=json.dumps(d),
    )

    assert conf["clients"] == {
        "server": {
            "PrivateKey": "pk",
            "Address": ["10.8.0.1/24", "10.8.0.2/24"],
            "DNS": ["1.1.1.1"],
        }
    }


def test_modify_remove_value(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    d["clients"]["server"] = {
        "Address": ["192.168.1.1/24"],
        "DNS": ["1.1.1.1", "1.1.1.2", "8.8.8.8"],
        "PersistentKeepalive": "10",
    }

    conf = getconf(
        "modify",
        "server",
        "dns",
        "remove",
        "1.1.1.2",
        "8.8.8.8",
        "address",
        "remove",
        "192.168.1.1/24",
        input=json.dumps(d),
    )

    assert conf["clients"] == {
        "server": {
            "PrivateKey": "pk",
            "Address": None,
            "DNS": ["1.1.1.1"],
            "PersistentKeepalive": "10",
        }
    }


def test_modify_simultaneous_add_and_remove(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    d["clients"]["server"] = {
        "DNS": ["1.1.1.1", "1.1.1.2", "8.8.8.8"],
    }

    conf = getconf(
        "modify",
        "server",
        "dns",
        "add",
        "1.1.1.3",
        "dns",
        "remove",
        "1.1.1.1",
        "dns",
        "add",
        "1.1.1.1",
        input=json.dumps(d),
    )

    assert conf["clients"] == {
        "server": {
            "PrivateKey": "pk",
            "DNS": ["1.1.1.2", "8.8.8.8", "1.1.1.3", "1.1.1.1"],
        }
    }


def test_modify_simultaneous_remove_missing(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    d["clients"]["server"] = {
        "DNS": ["1.1.1.1", "1.1.1.2", "8.8.8.8"],
    }

    conf = getconf(
        "modify", "server", "dns", "remove", "192.168.1.1", input=json.dumps(d)
    )

    assert conf["clients"] == {
        "server": {
            "PrivateKey": "pk",
            "DNS": ["1.1.1.1", "1.1.1.2", "8.8.8.8"],
        }
    }


def test_modify_add_on_single_value(getconf, run_mock, d, single_param):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    d["clients"]["server"] = {single_param: "foo"}

    with pytest.raises(ClientError):
        conf = getconf(
            "modify", "server", single_param, "add", "30", input=json.dumps(d)
        )

    with pytest.raises(ClientError):
        conf = getconf(
            "modify", "server", single_param, "add", "30", "20", input=json.dumps(d)
        )


def test_modify_remove_defaults(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "genkey", retval="pk")
    run_mock.on_call("/usr/bin/wg", "pubkey", retval="pubkey")

    d["clients"]["server"] = {"PersistentKeepalive": "30", "DNS": ["8.8.8.8"]}
    d["defaults"] = {"PersistentKeepalive": "25", "DNS": "1.1.1.1"}

    conf = getconf(
        "modify",
        "server",
        "persistentkeepalive",
        "unset",
        "dns",
        "remove",
        "8.8.8.8",
        input=json.dumps(d),
    )

    assert conf["clients"] == {
        "server": {
            "PrivateKey": "pk",
            "PersistentKeepalive": None,
            "DNS": None,
        }
    }


def test_modify_privatekey_generates_keypair(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="pk", retval="pubkey")
    run_mock.on_call("/usr/bin/wg", "pubkey", _input="new-pk", retval="new-pubkey")

    d["clients"]["server"] = {"PrivateKey": "pk"}
    conf = getconf("modify", "server", "privatekey", "new-pk", input=json.dumps(d))
    assert conf["clients"] == {
        "server": {
            "PrivateKey": "new-pk",
        }
    }


def test_modify_peers_are_unique(getconf, run_mock, d):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["clients"]["server"] = {
        "PrivateKey": "pk",
        "Peers": ["z", "a", "b", "c"],
    }
    conf = getconf(
        "modify", "server", "peers", "add", "b", "d", "e", "z", input=json.dumps(d)
    )

    assert conf["clients"]["server"]["Peers"] == ["z", "a", "b", "c", "d", "e"]


@pytest.mark.parametrize("client", ["default", "defaults"])
def test_modify_default(getconf, run_mock, d, wg_param, client):
    run_mock.on_call("/usr/bin/wg", retval="key")
    d["defaults"] = {wg_param: "value"}

    conf = getconf("modify", client, wg_param, "newval", input=json.dumps(d))
    assert conf["defaults"] == KeyEq(wg_param, Or("newval", ["newval"]))
