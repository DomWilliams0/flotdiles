import os
import subprocess


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


def is_git_repo(directory):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return False

    cmd = execute_cmd(["git", "status"], directory)
    return not cmd.startswith("fatal: Not a git repository")


def execute_cmd(cmd, cwd=None):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    out = p.communicate()
    return out[0]
