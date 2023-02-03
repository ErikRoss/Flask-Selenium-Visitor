from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = b"kd8jd9hn4q30n"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://webservice:20WebService23@localhost:5432/webservice"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:PostgresRoss2022@localhost:5432/fingerprints"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, routes


if __name__ == "__main__":
    app.run()
