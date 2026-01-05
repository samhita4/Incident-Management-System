from flask import Flask, render_template, request, redirect
from db import cursor, db

app = Flask(__name__)

@app.route("/")
def dashboard():
    cursor.execute("SELECT * FROM incidents ORDER BY created_at DESC")
    incidents = cursor.fetchall()
    return render_template("dashboard.html", incidents=incidents)

@app.route("/create", methods=["GET", "POST"])
def create_incident():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]

        cursor.execute(
            "INSERT INTO incidents (title, description, priority, status) VALUES (%s, %s, %s, %s)",
            (title, description, priority, "Open")
        )
        db.commit()
        return redirect("/")
    return render_template("create_incident.html")

# Assign person
@app.route("/assign/<int:id>", methods=["POST"])
def assign_incident(id):
    assignee = request.form["assignee"]

    cursor.execute(
        "UPDATE incidents SET assigned_to=%s, status=%s WHERE id=%s",
        (assignee, "Assigned", id)
    )
    db.commit()
    return redirect("/")

# Update status from Action dropdown
@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    action = request.form["action"]

    if action == "resolved":
        new_status = "Resolved"
    elif action == "not_resolved":
        new_status = "Not Resolved"
    else:
        new_status = "Assigned"

    cursor.execute(
        "UPDATE incidents SET status=%s WHERE id=%s",
        (new_status, id)
    )
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
