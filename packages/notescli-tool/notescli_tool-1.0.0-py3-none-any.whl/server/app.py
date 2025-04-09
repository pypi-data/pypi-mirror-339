from flask import Flask, request, jsonify
from auth import verify_token
from database import get_all_notes, get_note, create_note, update_note, delete_note

app = Flask(__name__)

@app.route("/notes", methods=["GET", "POST"])
def notes():
    user_id = verify_token(request.headers.get("Authorization"))
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "GET":
        notes = get_all_notes(user_id)
        return jsonify(notes), 200  # Ensure it returns a JSON list

    elif request.method == "POST":
        data = request.json
        note_id = create_note(user_id, data["title"], data["content"])
        return jsonify({"id": note_id}), 201

@app.route("/notes/<note_id>", methods=["GET", "PUT", "DELETE"])
def note_operations(note_id):
    user_id = verify_token(request.headers.get("Authorization"))
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "GET":
        note = get_note(user_id, note_id)
        if note:
            return jsonify(note), 200
        return jsonify({"error": "Note not found"}), 404

    elif request.method == "PUT":
        data = request.json
        updated = update_note(user_id, note_id, data["title"], data["content"])
        return jsonify({"updated": updated}), 200

    elif request.method == "DELETE":
        deleted = delete_note(user_id, note_id)
        return jsonify({"deleted": deleted}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
