from flask import jsonify, Blueprint, request
from app.models.candidate import Candidate, candidates_share_schema
from app.models.city import City
from app.models.technology import Technology
from app.models.candidate_technology import CandidateTechnology
from app import db
from sqlalchemy import text

CANDIDATE = Blueprint('CANDIDATE', __name__,  url_prefix="/candidates")

def marshal_data(payload):
  """ Validação dos dados """ 
  data = {
    'city':0,
    'tech':0,
    'min_experience':0,
    'max_experience':1000,
    'accept_remote': 2,
  }
  
  min_experience = data.get('min_experience')
  max_experience = data.get('max_experience')
  city = data.get('city')
  tech = data.get('tech')
  accept_remote = data.get('accept_remote')
  if payload.get('min_experience'):
    data['min_experience'] = payload.get('min_experience')
  if payload.get('max_experience'):
    data['max_experience'] = payload.get('max_experience')
  if payload.get('city'):
    data['city'] = payload.get('city') 
  if payload.get('tech'):
    data['tech'] = payload.get('tech')
  if payload.get('accept_remote') >= 2:
    data['accept_remote'] = data['accept_remote']
  elif payload.get('accept_remote') <= 1:    
    data['accept_remote'] = payload.get('accept_remote')
    
  return data 

@CANDIDATE.route('/search_for_specific_candidates', methods=['POST'])
def search_for_specific_candidates():
  
  data = request.json 
  data = marshal_data(data)

  min_exp = data.get('min_experience')
  max_exp = data.get('max_experience')
  city_id = data.get('city')
  tech_id = data.get('tech')
  accept_remote = data.get('accept_remote')
  message = ''

  candidate_query = Candidate.query\
    .join(City, City.id==Candidate.city_id)\
    .add_columns(City.name)
  result_candidates_technologies = Candidate.query\
    .join(CandidateTechnology, CandidateTechnology.candidate_id==Candidate.id)\
    .join(Technology, Technology.id==CandidateTechnology.technology_id)\
    .add_columns(Technology.name, CandidateTechnology.is_main_tech)
    
  if min_exp >= 0 and max_exp <=13:
    candidate_query = candidate_query.filter(((Candidate.maximum_experience_time == max_exp) 
                                | (Candidate.maximum_experience_time == min_exp)) 
                                | ((Candidate.minimum_experience_time == min_exp) 
                                | (Candidate.minimum_experience_time == max_exp)))

  if city_id > 0:
    candidate_query = candidate_query.filter(
      (Candidate.city_id == city_id)
    )
  if accept_remote <= 1:
    candidate_query = candidate_query.filter(
      (Candidate.accept_remote == (True if accept_remote == 1 else False))
    )

  if tech_id > 0:
    candidate_query = candidate_query.join(CandidateTechnology, CandidateTechnology.candidate_id == Candidate.id)\
                   .join(Technology, Technology.id == CandidateTechnology.technology_id)\
                   .filter(CandidateTechnology.technology_id == tech_id)

  try:
    result_candidates_info = candidate_query.limit(5).all()
    if len(result_candidates_info) == 0: 
      message = 'Nenhum candidado encontrado'    
    else:
      message = 'Filtro realizado com sucesso'
  except:
    message = 'Nenhum candidado encontrado'
    return jsonify({"message": message, "candidates": []}), 404
    
  result_candidates_technologies = result_candidates_technologies.all()
  all_candidates = []

  for count, info in enumerate(result_candidates_info):
    experience_candidate = str(info.Candidate.minimum_experience_time)+"-"+str(info.Candidate.maximum_experience_time)
    all_candidates.append(
      {"candidate_id": info.Candidate.id, 
        "candidate_name": info.Candidate.name,
        "candidate_photo": info.Candidate.photo_url,
        "experience": experience_candidate,
        "city_name": info.name, 
        "accept_remote": info.Candidate.accept_remote,
        "technologies": search_candidate_technologies(result_candidates_technologies, info.Candidate.id)
      })

  return jsonify({"message": message}, {"candidates":all_candidates}), 200

def search_candidate_technologies(candidates_technologies, candidate_id):
  technologies = []
  for item in candidates_technologies:
    if item.Candidate.id == candidate_id:
      technologies.append({"is_main_tech": item.is_main_tech, "name": item.name})
       
  return technologies 
