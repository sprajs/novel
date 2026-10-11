import json
from pathlib import Path

import pytest

from novel.runner import load_config


def test_checked_in_config_is_engineering_only():
    config = load_config(Path("configs/cpu-smoke.json"))
    assert config["task"]["split"] == "mechanics"


@pytest.mark.parametrize("field,value", [("dtype", "bfloat16"), ("device", "cuda"),
                                        ("max_new_tokens", 1000), ("atol", 0.2), ("enable_thinking", True)])
def test_config_rejects_unvalidated_conditions(tmp_path, field, value):
    config = json.loads(Path("configs/cpu-smoke.json").read_text())
    config[field] = value
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError):
        load_config(path)


def test_unknown_nested_config_cannot_be_silently_ignored(tmp_path):
    config = json.loads(Path("configs/cpu-smoke.json").read_text())
    config["sampling"]["secret_answer"] = "secret"
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError, match="sampling"):
        load_config(path)
