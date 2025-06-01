from egg_rally.egg_rally import EggRally
from egg_rally.extract_json import json_handler

if __name__ == "__main__":
    EggRally.main(json_handler('settings.json'))
