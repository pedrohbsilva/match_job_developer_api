from flask import jsonify, Blueprint, request
from app.models.candidate import Candidate, candidates_share_schema
from app.models.city import City
from app.models.technology import Technology
from app.models.candidate_technology import CandidateTechnology
from app import db

CANDIDATE = Blueprint('CANDIDATE', __name__,  url_prefix="/candidates")

def marshal_data(payload):
  """[summary]

  Args:
      payload ([dict]): [receives a dict with the data to be validated 
      in order to proceed with the logic.]

  Returns:
      [dict]: [returns a dict of validated data.]
  """  
  data = {
    'city':0,
    'tech':0,
    'min_exp':0,
    'max_exp':1000,
    'accept_remote': -1,
  }
  
  min_experience = payload.get('min_exp')
  max_experience = payload.get('max_exp')
  city = payload.get('city')
  tech = payload.get('tech')
  accept_remote = payload.get('accept_remote')

  if type(min_experience) == int:
    if min_experience >= 0:
      data['min_exp'] = min_experience

  if type(max_experience) == int:
    if max_experience:
      data['max_exp'] = max_experience

  if city:
    data['city'] = city

  if tech:
    data['tech'] = tech

  if accept_remote >= 0:
    if accept_remote: data['accept_remote'] = True
    else: data['accept_remote'] = False

  return data 

@CANDIDATE.route('/search_for_specific_candidates', methods=['POST'])
def search_for_specific_candidates():
  
  """[summary]
    This endpoint has the purpose of making filters according to 
    the data provided by the request.
  Returns:
      [json]: [
Return a json with all the candidate's information.
]
  """  
  
  #data provided
  data = request.json 
  #validate data provided
  data = marshal_data(data)
  
  
  #minimum experience of data provided
  min_exp = data.get('min_exp')
  #maximum experience of data provided
  max_exp = data.get('max_exp')
  #id city of data provided
  city_id = data.get('city')
  #id tech of data provided
  tech_id = data.get('tech')
  #accept_remote of data provided
  accept_remote = data.get('accept_remote')
  
  #message for response
  message = ''

  """
    query sql to get the candidate's data, 
    joining with the city table, to add the column 'name' to this table.
  """
  candidate_query = Candidate.query\
    .join(City, City.id==Candidate.city_id)\
    .add_columns(City.name)

  # returns the comparative logic between the minimum and maximum experience
  exact_experience = ((Candidate.minimum_experience_time >= min_exp)
    & (Candidate.maximum_experience_time <= max_exp))
    
  # returns the comparative logic between the minimum or maximum experience
  max_or_min_experience = ((Candidate.minimum_experience_time == max_exp)
    | (Candidate.maximum_experience_time == min_exp))

  """
  override the candidate_query variable and perform a filter 
  using the exact_experience or max_or_min_experience logic as a parameter.  
  """
  candidate_query = candidate_query.filter(
    exact_experience | max_or_min_experience
  )


  if city_id > 0:
    candidate_query = candidate_query.filter(
      (Candidate.city_id == city_id)
    )

  if accept_remote != -1:
    candidate_query = candidate_query.filter(
      (Candidate.accept_remote == accept_remote)
    )
  
  if tech_id > 0:
    candidate_query = candidate_query.join(CandidateTechnology, CandidateTechnology.candidate_id == Candidate.id)\
                   .join(Technology, Technology.id == CandidateTechnology.technology_id)\
                   .filter(CandidateTechnology.technology_id == tech_id)\
                   .order_by(CandidateTechnology.is_main_tech.desc())

  try:
    result_candidates_info = candidate_query.limit(5).all()
    if len(result_candidates_info) == 0: 
      message = 'Nenhum candidado encontrado'    
    else:
      message = 'Filtro realizado com sucesso'
  except:
    message = 'Nenhum candidado encontrado'
    return jsonify({"message": message, "candidates": []}), 404


  result_candidates_technologies = Candidate.query\
    .join(CandidateTechnology, CandidateTechnology.candidate_id==Candidate.id)\
    .join(Technology, Technology.id==CandidateTechnology.technology_id)\
    .add_columns(Technology.name, CandidateTechnology.is_main_tech)

  result_candidates_technologies = result_candidates_technologies.all()
  all_candidates = []

  #Loop for generate Json body
  for count, info in enumerate(result_candidates_info):
    experience_candidate = str(info.Candidate.minimum_experience_time)+" e "+str(info.Candidate.maximum_experience_time)
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
  
  """[summary]

  Args:
      candidates_technologies ([list]): [tuple list with the candidate's information and technologies.]
      candidate_id ([integer]): [candidate' id]

  Returns:
      [list]: [return dict list with technologies]
  """
  
  technologies = []
  main_technologies = []
  secondary_technologies = []
  for item in candidates_technologies:
    if item.Candidate.id == candidate_id:
      tech = {"is_main_tech": item.is_main_tech, "name": item.name}
      if item.is_main_tech:
        main_technologies.append(tech)
      else:
        secondary_technologies.append(tech)
  secondary_technologies = sorted(secondary_technologies, key=lambda k: k['name'])

  technologies = main_technologies + secondary_technologies
    
  return technologies 
