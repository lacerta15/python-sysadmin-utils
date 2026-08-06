from sysadmin_utils.logs.analyzer import analyze, grep_count
from sysadmin_utils.logs.tailer import tail

SAMPLE = """2026-01-01 INFO started
2026-01-01 ERROR disk failure on sda
2026-01-01 ERROR disk failure on sda
2026-01-01 WARNING high load
"""


def test_analyze(tmp_path):
    p = tmp_path / "app.log"
    p.write_text(SAMPLE)
    result = analyze(str(p))
    assert result["levels"]["ERROR"] == 2
    assert result["levels"]["WARN"] == 1
    assert result["top_errors"][0][1] == 2


def test_grep_count(tmp_path):
    p = tmp_path / "app.log"
    p.write_text(SAMPLE)
    assert grep_count(str(p), "disk failure") == 2


def test_tail(tmp_path):
    p = tmp_path / "big.log"
    p.write_text("\n".join(f"line{i}" for i in range(100)))
    assert tail(str(p), 3) == ["line97", "line98", "line99"]
