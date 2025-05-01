from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Survey(db.Model):
    __tablename__ = 'survey'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    telephone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_of_survey = db.Column(db.Date, nullable=False)

    liked_campus_features = db.relationship(
        'LikedFeature',
        backref='survey',
        cascade='all, delete-orphan',
        lazy=True
    )

    interest_source = db.Column(db.String(100))
    recommendation_likelihood = db.Column(db.String(50))

    raffle_numbers = db.relationship(
        'RaffleNumber',
        backref='survey',
        cascade='all, delete-orphan',
        lazy=True
    )

    additional_comments = db.Column(db.Text)
class LikedFeature(db.Model):
    __tablename__ = 'liked_features'

    id = db.Column(db.Integer, primary_key=True)
    feature = db.Column(db.String(100), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

class RaffleNumber(db.Model):
    __tablename__ = 'raffle_numbers'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
