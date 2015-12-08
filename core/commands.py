def handle_command(kwargs):
    cmd = kwargs.pop('subcommand')

    if cmd == 'add':
        handle_add(kwargs)
    elif cmd == "remove":
        handle_remove(kwargs)
    elif cmd == "list":
        handle_list(kwargs)
    elif cmd == 'sync':
        handle_sync(kwargs)
    else:
        raise StandardError("Unknown command '%s'" % cmd)


def handle_add(kwargs):
    files = kwargs.pop('files')

    # todo add
    print("Adding files %s" % files)


def handle_remove(kwargs):
    files = kwargs.pop('files')

    # todo remove
    print("Removing files %s" % files)


def handle_list(kwargs):
    # todo list
    print("Listing files")


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
