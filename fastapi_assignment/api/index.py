from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import csv
import pathlib

app = FastAPI()

# Allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Find the CSV file
BASE = pathlib.Path(__file__).parent
CSV = BASE / "q-fastapi.csv"

# Read students from the CSV file
students = []

with open(CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"].strip()
        })


@app.get("/api")
async def get_api(request: Request):

    # Get every class parameter from the URL
    classes = request.query_params.getlist("class")

    # Return all students if no class is specified
    if not classes:
        return {"students": students}

    # Filter students while preserving CSV order
    selected_classes = set(classes)

    filtered_students = [
        student
        for student in students
        if student["class"] in selected_classes
    ]

    return {"students": filtered_students}