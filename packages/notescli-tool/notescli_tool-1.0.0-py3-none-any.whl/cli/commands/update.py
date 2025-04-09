import click
import requests
from cli.commands.login import get_token

@click.command("update")
@click.argument("note_id")
def update_note(note_id):
    """Update an existing note."""
    click.echo("✏️ Updating note...")
    
    title = click.prompt("Enter the new title")
    content = click.prompt("Enter the new content")
    
    response = requests.put(
        f"http://13.71.28.224:5000/notes/{note_id}",  # Use your Azure VM's public IP here
        json={"title": title, "content": content},
        headers={"Authorization": f"Bearer {get_token()}"},
    )
    
    if response.status_code == 200:
        click.echo(f"✅ Successfully updated note ID: {note_id}")
    else:
        click.echo("❌ Failed to update the note. Please check the note ID.")
