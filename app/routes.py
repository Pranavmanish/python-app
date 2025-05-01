from flask import Blueprint, request, jsonify
from .models import db, Survey
from datetime import datetime

routes = Blueprint('routes', __name__)

from datetime import datetime
from app.models import Survey, LikedFeature, RaffleNumber, db


@routes.route('/survey', methods=['POST'])
def create_survey():
    data = request.get_json()

    # Create the base survey object
    survey = Survey(
        first_name=data['first_name'],
        last_name=data['last_name'],
        street_address=data['street_address'],
        city=data['city'],
        state=data['state'],
        zip_code=data['zip_code'],
        telephone_number=data['telephone_number'],  # ✅ not 'phone'
        email=data['email'],
        date_of_survey=datetime.strptime(data['date_of_survey'], '%Y-%m-%d'),
        interest_source=data.get('interest_source'),
        recommendation_likelihood=data.get('recommendation_likelihood'),
        additional_comments=data.get('additional_comments')
    )

    # Handle liked_campus_features (list of strings)
    features = data.get('liked_campus_features', [])
    for feature in features:
        survey.liked_campus_features.append(LikedFeature(feature=feature))

    # Handle raffle_numbers (list of integers)
    numbers = data.get('raffle_numbers', [])
    for number in numbers:
        survey.raffle_numbers.append(RaffleNumber(number=number))

    db.session.add(survey)
    db.session.commit()

    return jsonify({"message": "Survey created"}), 201


@routes.route("/surveys", methods=["GET"])
def get_surveys():
    surveys = Survey.query.all()
    result = []

    for s in surveys:
        result.append({
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "street_address": s.street_address,
            "city": s.city,
            "state": s.state,
            "zip_code": s.zip_code,
            "telephone_number": s.telephone_number,
            "email": s.email,
            "date_of_survey": s.date_of_survey.strftime('%Y-%m-%d'),
            "interest_source": s.interest_source,
            "recommendation_likelihood": s.recommendation_likelihood,
            "additional_comments": s.additional_comments,
            "liked_campus_features": [f.feature for f in s.liked_campus_features],
            "raffle_numbers": [r.number for r in s.raffle_numbers]
        })

    return jsonify(result), 200

@routes.route("/survey/<int:id>", methods=["PUT"])
def update_survey(id):
    data = request.json
    survey = Survey.query.get_or_404(id)
    for key, value in data.items():
        setattr(survey, key, value)
    db.session.commit()
    return jsonify({"message": "Survey updated"})

@routes.route("/survey/<int:id>", methods=["DELETE"])
def delete_survey(id):
    survey = Survey.query.get_or_404(id)
    db.session.delete(survey)
    db.session.commit()
    return jsonify({"message": "Survey deleted"})

