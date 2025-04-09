import click
import subprocess
import sys
import os

from cli.commands.create import create_note
from cli.commands.read import read_note
from cli.commands.update import update_note
from cli.commands.delete import delete_note
from cli.commands.login import login_user
from cli.commands.logout import logout_user
from cli.commands.whoami import whoami_user

@click.group()
def cli():
    """NOTESCLI - A CLI Tool for taking notes with Auth0 Security."""
    pass

@click.command("install")
def install():
    """Installs NOTECLI and all dependencies."""
    click.echo("🔧 Installing NOTECLI and dependencies...")

    # Install the package itself
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "notescli"], check=True)
        click.echo("✅ NOTECLI installed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to install NOTECLI: {e}")

    # Install dependencies from setup.py
    dependencies = ["click", "requests", "flask", "pymongo"]
    for package in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            click.echo(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Failed to install {package}: {e}")

    click.echo("🚀 Installation complete! You can now use 'notescli'.")

# Registering CLI commands
cli.add_command(install)
cli.add_command(create_note)
cli.add_command(read_note)
cli.add_command(update_note)
cli.add_command(delete_note)
cli.add_command(login_user)
cli.add_command(logout_user)
cli.add_command(whoami_user)

if __name__ == "__main__":
    cli()
