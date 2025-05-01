from app import create_app
from app.models import db

import os



# TEMP: Fallback for testing
if not os.getenv("DATABASE_URI"):
    os.environ["DATABASE_URI"] = "mysql+pymysql://admin:Pranav.1719@database-3.cn0oeqcmw45v.us-east-1.rds.amazonaws.com:3306/surveydb2"

print("DEBUG: DATABASE_URI =", os.getenv("DATABASE_URI"))

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
