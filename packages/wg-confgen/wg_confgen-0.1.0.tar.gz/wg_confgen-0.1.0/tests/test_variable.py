# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import json


def test_variable(getconf, d):
    d["variables"] = {
        "foo": "bar",
        "baz": "blah",
    }

    conf = getconf(
        "variable", "foo", "{ok}", "baz", "unset", "baz", "hi", "new", "1", input=d
    )
    assert conf["variables"] == {
        "foo": "{ok}",
        "baz": "hi",
        "new": "1",
    }


def test_variable_missing_variable_for_unset(runsut, d):
    d["variables"] = {
        "foo": "bar",
        "baz": "blah",
    }

    result = runsut(
        "variable", "baaaz", "unset", "baz", "unset", "blah", "hi", input=json.dumps(d)
    )
    assert result.returncode != 0

    conf = json.loads(result.stdout)
    assert conf["variables"] == {
        "foo": "bar",
        "blah": "hi",
    }


def test_variable_missing_value(runsut, d):
    d["variables"] = {
        "foo": "bar",
        "baz": "blah",
    }

    result = runsut("variable", "baz", input=json.dumps(d))
    assert result.returncode != 0

    conf = json.loads(result.stdout)
    assert conf["variables"] == {
        "foo": "bar",
        "baz": "blah",
    }
