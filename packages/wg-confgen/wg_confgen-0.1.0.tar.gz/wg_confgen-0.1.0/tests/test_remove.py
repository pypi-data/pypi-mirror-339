# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import json

import pytest
from cmplib import Contains, KeyEq, Not


@pytest.fixture(autouse=True)
def auto_keys(run_mock):
    run_mock.on_call("/usr/bin/wg", retval="key")


def test_remove(getconf, d):
    d["clients"] = {
        "server": {},
        "c1": {"Peers": ["server"]},
        "c2": {"Peers": ["c1", "server", "d1"]},
        "c3": {"Peers": ["c1", "server", "d1"]},
        "d1": {},
    }
    conf = getconf("remove", "server", "d1", input=d)
    assert conf["clients"] == {
        "c1": KeyEq("Peers", None),
        "c2": KeyEq("Peers", ["c1"]),
        "c3": KeyEq("Peers", ["c1"]),
    }


def test_remove_missing_clients(runsut, d):
    d["clients"] = {
        "server": {},
        "c1": {"Peers": ["server"]},
        "c2": {"Peers": ["c1", "server", "d1"]},
        "c3": {"Peers": ["c1", "server", "d1"]},
        "d1": {},
    }
    result = runsut("remove", "server", "foobar", input=json.dumps(d))
    assert result.returncode != 0

    conf = json.loads(result.stdout)
    assert conf["clients"] == {
        "c1": KeyEq("Peers", None),
        "c2": KeyEq("Peers", ["c1", "d1"]),
        "c3": KeyEq("Peers", ["c1", "d1"]),
        "d1": Not(Contains("Peers")),
    }
