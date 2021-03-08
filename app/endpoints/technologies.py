from flask import jsonify, Blueprint
from app.models.technology import Technology, technologies_share_schema
from app import db

TECHNOLOGY = Blueprint('TECHNOLOGY', __name__,  url_prefix="/technologies")

@TECHNOLOGY.route('/get_all_technologies', methods=['GET'])
def get_all_technologies():
  technologies_query = Technology.query.order_by(Technology.name).all()
  technologies = technologies_share_schema.dump(technologies_query)
  
  return jsonify(technologies), 200
  