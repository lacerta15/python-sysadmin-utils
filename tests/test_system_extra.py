from sysadmin_utils.system import cpu, memory, netio, uptime


def test_cpu_per_core():
    cores = cpu.per_core()
    assert isinstance(cores, list)
    assert len(cores) >= 1


def test_memory_snapshot():
    snap = memory.snapshot()
    assert snap["total"] > 0
    assert 0 <= snap["percent"] <= 100


def test_netio_counters():
    counters = netio.counters()
    assert isinstance(counters, dict)


def test_uptime_positive():
    assert uptime.uptime_seconds() > 0
    assert isinstance(uptime.uptime_human(), str)
