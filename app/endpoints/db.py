from flask import jsonify, Blueprint, request
import requests
import re
from app.models.candidate import Candidate
from app.models.city import City
from app.models.technology import Technology
from app.models.candidate_technology import CandidateTechnology
from app import db

db_blueprint = Blueprint('db_blueprint', __name__,  url_prefix="/data")

@db_blueprint.route('/', methods=['GET'])
def populate_database():
    """[summary]
        Endpoint to populate the database receiving json from Geek and RandomUser
    Returns:
        [json]: [return a json of geek]
    """    
    
    fake_data_user = requests.get("https://randomuser.me/api/?nat=br&results=100", timeout=10)
    fake_data_geek = requests.get("https://geekhunter-recruiting.s3.amazonaws.com/code_challenge.json", timeout=10)
    response_user_json = fake_data_user.json()['results']
    response_geek_json = fake_data_geek.json()['candidates']

    unique_cities = []
    unique_technologies = []
    for count, item in enumerate(response_geek_json):
        experience = reformule_experience(item['experience'])
        data_city = item['city']
        if data_city not in unique_cities:
            unique_cities.append(data_city)
            city = City(
                        name=data_city
                    )
            db.session.add(city)
        
        city_id = City.query.filter(City.name==data_city).first().id
        candidate = Candidate(
            id=item['id'],
            name=response_user_json[count]['name']['first'],
            city_id=city_id,
            minimum_experience_time=experience['minimum'],
            maximum_experience_time=experience['maximum'],
            photo_url=response_user_json[count]['picture']['large'],
            accept_remote=accept_remote(count)
        )
        for tech in item['technologies']:
            if tech['name'] not in unique_technologies:
                unique_technologies.append(tech['name'])
                technology = Technology(
                            name=tech['name']
                        )
                db.session.add(technology)
        db.session.add(candidate)

    db.session.commit()
    
    data_candidates = Candidate.query.all()
    data_technologies = Technology.query.all()

    for count, item in enumerate(data_candidates):
        if item.id == response_geek_json[count]['id']:
            for tech in response_geek_json[count]['technologies']:
                candidates_technologies = CandidateTechnology(
                    candidate_id=item.id,
                    technology_id=get_id(data_technologies, tech['name']),
                    is_main_tech=main_tech(response_geek_json[count]['technologies'], tech['name'])
                )
                db.session.add(candidates_technologies)
    db.session.commit()
    return jsonify(fake_data_geek.json())

def get_id(list_search, name):
    """[summary]
        Function to get the technology specific id.
    Args:
        list_search ([list]): [a list with technology data.]
        name ([string]): [technology name]

    Returns:
        [integer]: [return number id of technology]
    """    
    id_type = 0
    for item in list_search:
        if item.name == name:
            id_type = item.id
    return id_type

def main_tech(list_search, name):
    """[summary]
        Function to get the technology specific main_tech.
    Args:
       list_search ([list]): [a list with technology data.]
        name ([string]): [technology name]

    Returns:
        [boolean]: [return boolean main_tech]
    """    
    main_tech_boolean = False
    for item in list_search:
        if item['name'] == name:
            main_tech_boolean = item['is_main_tech']
    return main_tech_boolean

def accept_remote(number):
    """[summary]
        logical function to check if it is odd or even and return boolean from this.
    Args:
        number ([integer]): [number received]

    Returns:
        [boolean]: [Return a boolean]
    """    
    if (number % 2) == 0:
        return False
    else:
        return True

def reformule_experience(experience):
    """[summary]
        function to separate the experience string into a minimum and maximum dict
    Args:
        experience ([string]): [string experience]
    Returns:
        [dict]: [return a dict minimum and maximum experience of candidate]
    """    
  new_experience = {}
  for x in experience:
    if x == '+':      
      new_experience["minimum"] = int(experience.replace('+ years',''))
      new_experience["maximum"] = int(experience.replace('+ years',''))+1
    elif x == "-":
      new_experience["minimum"] = int(re.sub(r"(-.+)","",experience))
      correct_experience = re.sub(r"(.+-)","",experience)
      new_experience["maximum"] = int(correct_experience.replace(" years", ""))
  return new_experience