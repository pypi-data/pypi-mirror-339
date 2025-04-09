import click
import os

SESSION_TOKEN_FILE = os.path.expanduser("~/.session_token")

@click.command("logout")
def logout_user():
    """Log out of the NOTECLI app."""
    if os.path.exists(SESSION_TOKEN_FILE):
        os.remove(SESSION_TOKEN_FILE)
        click.echo("✅ Successfully logged out.")
    else:
        click.echo("❌ No user currently logged in.")
