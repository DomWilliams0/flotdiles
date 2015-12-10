# flotdiles
A python dotfile and not-quite-dotfile management system with no dependencies.

## Installation
* Clone this repository with `git clone https://github.com/DomWilliams0/flotdiles.git <optional location>` to anywhere you want to.
* If you don't already have a git repository with your current dotfiles, make one.
* Clone/create your dotfiles git repository in `~/.flotdiles`, then use any flotdiles command to create the config.
* If you have existing dotfiles you want to sync with, use `flotdiles.py sync --pull` to sync and apply changes.

## Usage
* Use `flotdiles.py` with no arguments to view the help menu. 
* Add/remove files and directories using `flotdiles.py [add | remove] <files...>`
* List your current flotdiles with `flotdiles.py list`
* Sync with your repository with `flotdiles.py sync` with the following arguments:
   * `--pull` to update from your repository *without ovewriting local changes* (using git's stash and rebase functionality)
   * `--pull -f` to clear all your local work and revert to the remote state
   * `--push` to push all your local changes
   * `--push -f` to *force* push all your local changes to overwrite the remote version, you savage. 
* Validate your flotdiles with `flotdiles verify`. This will create and delete invalid symlinks. 
* View differences between your local and remote flotdiles with `flotdiles.py status`