from flask import jsonify, Blueprint, request
from app.models.candidate import Candidate
from app.models.city import City
from app.models.tecnology import Tecnology
from app.models.candidates_in_city import CandidatesInCity
from app.models.candidate_tecnology import CandidateTecnology
from app import db

CANDIDATE = Blueprint('CANDIDATE', __name__,  url_prefix="/candidates")

@CANDIDATE.route('/search_all_candidates', methods=['GET'])
def search_all_candidates():
  
  #teste = CandidateTecnology.query.join(Candidate, CandidateTecnology.candidate_id==Candidate.id).all()
  candidates_info = Candidate.query\
    .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
    .join(City, City.id==CandidatesInCity.city_id)\
    .add_columns(Candidate.id, City.name).limit(5).all()
  
  candidates_tecnologies = Candidate.query\
    .join(CandidateTecnology, CandidateTecnology.candidate_id==Candidate.id)\
    .join(Tecnology, Tecnology.id==CandidateTecnology.tecnology_id)\
    .add_columns(Tecnology.name, CandidateTecnology.is_main_tech).all()
      
  all_candidates = []
  for info in candidates_info:
    all_candidates.append(
      {"candidate_id": info.Candidate.id, 
       "candidate_name": info.Candidate.name,
       "candidate_photo": info.Candidate.photo_url,
       "city_name": info.name, 
       "experience": info.Candidate.experience,
       "accept_remote": info.Candidate.accept_remote,
       "technologies": search_candidate_technologies(candidates_tecnologies, info.Candidate.id)
      })
    
  return jsonify(all_candidates)

def search_candidate_technologies(candidates_tecnologies, candidate_id):
  technologies = []
  for item in candidates_tecnologies:
    if item.Candidate.id == candidate_id:
      technologies.append({"is_main_tech": item.is_main_tech, "name": item.name})
       
  return technologies    
  
# @CANDIDATE.route('/search_for_specific_candidates', methods=['GET'])
# def search_for_specific_candidates():
  
#   city = request.args.get('city')
#   tech = request.args.get('technologies')
#   experience = request.args.get('experience')
#   accept_remote = request.args.get('accept_remote')

#   candidates_info = Candidate.query\
#     .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
#     .join(City, City.id==CandidatesInCity.city_id)
    
#   if city != '':
#     candidates_info.filter

#   if (city == '') and (tech == '') and (experience == '') and (accept_remote == ''): 
#     #Not filter   
#     candidates_info = Candidate.query\
#       .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
#       .join(City, City.id==CandidatesInCity.city_id).all()

#   if (city != '') and (tech == '') and (experience == '') and (accept_remote == ''):   
#     #Only filter by City 
#     candidates_info = Candidate.query\
#       .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
#       .join(City, City.id==CandidatesInCity.city_id)\
#       .filter(City.id == city)\
#       .all()
#     print(candidates_info)
  
#   if (tech != '') and (city == '') and (experience == '') and (accept_remote == ''):   
#     #Only filter by Tech
#     tech_id_or_ids = tech.split(',')
    
#     candidates_info = Candidate.query\
#       .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
#       .join(City, City.id==CandidatesInCity.city_id)\
#       .add_columns(Candidate.id, City.name).limit(5).all()
    
#     candidates_tecnologies = Candidate.query\
#       .join(CandidateTecnology, CandidateTecnology.candidate_id==Candidate.id)\
#       .join(Tecnology, Tecnology.id==CandidateTecnology.tecnology_id)\
#       .filter(Tecnology.id.in_(tech_id_or_ids))\
#       .add_columns(Tecnology.name, CandidateTecnology.is_main_tech).all()
  
#     print(candidates_tecnologies)
  
#   else:
#     print('tchau')
#   # teste = request.args.to_dict()
#   # for count, index in enumerate(teste):
#   #   print(index)
#   #   print(request.args.get(index))
  
#   # candidates_info = Candidate.query\
#   #   .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
#   #   .join(City, City.id==CandidatesInCity.city_id)\
#   #   .filter(Candidate.experience == experience_text)\
#   #   .add_columns(Candidate.id, City.name, Candidate.experience).all()
  
#   return 'oi'

# def search_candidate_technologies(candidates_tecnologies, candidate_id):
#   technologies = []
#   for item in candidates_tecnologies:
#     if item.Candidate.id == candidate_id:
#       technologies.append({"is_main_tech": item.is_main_tech, "name": item.name})
       
#   return technologies  