from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Load approved members from members.json
with open("members.json", "r", encoding="utf-8") as f:
    members = json.load(f)
member_lookup = {m["student_number"]: m for m in members}
print(len(member_lookup), "members gathered")  ## needed to be added to Oliver's version maybe

# Load requested members from requested_members.json
with open("requested_members.json", "r", encoding="utf-8") as f:
    requested_members = json.load(f)
requested_lookup = {m["student_number"]: m for m in requested_members}
print(len(requested_lookup), "requested members gathered") ## needed to be added to Oliver's version maybe

attendance_log = []       # in-memory log
signed_in_ids = set()     # track unique sign-ins for current session

# Route for home page and data being passed to the page.
@app.route("/")
def index():
    approved_count = len(members)
    requested_count = len(requested_members)
    return render_template("index.html", approved_count=approved_count, requested_count=requested_count)

# Logic for sign in process.
@app.route("/signin", methods=["POST"])
def signin():
    data = request.json
    student_number = data.get("student_number", "").strip()

    # Check if approved member
    member = member_lookup.get(student_number)
    if member:
        if student_number in signed_in_ids:
            return jsonify({
                "status": "error",
                "message": f"{member['full_name']} has already signed in today."
            }) # Prevent duplicate sign-ins for the same session
        
        # Sign in approved member
        log_entry = {
            "student_number": student_number,
            "full_name": member["full_name"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        attendance_log.append(log_entry) # Add to in-memory log
        signed_in_ids.add(student_number) # Mark as signed in to avoid duplicates
        return jsonify({
            "status": "ok",
            "message": f"Welcome {member['full_name']}. Go warm up!"
        })# Successful sign-in message

    # Check if in requested members (not yet approved - needs to pay)
    requested = requested_lookup.get(student_number)
    if requested:
        return jsonify({
            "status": "warn",
            "message": "20 euro cash payment is required. Please contact committee member."
        })

    # Not found anywhere
    return jsonify({
        "status": "error",
        "message": "Student number not found. Please contact committee member, or register online. with QR Code -> "
    })

# Export attendance log to CSV
@app.route("/export")
def export_csv():
    if not attendance_log:
        return jsonify({"status": "error", "message": "No attendance to export yet."})

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_{today}.csv"
    filepath = os.path.join("exports", filename)

    os.makedirs("exports", exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "student_number", "full_name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attendance_log)

    return send_file(filepath, as_attachment=True)

# Manual reset function but I suppose everytime you restart the server it resets anyway
@app.route("/reset")
def reset_session():
    """Resets the session so everyone can sign in again"""
    global attendance_log, signed_in_ids
    attendance_log = []
    signed_in_ids = set()
    return jsonify({"status": "ok", "message": "Session reset. All previous sign-ins cleared."})

# Admin page to view stats and logs
@app.route("/admin")
def admin_page():
    approved_count = len(members)
    requested_count = len(requested_members)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Filter sign-ins that happened today 
    today_log = [
        log for log in attendance_log 
        if log["timestamp"].startswith(today)
    ]

    attendance_count = len(today_log)

    return render_template(
        "admin.html",
        approved_count=approved_count,
        requested_count=requested_count,
        attendance_count=attendance_count,
        attendance_log=today_log
    )

if __name__ == "__main__":
    app.run(debug=True)