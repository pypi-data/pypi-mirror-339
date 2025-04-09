import click
import requests
from cli.commands.login import get_token

@click.command("delete")
@click.argument("note_id")
def delete_note(note_id):
    """Delete a note by ID."""
    confirm = click.confirm(f"Are you sure you want to delete note {note_id}? This action cannot be undone.", default=False)
    if not confirm:
        click.echo("❌ Deletion canceled.")
        return
    
    response = requests.delete(
        f"http://13.71.28.224:5000/notes/{note_id}",  # Use your Azure VM's public IP here
        headers={"Authorization": f"Bearer {get_token()}"},
    )
    
    if response.status_code == 200:
        click.echo(f"✅ Successfully deleted note ID: {note_id}")
    else:
        click.echo("❌ Failed to delete the note. Please check the note ID.")
