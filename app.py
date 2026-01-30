# app.py

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import sqlite3
from datetime import datetime
import random

# Initialize Flask app
app = Flask(__name__)
CORS(app)

DB_PATH = "emergency.db"

# --- Admin credentials ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# --- Vehicle state (simulation) ---
vehicle = {
    "speed": 40,
    "door_locked": True
}

# --- Database functions ---
def create_db():
    """Create database and emergency_logs table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            speed INTEGER,
            door_locked BOOLEAN,
            latitude REAL,
            longitude REAL,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_log(timestamp, speed, door_locked, latitude, longitude, message):
    """Insert a new SOS log into the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emergency_logs
        (timestamp, speed, door_locked, latitude, longitude, message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, speed, door_locked, latitude, longitude, message))
    conn.commit()
    conn.close()

def fetch_logs():
    """Fetch all emergency logs"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emergency_logs")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Routes ---

@app.route("/")
def home():
    return "Backend is running"

@app.route("/status")
def status():
    """Return current vehicle status"""
    return jsonify(vehicle)

@app.route("/sos")
def sos():
    """Trigger SOS: stop vehicle, unlock doors, log event with GPS"""
    vehicle["speed"] = 0
    vehicle["door_locked"] = False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latitude = round(random.uniform(12.9000, 13.1000), 6)   # Simulated GPS
    longitude = round(random.uniform(77.5000, 77.7000), 6)  # Simulated GPS

    insert_log(timestamp, vehicle["speed"], vehicle["door_locked"], latitude, longitude, "Emergency SOS Activated")
    return "SOS Triggered Successfully"

# --- Admin login route ---
@app.route("/admin/login", methods=["POST"])
def admin_login():
    """Check admin credentials for login"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return abort(401, "Invalid credentials")

# --- Protected logs route ---
@app.route("/logs", methods=["GET"])
def logs():
    """Return all logs only for authorized admin"""
    auth = request.authorization
    if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
        return abort(401, "Unauthorized")
    
    data = fetch_logs()
    return jsonify(data)

# --- Run server ---
create_db()
if __name__ == "__main__":
    app.run(debug=True)
