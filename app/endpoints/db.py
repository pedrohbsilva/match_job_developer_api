from flask import jsonify, Blueprint, request
import requests
from app.models.candidate import Candidate
from app.models.city import City
from app.models.tecnology import Tecnology
from app.models.candidates_in_city import CandidatesInCity
from app.models.candidate_tecnology import CandidateTecnology
from app import db
db_blueprint = Blueprint('db_blueprint', __name__,  url_prefix="/data")

@db_blueprint.route('/', methods=['GET'])
def populate_database():
    
    fake_data_user = requests.get("https://randomuser.me/api/?nat=br&results=100", timeout=10)
    fake_data_geek = requests.get("https://geekhunter-recruiting.s3.amazonaws.com/code_challenge.json", timeout=10)
    response_user_json = fake_data_user.json()['results']
    response_geek_json = fake_data_geek.json()['candidates']

    unique_cities = []
    unique_technologies = []
    for count, item in enumerate(response_geek_json):

        candidate = Candidate(
            id=item['id'],
            experience=item['experience'],
            name=response_user_json[count]['name']['first'],
            photo_url=response_user_json[count]['picture']['large'],
            accept_remote=accept_remote(count)
        )
        if item['city'] not in unique_cities:
            unique_cities.append(item['city'])
            city = City(
                        name=item['city']
                    )
            db.session.add(city)
        for tech in item['technologies']:
            if tech['name'] not in unique_technologies:
                unique_technologies.append(tech['name'])
                technology = Tecnology(
                            name=tech['name']
                        )
                db.session.add(technology)
        db.session.add(candidate)
    db.session.commit()
    
    data_candidates = Candidate.query.all()
    data_cities = City.query.all()
    data_technologies = Tecnology.query.all()

    for count, item in enumerate(data_candidates):
        if item.id == response_geek_json[count]['id']:
            candidates_in_city = CandidatesInCity(
                candidate_id=item.id,
                city_id=get_id(data_cities, response_geek_json[count]['city'])
            )
            for tech in response_geek_json[count]['technologies']:
                candidates_technologies = CandidateTecnology(
                    candidate_id=item.id,
                    tecnology_id=get_id(data_technologies, tech['name']),
                    is_main_tech=main_tech(response_geek_json[count]['technologies'], tech['name'])
                )
                db.session.add(candidates_technologies)
            db.session.add(candidates_in_city)
    db.session.commit()

    return jsonify(fake_data_geek.json())

def get_id(list_search, name):
    id_type = 0
    for item in list_search:
        if item.name == name:
            id_type = item.id
    return id_type

def main_tech(list_search, name):
    main_tech_boolean = False
    for item in list_search:
        if item['name'] == name:
            main_tech_boolean = item['is_main_tech']
    return main_tech_boolean

def accept_remote(number):
    if (number % 2) == 0:
        return False
    else:
        return True