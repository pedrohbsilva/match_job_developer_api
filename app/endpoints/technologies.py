from flask import jsonify, Blueprint
from app.models.tecnology import Tecnology, tecnologies_share_schema
from app import db

TECNOLOGY = Blueprint('TECNOLOGY', __name__,  url_prefix="/technologies")

@TECNOLOGY.route('/get_all_technologies', methods=['GET'])
def get_all_technologies():
  technologies_query = Tecnology.query.order_by(Tecnology.name).all()
  technologies = tecnologies_share_schema.dump(technologies_query)
  
  return jsonify(technologies), 200
  