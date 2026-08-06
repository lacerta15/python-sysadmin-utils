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
