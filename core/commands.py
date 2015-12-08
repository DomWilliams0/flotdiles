from core import fsutils
from core.flotdiles import Flotdiles

flotdiles = Flotdiles()


def handle_command(kwargs):
    cmd = kwargs.pop('subcommand')

    if cmd == 'add':
        handle_add_remove(kwargs, True)
    elif cmd == "remove":
        handle_add_remove(kwargs, False)
    elif cmd == "list":
        handle_list(kwargs)
    elif cmd == 'sync':
        handle_sync(kwargs)
    else:
        raise StandardError("Unknown command '%s'" % cmd)

    flotdiles.save()


def handle_add_remove(kwargs, is_add):
    files = kwargs.pop('files')
    all_files = []
    map(lambda f: all_files.extend(fsutils.get_all_files(f)), files)

    action = "add" if is_add else "remove"
    func = flotdiles.add_flotdile if is_add else flotdiles.remove_flotdile

    print("Attempting to %s %d file(s)" % (action, len(files)))

    map(func, all_files)


def handle_list(kwargs):
    files = flotdiles.get_synced_files()
    print("Showing %d synced files: " % len(files))

    print(":-------")
    for f in files:
        print(": SRC -> %s" % f["flotdile"])
        print(": LOC -> %s" % f["dotfile"])
        print(":-------")


def handle_sync(kwargs):
    push = kwargs.get('push', False)
    pull = kwargs.get('pull', False)
    force = kwargs['force']

    # validate
    if push == pull:
        if not push:
            push = True  # default
        else:
            raise StandardError("Push OR pull, not both!")

    # todo sync
    print("Sync %sing%s" % ("push" if push else "pull", " forcefully" if force else ""))