from sysadmin_utils.cli import build_parser


def test_all_subcommands_registered():
    parser = build_parser()
    # argparse stores subparser choices on the _SubParsersAction
    actions = [a for a in parser._actions if hasattr(a, "choices") and a.choices]
    names = set()
    for a in actions:
        names.update(a.choices.keys())
    for expected in ("health", "report", "checks", "watch", "exporter",
                     "remote-run", "logscan", "uptime", "sensors", "ports"):
        assert expected in names
