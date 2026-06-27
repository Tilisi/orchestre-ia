import os
from pathlib import Path

from orchestre.env import load_env


def test_load_env_fallback_preserve_existing(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("A=1\nB='deux mots'\n# commentaire\n", encoding="utf-8")
    monkeypatch.setenv("A", "existant")
    load_env(env_file)
    assert os.environ["A"] == "existant"
    assert os.environ["B"] == "deux mots"


def test_load_env_override(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text('A="nouveau"\n', encoding="utf-8")
    monkeypatch.setenv("A", "ancien")
    load_env(env_file, override=True)
    assert os.environ["A"] == "nouveau"
