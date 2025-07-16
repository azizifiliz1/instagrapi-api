from flask import Flask, request, jsonify
from instagrapi import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

cl = Client()
SESSION_ID = os.getenv("INSTAGRAM_SESSIONID")
cl.sessionid = SESSION_ID

@app.route("/get_user", methods=["GET"])
def get_user():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username parametresi eksik"}), 400

    try:
        user_info = cl.user_info_by_username(username)
        return jsonify(user_info.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
