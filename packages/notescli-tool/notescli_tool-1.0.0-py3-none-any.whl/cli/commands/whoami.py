import click
import requests
from cli.commands.login import get_token

AUTH0_DOMAIN = "dev-g685aqnukt2eao2p.us.auth0.com"

@click.command("whoami")
def whoami_user():
    """Show the currently logged-in user."""
    token = get_token()
    if not token:
        click.echo("❌ You are not logged in.")
        return
    user_info = requests.get(
        f"https://{AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    if user_info.status_code == 200:
        user = user_info.json()
        click.echo(f"👤 You are logged in with email: {user['email']}")
    else:
        click.echo("❌ Unable to fetch user information. Please log in again.")
