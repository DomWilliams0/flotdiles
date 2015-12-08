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


def execute_cmd(cmd, get_output, cwd=None):
    """
    Execute a command

    :param cmd: The command
    :param get_output: If True, the output is returned as a string, otherwise it is printed to stdout
    :param cwd: The directory to execute in
    :return: The command output if get_output is True, otherwise None
    """
    if get_output:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
    else:
        stdout = stderr = None

    out = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, cwd=cwd, shell=True).communicate()
    if get_output:
        return out[0]


def push(directory, force):
    # todo intelligent messages

    push_cmd = "git push origin master"
    if force:
        push_cmd += " -f"

    cmds = ("git add -A", "git commit -a -m \"Updated me dotfiles :^)\"", push_cmd)
    map(lambda c: execute_cmd(c, False, directory), cmds)


def pull(directory, force):
    if not force:
        cmds = ("git stash", "git fetch", "git rebase FETCH_HEAD", "git stash pop")
    else:
        cmds = ("git fetch origin", "git clean -fdx", "git reset --hard HEAD")

    map(lambda c: execute_cmd(c, False, directory), cmds)
