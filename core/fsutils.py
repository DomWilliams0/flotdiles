import os


def symlink(link, real_file):
    # todo
    pass


def get_all_files(f):
    """
    :param f: File or directory
    :return: Generator for all children if f is a directory, otherwise a generator with the file as the only element
    """
    if not os.path.isdir(f):
        yield f
    else:
        for dir, subdir, files in os.walk(f):
            for f in files:
                yield os.path.join(dir, f)
