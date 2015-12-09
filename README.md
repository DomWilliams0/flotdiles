# flotdiles
A python dotfile and not-quite-dotfile management system with no dependencies.

## Usage
* Clone/create your dotfiles git repository in `~/.flotdiles`, then use any `flotdiles` command to create the config.
* Add/remove files and directories using `flotdiles [add | remove] <files...>`
* List your current flotdiles with `flotdiles list`
* Sync with your repository with `flotdiles sync` with the following arguments:
   * `--pull` to update from your repository *without ovewriting local changes* (using git's stash and rebase functionality)
   * `--pull -f` to clear all your local work and revert to the remote state
   * `--push` to push all your local changes
   * `--push -f` to *force* push all your local changes to overwrite the remote version, you savage 