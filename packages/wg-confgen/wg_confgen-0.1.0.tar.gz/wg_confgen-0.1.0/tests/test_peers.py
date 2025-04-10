# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import pytest
from cmplib import Contains, KeyEq, Not


@pytest.fixture(autouse=True)
def auto_keys(run_mock):
    run_mock.on_call("/usr/bin/wg", retval="key")


def test_peers_add_to_selected(getconf, d):
    d["clients"] = {"server": {}, "c1": {}, "c2": {}, "c3": {}, "d1": {}}
    conf = getconf("peers", "server", "addto", "c1", "c3", input=d)
    assert conf["clients"] == {
        "server": Not(Contains("Peers")),
        "c1": KeyEq("Peers", ["server"]),
        "c2": Not(Contains("Peers")),
        "c3": KeyEq("Peers", ["server"]),
        "d1": Not(Contains("Peers")),
    }


def test_peers_patterns_add(getconf, d):
    d["clients"] = {"server": {}, "c1": {}, "c2": {}, "c3": {}, "d1": {}}
    conf = getconf("peers", "server", "addto", "c*", input=d)
    assert conf["clients"] == {
        "server": Not(Contains("Peers")),
        "c1": KeyEq("Peers", ["server"]),
        "c2": KeyEq("Peers", ["server"]),
        "c3": KeyEq("Peers", ["server"]),
        "d1": Not(Contains("Peers")),
    }


def test_peers_patterns_dont_add_to_self(getconf, d):
    d["clients"] = {"server": {}, "c1": {}, "c2": {}, "c3": {}, "d1": {}}
    conf = getconf("peers", "server", "addto", "*", input=d)
    assert conf["clients"] == {
        "server": Not(Contains("Peers")),
        "c1": KeyEq("Peers", ["server"]),
        "c2": KeyEq("Peers", ["server"]),
        "c3": KeyEq("Peers", ["server"]),
        "d1": KeyEq("Peers", ["server"]),
    }


def test_peers_patterns_add_unique(getconf, d):
    d["clients"] = {
        "server": {},
        "c1": {"Peers": ["server"]},
        "c2": {"Peers": ["c1", "d1"]},
        "c3": {"Peers": ["c1", "server", "d1"]},
        "d1": {},
    }
    conf = getconf("peers", "server", "addto", "*", input=d)
    assert conf["clients"] == {
        "server": Not(Contains("Peers")),
        "c1": KeyEq("Peers", ["server"]),
        "c2": KeyEq("Peers", ["c1", "d1", "server"]),
        "c3": KeyEq("Peers", ["c1", "server", "d1"]),
        "d1": KeyEq("Peers", ["server"]),
    }


def test_peers_patterns_remove_all(getconf, d):
    d["clients"] = {
        "server": {},
        "c1": {"Peers": ["server"]},
        "c2": {"Peers": ["c1", "d1"]},
        "c3": {"Peers": ["c1", "server", "d1"]},
        "d1": {},
    }
    conf = getconf("peers", "server", "removefrom", "*", input=d)
    assert conf["clients"] == {
        "server": Not(Contains("Peers")),
        "c1": KeyEq("Peers", None),
        "c2": KeyEq("Peers", ["c1", "d1"]),
        "c3": KeyEq("Peers", ["c1", "d1"]),
        "d1": Not(Contains("Peers")),
    }


def test_peers_patterns_remove_from_selected(getconf, d):
    d["clients"] = {
        "server": {},
        "c1": {"Peers": ["server"]},
        "c2": {"Peers": ["c1", "server", "d1"]},
        "c3": {"Peers": ["c1", "server", "d1"]},
        "d1": {},
    }
    conf = getconf("peers", "server", "removefrom", "c1", "c3", input=d)
    assert conf["clients"] == {
        "server": Not(Contains("Peers")),
        "c1": KeyEq("Peers", None),
        "c2": KeyEq("Peers", ["c1", "server", "d1"]),
        "c3": KeyEq("Peers", ["c1", "d1"]),
        "d1": Not(Contains("Peers")),
    }
