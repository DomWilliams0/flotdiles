import json
import os


class Flotdiles:
    DIR_NAME = '.flotdiles'
    CONFIG_FILE = 'flotdiles.conf'

    def __init__(self, path=None):
        # default
        if not path:
            path = os.path.join(os.environ["HOME"], self.DIR_NAME)

        # create dir
        if not os.path.exists(path):
            print("Flotdile directory not found, creating at '%s'" % path)
            os.mkdir(path)

        self.path = path

        # load config
        self._config = {}
        config_path = os.path.join(path, self.CONFIG_FILE)

        # create config
        if not os.path.exists(config_path):
            self._create_default(config_path)

        # load config
        else:
            with open(config_path) as config:
                self._config = json.load(config)

    def _create_default(self, config_path):
        print("Flotdiles config not found, creating at '%s'" % config_path)
        with open(config_path, 'w') as config:
            json.dump({}, config, indent=4)

    def __getitem__(self, item):
        return self._config[item]

    # operations

    def add_file(self, file):
        # todo
        pass

    # helpers
    
    def __setitem__(self, key, value):
        self._config[key] = value
        # todo save config

    @property
    def synced_files(self):
        return self._config.get("syncedFiles", {})

    @synced_files.setter
    def synced_files(self, value):
        self["syncedFiles"] = value
