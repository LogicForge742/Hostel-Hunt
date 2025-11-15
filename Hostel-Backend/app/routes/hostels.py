from flask import Blueprint, request, jsonify
from ..models.hostel import Hostel
from ..extensions import db

bp = Blueprint("hostels", __name__)

@bp.get("/")
def get_all_hostels():
    hostels = Hostel.query.all()
    return jsonify([{"id": h.id, "name": h.name, "location": h.location} for h in hostels])

@bp.post("/")
def create_hostel():
    data = request.json
    hostel = Hostel(**data)
    db.session.add(hostel)
    db.session.commit()
    return jsonify(message="Hostel created"), 201
