import pytest

from sysadmin_utils.cli import build_parser, main


def test_parser_version():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])


def test_health_command(capsys):
    rc = main(["health"])
    out = capsys.readouterr().out
    assert "Overall" in out
    assert rc in (0, 1)


def test_uptime_command(capsys):
    from sysadmin_utils.cli import main
    rc = main(["uptime"])
    out = capsys.readouterr().out
    assert "up " in out
    assert rc == 0
