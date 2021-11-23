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

    def __init__(self):
        xdg_config_path = _expand_path(os.environ.get("XDG_CONFIG_HOME", "~/.config"))

        if os.name not in self.VALID_FILE_SYSTEMS:
            raise Exception(
                f"Invalid file system, only implemented for {self.VALID_FILE_SYSTEMS}."
            )

        self.path = xdg_config_path / self.FILE_NAME

        self._data = self._read_data()

    def add_config(self, app_name: str, config_path: str) -> bool:
        """Adds a new config path for a specific app."""
        # See if the app already has a config path
        # if so, append this as a new config
        # otherwise create new app secton with a list containing the config path
        pass

    def contain(self, app_name: str) -> bool:
        """Checks if the figfile has an entry for a specific app."""
        pass

    def contains_config(self, app_name: str, config_path: str) -> bool:
        """Checks if the figfile contains a specific config path for an app."""
        pass

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
        """Read YAML data from the figfile."""
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
