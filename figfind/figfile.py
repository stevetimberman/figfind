"""Class representing the figfile.yaml file.

The yaml file is structured with keys representing app names, and those apps are
mapped to the corresponding list of config file paths. When this is loaded into
Python, it is represented as an app name dictionary that maps each name to a list
of strings containing the config file paths.

TODO: Delete the filesystem module. Then start using these in the cli.
"""
import os
import pathlib

import yaml  # type: ignore


class FigFile:

    VALID_FILE_SYSTEMS = ["posix"]  # Options are posix, nt and java
    FILE_NAME = "figfile.yml"

    def __init__(self, preload=True):
        xdg_config_path = _expand_path(os.environ.get("XDG_CONFIG_HOME", "~/.config"))

        if os.name not in self.VALID_FILE_SYSTEMS:
            raise Exception(
                f"Invalid file system, only implemented for {self.VALID_FILE_SYSTEMS}."
            )

        self.path = xdg_config_path / self.FILE_NAME

        self._loaded = False
        self._local_data = dict()

        if preload:
            self._load_data()

    def _load_data(self, overwrite=False):
        if overwrite or not self._loaded:
            self._local_data = self._read_data()
            self._loaded = True

    def add_app_config(self, app_name: str, config_path: str, write_to_file: bool = True) -> None:
        """Adds a new config path for a specific app."""
        self._load_data()

        if self._contains_app(app_name):
            self._local_data[app_name] = []

        if not self._contains_path_for_app(config_path):
            expanded_config_path = _expand_path(config_path)
            self._local_data[app_name].append(expanded_config_path)

            if write_to_file:
                self._write_data(self._local_data)

    def _contains_app(self, app_name: str) -> bool:
        """Checks if the figfile has an entry for a specific app."""
        self._load_data()
        return True if app_name in self._local_data else False

    def _contains_path_for_app(self, app_name: str, config_path: str) -> bool:
        """Checks if the figfile contains a specific config path for an app."""
        self._load_data()
        app_paths = self._local_data.get(app_name, [])
        expanded_config_path = _expand_path(config_path)
        return True if config_path in app_paths else False

    def exists(self) -> bool:
        """Checks if a figfile exists in the file system."""
        return self.path.is_file()

    def _write_data(self, data: dict[str, list[str]]) -> bool:
        """Write YAML data to the figfile.

        Writes a dictonary, which maps strings each to a list of strings to a
        YAML file. Returns True of the write succeeds, otherwise False.
        """
        try:
            with open(self.path, "w") as file:
                yaml.dump(data, file)

        except Exception:
            return False

        return True

    def _read_data(self) -> dict[str, list[str]] | None:
        """Read YAML data from the figfile.

        Reads data from figfile.yml, a dictionary where names of apps
        are mapped to a list of config files.
        """
        if not self.exists():
            return {}

        try:
            with open(self.path, "r") as file:
                data = yaml.safe_load(file)

        except Exception:
            return None
            # raise Exception(f'Unable to read data from {self.path}')

        return data


def _expand_path(path: str | pathlib.Path) -> pathlib.Path:
    return pathlib.Path(path).expanduser()
