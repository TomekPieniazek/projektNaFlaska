import json
from flask import request, jsonify

def load_json():
    with open('data.json') as document:
        return json.load(document)

def get_json(id: int = 0):
    data = load_json()
    return [user for user in data if user["id"] == id] if id else data

def find_first_free_id() -> int:
    data = load_json()
    taken_ids = {item["id"] for item in data}
    return next(i for i in range(1, max(taken_ids, default=0) + 2) if i not in taken_ids)

def insert_user():
    if not request.json or "name" not in request.json or "lastname" not in request.json:
        return jsonify({"error": "Bad Request"}), 400

    users = load_json()
    new_user_id = find_first_free_id()
    new_user = {"id": new_user_id, "name": request.json["name"], "lastname": request.json["lastname"]}
    users.append(new_user)
    return jsonify(new_user), 201

def update_user(user_id: int = 0):
    if not user_id:
        return jsonify({"error": "No ID"}), 400

    users = load_json()
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "Not Found"}), 400

    if not request.json:
        return jsonify({"error": "Empty Body"}), 400

    for key, value in request.json.items():
        if key in ["name", "lastname"]:
            user[key] = value
        else:
            return jsonify({"error": "Invalid Field"}), 400
    return '', 204

def delete_user(user_id: int = 0):
    if not user_id:
        return jsonify({"error": "No ID"}), 400

    users = load_json()
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "Not Found"}), 400

    users = [u for u in users if u['id'] != user_id]
    return '', 204