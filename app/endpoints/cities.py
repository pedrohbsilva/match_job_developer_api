from flask import jsonify, Blueprint, request
from app.models.city import City, cities_share_schema
from app import db

CITY = Blueprint('CITY', __name__,  url_prefix="/cities")

@CITY.route('/get_all_cities', methods=['GET'])
def get_all_cities():
  cities_query = City.query.order_by(City.name).all()
  cities = cities_share_schema.dump(cities_query)
  
  return jsonify(cities), 200
  