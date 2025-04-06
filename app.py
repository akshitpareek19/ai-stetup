from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Enum as SqlEnum
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SeverityLevel(enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(SqlEnum(SeverityLevel), nullable=False)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "reported_at": self.reported_at.isoformat() + 'Z'
        }

@app.before_first_request
def create_tables():
    db.create_all()
    if not Incident.query.first():
        # Prepopulate with sample incidents
        sample_incidents = [
            Incident(title="AI model refused to shut down", description="The AI system ignored shutdown commands.", severity=SeverityLevel.High),
            Incident(title="Bias in hiring model", description="The model showed gender bias in job applications.", severity=SeverityLevel.Medium)
        ]
        db.session.bulk_save_objects(sample_incidents)
        db.session.commit()

@app.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([i.to_dict() for i in incidents]), 200

@app.route('/incidents', methods=['POST'])
def create_incident():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'description', 'severity')):
        return jsonify({"error": "Missing required fields."}), 400
    if data['severity'] not in SeverityLevel._member_names_:
        return jsonify({"error": "Invalid severity level."}), 400

    incident = Incident(
        title=data['title'],
        description=data['description'],
        severity=SeverityLevel[data['severity']]
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify(incident.to_dict()), 201

@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found."}), 404
    return jsonify(incident.to_dict()), 200

@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found."}), 404
    db.session.delete(incident)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)