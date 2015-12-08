import json
import os
import shutil


class Flotdiles:
    DIR_NAME = '.flotdiles'
    CONFIG_FILE = 'flotdiles.conf'

    _SYNCED_FILE_KEY = "synced-files"

    def __init__(self):
        self.path = os.path.join(os.environ["HOME"], self.DIR_NAME)

        # create dir
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # config
        self._config = {}
        self._config_path = os.path.join(self.path, self.CONFIG_FILE)
        self._load_config()

    def _load_config(self):
        # create
        if not os.path.exists(self._config_path):
            print("Flotdiles config not found, creating at '%s'" % self._config_path)
            with open(self._config_path, 'w') as f:
                json.dump({}, f)

        # load
        else:
            with open(self._config_path) as config:
                self._config = json.load(config)

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self._config[key] = value

    # operations

    def add_flotdile(self, f):
        return self._do_flotdile_operation(f, True)

    def remove_flotdile(self, f):
        return self._do_flotdile_operation(f, False)

    def _do_flotdile_operation(self, f, is_add):
        try:
            return self._add_flotdile(f) if is_add else self._remove_flotdile(f)
        except StandardError as e:
            print("Skipping '%s' %s" % (f, e.message))

    def _add_flotdile(self, f):
        """
        Adds a flotdile for the given file, by replacing it with a symlink to the flotdile directory

        :param f: A single file path
        """
        f = os.path.abspath(f)

        if not os.path.exists(f):
            raise StandardError("as it doesn't exist")

        if not os.path.isfile(f) or os.path.islink(f):
            raise StandardError("as it isn't a file")

        filename = os.path.basename(f)
        new_path = self.ensure_unique_file(os.path.join(self.path, filename))

        # move to path and add symlink
        shutil.move(f, new_path)
        os.symlink(new_path, f)

        # add to config
        self._add_synced_file(new_path, f)

    def _remove_flotdile(self, f):
        """
        Removes the given file from the flotdiles, by replacing its symlink with the original file

        :param f: A file path to a single flotdile symlink
        """
        f = os.path.abspath(f)

        if not os.path.exists(f):
            raise StandardError("as it doesn't exist")

        if not os.path.islink(f):
            raise StandardError("as it isn't a flotdile symlink")

        flotdile_results = filter(lambda x: x["dotfile"] == f, self.get_synced_files())

        if len(flotdile_results) == 0:
            raise StandardError("as it isn't a flotdile")

        if len(flotdile_results) != 1:
            raise StandardError("as it...what? There are multiple flotdiles linking to this single file. WAT?")

        src = flotdile_results[0]["flotdile"]

        # replace symlink with original
        os.remove(f)
        shutil.move(src, f)

        self._remove_synced_file(f)

    def get_synced_files(self):
        return self._config.get(self._SYNCED_FILE_KEY, [])

    def _add_synced_file(self, flotdile, dotfile):
        all_synced = self.get_synced_files()
        all_synced.append({
            "flotdile": flotdile,
            "dotfile": dotfile
        })

        self._config[self._SYNCED_FILE_KEY] = all_synced

        print("Added flotdile for %s" % dotfile)

    def _remove_synced_file(self, dotfile):
        new_synced = filter(lambda x: x["dotfile"] != dotfile, self.get_synced_files())
        self._config[self._SYNCED_FILE_KEY] = new_synced

        print("Removed flotdile for %s" % dotfile)

    def save(self):
        with open(os.path.join(self.path, self.CONFIG_FILE), 'w') as config:
            json.dump(self._config, config, indent=4)

    @staticmethod
    def ensure_unique_file(path):
        if not os.path.exists(path):
            return path

        new_path = path
        i = 0
        while os.path.exists(new_path):
            new_path = "%s.fd%d" % (path, i)

        return new_path
