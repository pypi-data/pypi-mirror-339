import click
import requests
from cli.commands.login import get_token

API_URL = "http://13.71.28.224:5000/notes"

@click.command("read")
@click.argument("note_id", required=False)
def read_note(note_id):
    """Read all notes or a specific note by ID."""
    headers = {"Authorization": f"Bearer {get_token()}"}

    if note_id:
        # Fetch a specific note
        response = requests.get(f"{API_URL}/{note_id}", headers=headers)
        if response.status_code == 200:
            note = response.json()
            click.echo(f"📝 Note ID: {note['_id']}\nTitle: {note['title']}\nContent: {note['content']}")
        else:
            click.echo("❌ Failed to fetch the note. Check the note ID.")
    else:
        # Fetch all notes
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            notes = response.json()
            if isinstance(notes, list) and notes:
                click.echo("📋 Your Notes:")
                for note in notes:
                    click.echo(f"📝 {note['_id']} - {note['title']}")
            else:
                click.echo("ℹ️ No notes found.")
        else:
            click.echo("❌ Failed to fetch notes.")
