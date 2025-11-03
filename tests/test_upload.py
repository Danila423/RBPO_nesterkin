from pathlib import Path

from app.utils.upload import secure_save


def test_rejects_big_file(tmp_path: Path):
    data = b"\x89PNG\r\n\x1a\n" + b"0" * (5_000_001)
    ok, reason = secure_save(tmp_path, "x.png", data)
    assert not ok and reason == "too_big"


def test_sniffs_bad_type(tmp_path: Path):
    ok, reason = secure_save(tmp_path, "x.png", b"not_an_image")
    assert not ok and reason == "bad_type"


