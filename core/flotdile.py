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
        except SkippedFileError as e:
            print("Skipping '%s' %s" % (f, e.message))

    def _add_flotdile(self, f):
        """
        Adds a flotdile for the given file, by replacing it with a symlink to the flotdile directory

        :param f: A single file path
        """
        f = os.path.abspath(f)

        if not os.path.exists(f):
            raise SkippedFileError("as it doesn't exist")

        if not os.path.isfile(f) or os.path.islink(f):
            raise SkippedFileError("as it isn't a file")

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
            raise SkippedFileError("as it doesn't exist")

        if not os.path.islink(f):
            raise SkippedFileError("as it isn't a flotdile symlink")

        flotdile = self.get_synced_files().get(f)

        if flotdile is None:
            raise SkippedFileError("as it isn't a flotdile")

        # replace symlink with original
        os.remove(f)
        shutil.move(flotdile, f)

        self._remove_synced_file(f)

    def get_synced_files(self):
        return self._config.get(self._SYNCED_FILE_KEY, {})

    def _add_synced_file(self, flotdile, dotfile):
        synced = self.get_synced_files()
        if dotfile in synced:
            raise SkippedFileError("as there is already a flotdile for this file")

        synced[dotfile] = flotdile

        self._update_synced_files(synced)

        print("Added flotdile for %s" % dotfile)

    def _remove_synced_file(self, dotfile):
        synced = self.get_synced_files()
        if dotfile not in synced:
            raise SkippedFileError("as there is not already a flotdile for this file")

        del synced[dotfile]
        self._update_synced_files(synced)

        print("Removed flotdile for %s" % dotfile)

    def _update_synced_files(self, new_dict):
        self._config[self._SYNCED_FILE_KEY] = new_dict

    def verify(self):
        files = self.get_synced_files()
        for src, link in files.items():
            try:
                # check existence
                if not os.path.exists(src):
                    raise InvalidFlotdile(src, "File not found in flotdile directory")
                if not os.path.exists(link):
                    raise InvalidFlotdile(link, "Symlink not found")

                    # todo check for newer file in place of link and update self
            except InvalidFlotdile as e:
                print("Invalid flotdile, removing: " + e.message)

                # replace link with file
                if os.path.exists(link):
                    os.remove(link)
                if os.path.exists(src):
                    shutil.move(src, link)

                self._remove_synced_file(src)

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
            i += 1

        return new_path


class SkippedFileError(RuntimeError):
    pass


class InvalidFlotdile(RuntimeError):
    def __init__(self, f, msg):
        RuntimeError.__init__(self, "%s (%s)" % (msg, f))
