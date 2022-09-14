import os
from flask import Flask
# import requests
# from app import create_app, db
# from app.models import candidate, city, technology, candidate_technology
# from app.endpoints.db import db_blueprint
# from app.endpoints.candidates import CANDIDATE
# from app.endpoints.cities import CITY
# from app.endpoints.technologies import TECHNOLOGY
# from app.endpoints.db import populate_database

# manager, app = create_app()
# app.register_blueprint(db_blueprint)
# app.register_blueprint(CANDIDATE)
# app.register_blueprint(CITY)
# app.register_blueprint(TECHNOLOGY)
app = Flask(__name__)

@app.route('/')
def index():

    return "Api is Online"
 
# @manager.command
# def recreate_db():
#   db.drop_all()
#   db.create_all()
#   db.session.commit()
#   print('Success')
  
# @manager.command
# def populate_db():
#   populate_database()
#   print('Success')
     
if __name__ == "__main__":
  app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0',debug=False)
