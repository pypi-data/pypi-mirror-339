# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 Michał Góral.

import io
import json
from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from wg_confgen.wg_confgen import Client, ListWg, run_confgen, wg_iter_params

LIST_PARAMS = [
    param for param, f in wg_iter_params(Client) if issubclass(f.type, ListWg)
]
SINGLE_PARAMS = [
    param for param, f in wg_iter_params(Client) if not issubclass(f.type, ListWg) and param != "PublicKey"
]


class RunCall:
    def __init__(self, monkeymock):
        self._retvals = []
        self.mock = monkeymock("wg_confgen.wg_confgen.run")
        self.mock.side_effect = self._side_effect

    def on_call(self, *args, retval, **kwargs):
        self._retvals.append((args, kwargs, retval))

        # sort by length of arguments so side_effect checks more specific calls
        # earlier, e.g. "wg pubkey" is checked before "wg"
        self._retvals.sort(reverse=True, key=lambda v: (len(v[0]), bool(v[1])))

    def _side_effect(self, *args, **kwargs):
        for i, (cargs, ckwargs, retval) in enumerate(self._retvals):
            cl = len(cargs)
            if (
                cl <= len(args)
                and args[:cl] == cargs
                and (kwargs == ckwargs or not ckwargs)
            ):
                if isinstance(retval, (list, tuple)):
                    if not retval:
                        raise IndexError(
                            f"exhausted return values for run mock with args={cargs}, kwargs={ckwargs}"
                        )
                    temp = retval[0]
                    self._retvals[i] = (cargs, ckwargs, retval[1:])
                    retval = temp
                if isinstance(retval, Exception):
                    raise retval
                return retval

        raise KeyError(
            f"run mock called with not configured args={args}, kwargs={kwargs}"
        )


@pytest.fixture
def monkeymock(monkeypatch):
    def _patch(*args):
        m = Mock()
        monkeypatch.setattr(*args, m)
        return m

    return _patch


@pytest.fixture
def run_mock(monkeymock) -> RunCall:
    return RunCall(monkeymock)


@pytest.fixture
def runsut(monkeypatch):
    @dataclass
    class Result:
        returncode: int = 0
        stdout: str = ""
        stderr: str = ""

    def run(*args, input=""):
        stdout = io.StringIO()
        stderr = io.StringIO()

        argv = ("-c", "-") + args

        r = Result()
        try:
            with monkeypatch.context() as m:
                m.setattr("sys.stdin", io.StringIO(input))
                m.setattr("sys.stdout", stdout)
                m.setattr("sys.stderr", stderr)
                r.returncode = run_confgen(argv)
        except SystemExit as e:
            r.returncode = e.code

        r.stdout = stdout.getvalue()
        r.stderr = stderr.getvalue()
        return r

    return run


@pytest.fixture
def getconf(runsut):
    def get(*args, **kwargs):
        input_ = kwargs.get("input")
        if isinstance(input_, dict):
            kwargs["input"] = json.dumps(input_)

        result = runsut(*args, **kwargs)
        assert result.returncode == 0
        return json.loads(result.stdout)

    return get


@pytest.fixture
def d():
    return {
        "clients": {},
        "defaults": {},
        "variables": {},
    }


@pytest.fixture(params=LIST_PARAMS)
def list_param(request):
    return request.param


@pytest.fixture(params=SINGLE_PARAMS)
def single_param(request):
    return request.param


@pytest.fixture(params=SINGLE_PARAMS + LIST_PARAMS)
def wg_param(request):
    return request.param
