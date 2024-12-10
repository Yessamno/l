from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import mariadb

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

# Connect to MariaDB
def connect_to_db():
    return mariadb.connect(
        host="127.0.0.1",
        port=3306,
        user="root",  
        password="07312004",  
        database="chatbox"
    )

# Save a message to the database
def save_message(conversation_id, message, sender):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = """
        INSERT INTO chatmessages (conversation_id, sender, message, timestamp)
        VALUES (%s, %s, %s, %s)
    """
    timestamp = datetime.now()
    cursor.execute(query, (conversation_id, sender, message, timestamp))
    connection.commit()
    connection.close()

# API Endpoint to receive chat messages
@app.route('/save_message', methods=['POST'])
def save_message_endpoint():
    data = request.json
    conversation_id = data.get("conversation_id", 1)  # Default to 1 if not provided
    message = data["message"]
    sender = data["sender"]

    save_message(conversation_id, message, sender)
    return jsonify({"status": "success", "message": "Message saved successfully."})

if __name__ == "__main__":
    app.run(debug=True)
