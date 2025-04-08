import gkeepapi
import json
import sys
import os
from dotenv import load_dotenv

def get_notes():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    email = os.getenv('GOOGLE_EMAIL')
    master_token = os.getenv('GOOGLE_MASTER_TOKEN')
    
    if not email or not master_token:
        raise ValueError("Missing credentials in environment variables")
    
    # Initialize the Keep API
    keep = gkeepapi.Keep()
    
    # Authenticate
    keep.authenticate(email, master_token)
    
    # Get all notes
    notes = keep.all()
    
    # Convert notes to a serializable format
    notes_data = []
    for note in notes:
        notes_data.append({
            'id': note.id,
            'title': note.title,
            'text': note.text,
            'pinned': note.pinned,
            'archived': note.archived,
            'color': note.color.value if note.color else None,
            'labels': [label.name for label in note.labels.all()]
        })
    
    # Return the JSON string
    return json.dumps(notes_data)

def create_note(title: str, text: str, pinned: bool = False) -> str:
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    email = os.getenv('GOOGLE_EMAIL')
    master_token = os.getenv('GOOGLE_MASTER_TOKEN')
    
    if not email or not master_token:
        raise ValueError("Missing credentials in environment variables")
    
    # Initialize the Keep API
    keep = gkeepapi.Keep()
    
    # Authenticate
    keep.authenticate(email, master_token)
    
    # Create a new note
    note = keep.createNote(title, text)
    note.pinned = pinned
    
    # Sync changes
    keep.sync()
    
    # Return the created note's data
    return json.dumps({
        'id': note.id,
        'title': note.title,
        'text': note.text,
        'pinned': note.pinned,
        'archived': note.archived,
        'color': note.color.value if note.color else None,
        'labels': [label.name for label in note.labels.all()]
    })

if __name__ == '__main__':
    print(get_notes()) 