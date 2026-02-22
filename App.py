from flask import Flask, json, jsonify, render_template, request
import sqlite3
import urllib.request

app = Flask(__name__)

#helper function that opens connection to the database (opening a file before you can read/write)
def get_db():
    conn = sqlite3.connect("prs.db") #open
    conn.row_factory = sqlite3.Row #results to dicts
    return conn

def init_db():
    conn = get_db()
    #recreate tables that already exists
    conn.execute("""
                     CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                 )
             """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pr_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER NOT NULL,
            weight REAL NOT NULL,
            reps INTEGER NOT NULL,
            unit TEXT DEFAULT 'lbs',
            date TEXT NOT NULL,
            is_pr INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/app")
def index():
    return render_template("index.html")

#gets the list of exercises in the api
@app.route("/api/exercises", methods = ["GET"])
def get_exercises():
    conn = get_db()
    rows = conn.execute("SELECT * FROM exercises ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

#add the exercise into a list
@app.route("/api/exercises", methods = ["POST"])
def add_exercise():
    data = request.json
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name Required"})
    conn = get_db()
    try:
        cur = conn.execute("INSERT INTO exercises (name) VALUES (?)", (name,))
        conn.commit()
        ex_id = cur.lastrowid
        conn.close()
        return jsonify({"id": ex_id, "name": name})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Exercise already exists"}), 409
    
#logs
@app.route("/api/logs", methods=["POST"])
def log_set():
    data = request.json
    exercise_id = data["exercise_id"]
    weight = float(data["weight"])
    reps = int(data["reps"])
    unit = data.get("unit", "lbs")
    date = data.get("date")

    conn = get_db()

    #check if weight beats the current best
    prev_best = conn.execute(
        "SELECT MAX(weight) as best FROM pr_logs WHERE exercise_id = ?",
        (exercise_id,)
    ).fetchone()["best"]
    
    is_pr = 1 if (prev_best is None or weight > prev_best) else 0

    cur = conn.execute(
        "INSERT INTO pr_logs (exercise_id, weight, reps, unit, date, is_pr) VALUES (?,?,?,?,?,?)",
        (exercise_id, weight, reps, unit, date, is_pr)
    )

    log_id = cur.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "id": log_id,
        "is_pr": bool(is_pr),
        "weight": weight,
        "reps": reps,
    })

#history of the exercise progress
@app.route("/api/logs/<int:exercise_id>", methods = ["GET"])
def get_logs(exercise_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM pr_logs WHERE exercise_id=? ORDER BY date ASC",
        (exercise_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/quote")
def get_quote():
    try:
        url = "https://zenquotes.io/api/random"
        req = urllib.request.Request(url, headers = {"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return jsonify({"quote": data[0]["q"], "author": data[0]["a"]})
    except:
        return jsonify({"quote": "The pain you feel today is the strength you feel tomorrow.", "author": "Unknown"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5050)
    