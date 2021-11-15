import os
import pathlib


def config_path(filename: str = "") -> pathlib.Path:
    xdg_config_path = _expanded_path(os.environ.get("XDG_CONFIG_HOME", "~/.config"))
    return xdg_config_path / filename


def _is_valid_filesystem():
    return os.name == "posix"


def _expanded_path(path: str | pathlib.Path) -> pathlib.Path:
    return pathlib.Path(path).expanduser()
