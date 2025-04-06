# AI Safety Incident Log API

This is a backend RESTful API built using Flask and SQLite to log and manage hypothetical AI safety incidents.

## 🔧 Tech Stack

- Python 3
- Flask
- SQLite
- SQLAlchemy

## 🚀 Setup Instructions

1. **Clone the repo or unzip the folder**.

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```

The app will start on `http://127.0.0.1:5000`.

## 📦 Database

- SQLite database `incidents.db` is auto-created with 2 sample incidents.

## 📫 API Endpoints

### GET /incidents

Fetch all incidents.

```bash
curl http://localhost:5000/incidents
```

### POST /incidents

Create a new incident.

```bash
curl -X POST http://localhost:5000/incidents -H "Content-Type: application/json" -d '{"title": "Model failure", "description": "Failed to predict accurately", "severity": "Low"}'
```

### GET /incidents/<id>

Fetch an incident by ID.

```bash
curl http://localhost:5000/incidents/1
```

### DELETE /incidents/<id>

Delete an incident by ID.

```bash
curl -X DELETE http://localhost:5000/incidents/1
```

## ✅ Notes

- Valid severity values: `"Low"`, `"Medium"`, `"High"`.
- `reported_at` timestamp is set automatically.

Enjoy! 😄