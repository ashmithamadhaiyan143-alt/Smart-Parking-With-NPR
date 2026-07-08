from flask import Flask, render_template, request, redirect
import sqlite3
import time
import os
from ocr import detect_plate

app = Flask(__name__)

# 🔥 IMPORTANT: Increase upload size (FIX YOUR ISSUE)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024 # 200MB

# TOTAL PARKING SLOTS
TOTAL_SLOTS = 35

UPLOAD_FOLDER = "captured_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return sqlite3.connect("data/parking.db")

# 🏠 HOME
@app.route("/")
def home():
    return render_template("home.html")

# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/dashboard")
    return render_template("login.html")

# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 📷 REGISTER VEHICLE
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        files = request.files.getlist("images")

        # ✅ FIX: handle empty upload
        if not files or files[0].filename == "":
            return render_template("register.html", message="No files selected")

        conn = get_db()
        cur = conn.cursor()

        # Get booked slots
        cur.execute("SELECT slot FROM parking WHERE status='Booked'")
        booked = [row[0] for row in cur.fetchall()]

        for file in files:

            # 🚫 Stop when full
            if len(booked) >= TOTAL_SLOTS:
                conn.close()
                return render_template("register.html", message="🚫 Parking Full!")

            if file.filename == "":
                continue

            # Save image
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            # OCR detection
            vehicle = detect_plate(path)

            if vehicle == "NOT DETECTED":
                continue

            # ✅ Efficient slot allocation
            available_slots = set(range(1, TOTAL_SLOTS + 1)) - set(booked)

            if not available_slots:
                conn.close()
                return render_template("register.html", message="🚫 Parking Full!")

            slot = min(available_slots)

            entry_time = time.strftime("%Y-%m-%d %H:%M:%S")

            # Insert into DB
            cur.execute("""
                INSERT INTO parking(vehicle, slot, entry, status)
                VALUES (?, ?, ?, ?)
            """, (vehicle, slot, entry_time, "Booked"))

            booked.append(slot)

        conn.commit()
        conn.close()

        return redirect("/result")

    return render_template("register.html")


# 🅿️ RESULT PAGE
@app.route("/result")
def result():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM parking")
    records = cur.fetchall()

    cur.execute("SELECT slot FROM parking WHERE status='Booked'")
    booked_slots = [row[0] for row in cur.fetchall()]

    conn.close()

    return render_template(
        "result.html",
        records=records,
        booked_slots=booked_slots,
        total_slots=TOTAL_SLOTS
    )

# 🚪 EXIT VEHICLE
@app.route("/exit/<vehicle>")
def exit_vehicle(vehicle):
    conn = get_db()
    cur = conn.cursor()

    exit_time = time.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        UPDATE parking
        SET exit=?, status='Exited'
        WHERE vehicle=? AND status='Booked'
    """, (exit_time, vehicle))

    conn.commit()
    conn.close()

    return redirect("/result")

# 🗑 DELETE RECORD
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM parking WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/result")

# ▶️ RUN APP
if __name__ == "__main__":
    app.run(debug=True)