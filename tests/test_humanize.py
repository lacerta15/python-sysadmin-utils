from sysadmin_utils.core.humanize import bytes_to_human, seconds_to_human


def test_bytes_to_human():
    assert bytes_to_human(0) == "0.0 B"
    assert bytes_to_human(1024) == "1.0 KiB"
    assert bytes_to_human(1024 ** 3).endswith("GiB")


def test_seconds_to_human():
    assert seconds_to_human(59) == "59s"
    assert seconds_to_human(3661) == "1h 1m 1s"
    assert seconds_to_human(90061).startswith("1d")
