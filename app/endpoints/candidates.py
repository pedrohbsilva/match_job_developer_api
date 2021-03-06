from flask import jsonify, Blueprint, request
from app.models.candidate import Candidate
from app.models.city import City
from app.models.tecnology import Tecnology
from app.models.candidates_in_city import CandidatesInCity
from app.models.candidate_tecnology import CandidateTecnology
from app import db

CANDIDATE = Blueprint('CANDIDATE', __name__,  url_prefix="/candidates")
 
@CANDIDATE.route('/search_for_specific_candidates', methods=['GET'])
def search_for_specific_candidates():
  
  city = request.args.get('city')
  tech = request.args.get('technologies')
  experience = request.args.get('experience')
  accept_remote = request.args.get('accept_remote')
  message = ''
  
  candidates_info = Candidate.query\
    .join(CandidatesInCity, CandidatesInCity.candidate_id==Candidate.id)\
    .join(City, City.id==CandidatesInCity.city_id)\
    .add_columns(Candidate.id, City.name)
  
  candidates_tecnologies = Candidate.query\
    .join(CandidateTecnology, CandidateTecnology.candidate_id==Candidate.id)\
    .join(Tecnology, Tecnology.id==CandidateTecnology.tecnology_id)\
    .add_columns(Tecnology.name, CandidateTecnology.is_main_tech)

  result_candidates_info = []
  result_candidates_tecnologies = []
  
  if (city == '') and (tech == '') and (experience == '') and (accept_remote == ''):
    message = 'Resultados sem filtros aplicados.'
    result_candidates_info = candidates_info.order_by(Candidate.maximum_experience_time.desc()).limit(5).all()
    result_candidates_tecnologies = candidates_tecnologies.all()

  if (city == '') and (tech == '') and (experience != '') and (accept_remote == ''):
    message = 'Resultados com filtro de experiência aplicado.'
    if ',' in experience:
      get_experience = experience.split(",")
      result_candidates_info = candidates_info\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      message = 'Resultados com filtro de experiência aplicado.'
      result_candidates_info = candidates_info\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
         
  if (city != '') and (tech == '') and (experience == '') and (accept_remote == ''):
    message = 'Resultados com filtro de cidade aplicado.'
    result_candidates_info = candidates_info.filter(City.id == city).limit(5).all()
    result_candidates_tecnologies = candidates_tecnologies.all()

  if (tech != '') and (city == '') and (experience == '') and (accept_remote == ''):   
    message = 'Resultados com filtro de tecnologia aplicado.'
    tech_id_or_ids = tech.split(',')
    result_candidates_info = candidates_info\
                              .join(CandidateTecnology, CandidateTecnology.candidate_id == Candidate.id)\
                              .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                              .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), Candidate.id == CandidateTecnology.candidate_id)\
                              .limit(5).all()
    
    result_candidates_tecnologies = candidates_tecnologies.all()

  if (tech == '') and (city == '') and (experience == '') and (accept_remote != ''): 
    message = 'Resultados com filtro de trabalho remoto aplicado.'
    result_candidates_info = candidates_info\
                              .filter(Candidate.accept_remote == accept_remote)\
                              .limit(5).all()
    
    result_candidates_tecnologies = candidates_tecnologies.all()
  
  if (city == '') and (tech == '') and (experience != '') and (accept_remote != ''):
    message = 'Resultados com filtro de experiência e acesso remoto aplicado.'
    if ',' in experience:
      get_experience = experience.split(",")
      result_candidates_info = candidates_info\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      result_candidates_info = candidates_info\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
      
  if (city != '') and (tech == '') and (experience != '') and (accept_remote == ''):
    message = 'Resultados com filtro de experiência e de cidade aplicado.'
    if ',' in experience:
      get_experience = experience.split(",")
      result_candidates_info = candidates_info\
                                .filter(City.id == city)\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      result_candidates_info = candidates_info\
                                .filter(City.id == city)\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()

  if (city == '') and (tech != '') and (experience != '') and (accept_remote == ''):
    message = 'Resultados com filtro de experiência e de tecnologia aplicado.'
    if ',' in experience:
      get_experience = experience.split(",")
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), Candidate.id == CandidateTecnology.candidate_id)\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), 
                                        Candidate.id == CandidateTecnology.candidate_id)\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()

  if (city != '') and (tech == '') and (experience == '') and (accept_remote != ''): 
    message = 'Resultados com filtro de trabalho remoto e cidade aplicado.'
    result_candidates_info = candidates_info\
                              .filter(Candidate.accept_remote == accept_remote, City.id == city)\
                              .limit(5).all()
    
    result_candidates_tecnologies = candidates_tecnologies.all()

  if (city == '') and (tech != '') and (experience == '') and (accept_remote != ''): 
    message = 'Resultados com filtro de trabalho remoto e tecnologia.'
    tech_id_or_ids = tech.split(',')
    result_candidates_info = candidates_info\
                              .join(CandidateTecnology, CandidateTecnology.candidate_id == Candidate.id)\
                              .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                              .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), Candidate.id == CandidateTecnology.candidate_id)\
                              .filter(Candidate.accept_remote == accept_remote)\
                              .limit(5).all()
    
    result_candidates_tecnologies = candidates_tecnologies.all()

  if (tech != '') and (city != '') and (experience == '') and (accept_remote == ''): 
    message = 'Resultados com filtro de cidade e tecnologia aplicado.'
    tech_id_or_ids = tech.split(',')
    result_candidates_info = candidates_info\
                              .join(CandidateTecnology, CandidateTecnology.candidate_id == Candidate.id)\
                              .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                              .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids))\
                              .filter(City.id == city)\
                              .limit(5).all()
    
    result_candidates_tecnologies = candidates_tecnologies.all()

  if (city != '') and (tech != '') and (experience == '') and (accept_remote != ''): 
    message = 'Resultados com filtro de trabalho remoto, tecnologia e cidade aplicado.'
    tech_id_or_ids = tech.split(',')
    result_candidates_info = candidates_info\
                              .join(CandidateTecnology, CandidateTecnology.candidate_id == Candidate.id)\
                              .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                              .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids))\
                              .filter(City.id == city)\
                              .filter(Candidate.accept_remote == accept_remote)\
                              .limit(5).all()
    
    result_candidates_tecnologies = candidates_tecnologies.all()
  
  if (city != '') and (tech != '') and (experience != '') and (accept_remote == ''):
    message = 'Resultados com filtro de experiência, tecnologia e cidade aplicado.'
    if ',' in experience:
      get_experience = experience.split(",")
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), Candidate.id == CandidateTecnology.candidate_id)\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .filter(City.id == city)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), 
                                        Candidate.id == CandidateTecnology.candidate_id)\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .filter(City.id == city)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
  if (city == '') and (tech != '') and (experience != '') and (accept_remote != ''):
    message = 'Resultados com filtro de experiência, tecnologia e trabalho remoto aplicado.'    
    if ',' in experience:
      get_experience = experience.split(",")
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), Candidate.id == CandidateTecnology.candidate_id)\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), 
                                        Candidate.id == CandidateTecnology.candidate_id)\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    
  if (city != '') and (tech == '') and (experience != '') and (accept_remote != ''):
    message = 'Resultados com filtro de experiência, cidade e trabalho remoto aplicado.'        
    if ',' in experience:
      get_experience = experience.split(",")
      result_candidates_info = candidates_info\
                                .filter(City.id == city)\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      result_candidates_info = candidates_info\
                                .filter(City.id == city)\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    
  if (city != '') and (tech != '') and (experience != '') and (accept_remote != ''):
    message = 'Resultados com todos os filtros aplicados.'        
    if ',' in experience:
      get_experience = experience.split(",")
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), Candidate.id == CandidateTecnology.candidate_id)\
                                .filter(((Candidate.maximum_experience_time == get_experience[1]) 
                                | (Candidate.maximum_experience_time == get_experience[0])) 
                                | ((Candidate.minimum_experience_time == get_experience[0]) 
                                | (Candidate.minimum_experience_time == get_experience[1])))\
                                .filter(City.id == city)\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()
    else:
      tech_id_or_ids = tech.split(',')
      result_candidates_info = candidates_info\
                                .join(CandidateTecnology, 
                                      CandidateTecnology.candidate_id == Candidate.id)\
                                .join(Tecnology, Tecnology.id == CandidateTecnology.tecnology_id)\
                                .filter(CandidateTecnology.tecnology_id.in_(tech_id_or_ids), 
                                        Candidate.id == CandidateTecnology.candidate_id)\
                                .filter((Candidate.minimum_experience_time == experience) 
                                | (Candidate.maximum_experience_time == experience))\
                                .filter(City.id == city)\
                                .filter(Candidate.accept_remote == accept_remote)\
                                .limit(5).all()
      result_candidates_tecnologies = candidates_tecnologies.all()

  all_candidates = []
  if len(result_candidates_info) == 0:
      return jsonify({"message": "Nenhum candidato com estes filtros", "candidates": []}), 200
  else: 
    for count, info in enumerate(result_candidates_info):
      experience_candidate = str(info.Candidate.minimum_experience_time)+"-"+str(info.Candidate.maximum_experience_time)
      all_candidates.append(
        {"candidate_id": info.Candidate.id, 
          "candidate_name": info.Candidate.name,
          "candidate_photo": info.Candidate.photo_url,
          "city_name": info.name, 
          "experience": experience_candidate,
          "accept_remote": info.Candidate.accept_remote,
          "technologies": search_candidate_technologies(result_candidates_tecnologies, info.Candidate.id)
        })

      
    return jsonify({"message": message}, {"candidates":all_candidates}), 200

def search_candidate_technologies(candidates_tecnologies, candidate_id):
  technologies = []
  for item in candidates_tecnologies:
    if item.Candidate.id == candidate_id:
      technologies.append({"is_main_tech": item.is_main_tech, "name": item.name})
       
  return technologies 
