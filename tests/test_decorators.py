import logging
from fraktal.decorators import time_and_memory


def test_time_and_memory_runs():
    called = {"ok": False}

    @time_and_memory(log=lambda s: logging.getLogger("test").info(s))
    def _sample(x):
        return x * 2

    assert _sample(3) == 6
    called["ok"] = True
    assert called["ok"]
