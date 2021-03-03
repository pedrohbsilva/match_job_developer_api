from flask import jsonify
import requests
from app import create_app, db
from app.models import candidate, candidates_in_city, city, tecnology, candidate_tecnology
from app.endpoints.db import db_blueprint
from app.endpoints.candidates import CANDIDATE
from app.endpoints.cities import CITY
from app.endpoints.technologies import TECNOLOGY
from app.endpoints.db import populate_database

manager, app = create_app()
app.register_blueprint(db_blueprint)
app.register_blueprint(CANDIDATE)
app.register_blueprint(CITY)
app.register_blueprint(TECNOLOGY)

@app.route('/')
def index():

    return "Api is Online"
 
@manager.command
def recreate_db():
  db.drop_all()
  db.create_all()
  db.session.commit()
  
@manager.command
def populate_db():
  populate_database()
     
if __name__ == "__main__":
  manager.run()
