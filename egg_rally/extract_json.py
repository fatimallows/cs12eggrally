from __future__ import annotations
import json
from typing import Protocol, Sequence, Literal

type SettingsValue = float
type SettingsDict = dict[str, SettingsValue]


class json_handler_protocol(Protocol):
    def extract_settings(self, settings_args: Sequence[str] | Literal['all']):
        ...


class json_handler():
    def __init__(self, json_filename: str):
        """On creation, the object should take in a json filename and read from it

        Args:
            json_filename (str): _description_
        """
        try:
            with open(json_filename, 'r') as json_settings:
                self._settings: SettingsDict = json.load(json_settings)
        except FileNotFoundError:
            raise ValueError("file does not exist")

    def extract_settings(self, setting_args: Sequence[str] | Literal['all']) -> SettingsDict:
        """Extracts values of the settings in order of the arguements put in 

        Args:
            settings_args: The list of values to extract from the settings json. 

        Raises:
            KeyError: There exists a key that does not exist in the settings json 

        Returns:
            Extract: A truncated settings dictionary based on the arguement
        """
        if setting_args == 'all':
            return {key: self._settings[key] for key in self._settings}
        try:
            return {key: self._settings[key] for key in setting_args}
        except KeyError:
            # capture which settings dont exist by using 'try: ...; except KeyError as e: ...;'
            raise KeyError(
                (*(tuple(key for key in setting_args if key not in self._settings)),))


if __name__ == "__main__":
    _object = json_handler('implementation1/settings.json')
    try:
        print(_object.extract_settings(
            ("game_fps", "world_width", "world_height")))
    except KeyError as e:
        print(e)
