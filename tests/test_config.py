from fraktal import load_default_config


def test_load_default_config():
    cfg = load_default_config()
    assert isinstance(cfg, dict)
    assert "app" in cfg
    assert "calculation" in cfg
