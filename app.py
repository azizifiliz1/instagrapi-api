from flask import Flask, request, jsonify
from instagrapi import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Initialize the Client object
cl = Client()

# Get the session ID from environment variables
SESSION_ID = os.getenv("INSTAGRAM_SESSIONID")

# --- IMPORTANT CHANGE STARTS HERE ---
if SESSION_ID:
    try:
        # Attempt to set the session ID using set_settings
        cl.set_settings({"sessionid": SESSION_ID})
        print("INSTAGRAM_SESSIONID loaded successfully.")
    except Exception as e:
        # Handle cases where set_settings might fail or if the session ID is invalid
        print(f"Error setting session ID: {e}")
        # Optionally, you might want to exit or raise an error if the app cannot proceed without a valid session
        raise ValueError("Failed to set INSTAGRAM_SESSIONID. Application cannot start.")
else:
    # If SESSION_ID is not found in environment variables
    print("Warning: INSTAGRAM_SESSIONID environment variable is not set.")
    # It's crucial to decide how your app behaves if the session ID is missing.
    # For a production app, you probably want to prevent it from starting.
    raise ValueError("INSTAGRAM_SESSIONID environment variable is required but not found.")
# --- IMPORTANT CHANGE ENDS HERE ---

@app.route("/get_user", methods=["GET"])
def get_user():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username parametresi eksik"}), 400

    try:
        # Ensure the client is logged in/session is valid before making requests
        # You might want to add a more robust session validation here if needed
        user_info = cl.user_info_by_username(username)
        return jsonify(user_info.dict())
    except Exception as e:
        # Specific error handling for instagrapi (e.g., login required, user not found)
        # would be better than a generic exception
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)