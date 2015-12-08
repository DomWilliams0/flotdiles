import json
import os
import shutil


class Flotdiles:
    DIR_NAME = '.flotdiles'
    CONFIG_FILE = 'flotdiles.conf'

    _SYNCED_FILE_KEY = "synced-files"

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
            json.dump({}, config)

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self._config[key] = value
        # todo save config

    # operations

    def add_file(self, f):
        if not os.path.exists(f):
            print("Skipping '%s', as it doesn't exist" % f)

        f = os.path.abspath(f)
        filename = os.path.basename(f)
        new_path = self.sign_file(os.path.join(self.path, filename))

        # move to path and add symlink
        shutil.move(f, new_path)
        os.symlink(new_path, f)

        # add to config
        self._add_synced_file(new_path, f)

    # helpers

    def sign_file(self, path):
        if not os.path.exists(path):
            return path

        new_path = path
        i = 0
        while os.path.exists(new_path):
            new_path = "%s.fd%d" % (path, i)

        return new_path

    def get_synced_files(self):
        return self._config.get(self._SYNCED_FILE_KEY, [])

    def _add_synced_file(self, flotdile, dotfile, save=True):
        all_synced = self.get_synced_files()
        all_synced.append({
            "flotdile": flotdile,
            "dotfile": dotfile
        })

        self._config[self._SYNCED_FILE_KEY] = all_synced

        print("Added flotdile for %s" % dotfile)

        if save:
            with open(os.path.join(self.path, self.CONFIG_FILE), 'w') as config:
                json.dump(self._config, config, indent=4)
