from sysadmin_utils.security import integrity


def test_sha256(tmp_path):
    p = tmp_path / "f.txt"
    p.write_text("hello")
    digest = integrity.sha256(str(p))
    assert digest == (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_manifest_and_diff(tmp_path):
    (tmp_path / "a.txt").write_text("one")
    m1 = integrity.build_manifest(str(tmp_path))
    (tmp_path / "b.txt").write_text("two")
    (tmp_path / "a.txt").write_text("changed")
    m2 = integrity.build_manifest(str(tmp_path))
    d = integrity.diff_manifest(m1, m2)
    assert "b.txt" in d["added"]
    assert "a.txt" in d["changed"]


def test_auth_log(tmp_path):
    from sysadmin_utils.security import auth_log
    log = tmp_path / "auth.log"
    log.write_text(
        "May 1 sshd: Failed password for root from 10.0.0.1 port 22 ssh2\n"
        "May 1 sshd: Failed password for invalid user admin from 10.0.0.1\n"
    )
    fails = auth_log.failed_logins(str(log))
    assert len(fails) == 2
    assert auth_log.top_offenders(str(log))[0] == ("10.0.0.1", 2)
