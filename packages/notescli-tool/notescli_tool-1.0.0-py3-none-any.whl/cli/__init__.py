from cli.commands.login import login_user
from cli.commands.whoami import whoami_user
from cli.commands.create import create_note
from cli.commands.read import read_note
from cli.commands.update import update_note
from cli.commands.delete import delete_note
from cli.commands.logout import logout_user

commands = [login_user, whoami_user, create_note, read_note, update_note, delete_note, logout_user]
