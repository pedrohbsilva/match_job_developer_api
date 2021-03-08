import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_restful import Api
from flask_cors import CORS
from app.config import app_config

db = SQLAlchemy()
cors = CORS()
ma = Marshmallow()

def create_app(): 

  app = Flask(__name__)

  app.config.from_object(app_config[os.getenv('FLASK_ENV')])
  db.init_app(app)
  cors.init_app(app, resources={r"*": {"origins": ["https://quizzical-engelbart-189acb.netlify.app/","http://localhost:3000"]}})
  ma.init_app(ma)
  api = Api(app)
  manager = Manager(app)

  return manager, app