import pathlib

import pytest  # noqa: F401

from figfind.filesystem import _expanded_path, _is_valid_filesystem, config_path


def test_is_valid_filesystem(mock_os):
    mock_os.name = "posix"
    assert _is_valid_filesystem()

    mock_os.name = "nt"
    assert not _is_valid_filesystem()


def test_expand_path_same_with_string_and_with_path():
    fake_path = "/etc"
    assert _expanded_path(fake_path) == _expanded_path(pathlib.Path(fake_path))


def test_config_path_no_file(mock_os):
    config_dir = ".config"
    mock_os.environ = {"XDG_CONFIG_HOME": f"~/{config_dir}"}
    path = pathlib.Path.home() / config_dir
    assert config_path() == path


def test_config_path_with_file(mock_os):
    config_dir = ".config"
    mock_os.environ = {"XDG_CONFIG_HOME": f"~/{config_dir}"}
    filename = "filename"
    path_with_file = pathlib.Path.home() / config_dir / filename
    assert config_path(filename) == path_with_file
