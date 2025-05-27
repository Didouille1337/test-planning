from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)
CSV_FILE = 'planning.csv'
DESIGNERS = [f"Designer {i+1}" for i in range(15)]

def read_projects():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_project(data):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["nom", "designer", "start", "deadline"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        projet = {
            "nom": request.form["nom"],
            "designer": request.form["designer"],
            "start": request.form["start"],
            "deadline": request.form["deadline"]
        }
        save_project(projet)
        return redirect("/planning")
    return render_template("index.html", designers=DESIGNERS)

@app.route("/planning")
def planning():
    projets = read_projects()
    return render_template("planning.html", projets=projets)

if __name__ == "__main__":
    app.run(debug=True)
