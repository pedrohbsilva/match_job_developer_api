from app import db, ma
from app.models.candidate import Candidate
from app.models.tecnology import Tecnology

class CandidateTecnology(db.Model):
  __tablename__ = 'candidate_tecnologies'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  candidate_id = db.Column(db.Integer, db.ForeignKey(Candidate.id), nullable=False)
  tecnology_id = db.Column(db.Integer, db.ForeignKey(Tecnology.id), nullable=False)
  is_main_tech = db.Column(db.Boolean, nullable=False)

  def __init__(self, candidate_id, tecnology_id, is_main_tech):
    self.candidate_id = candidate_id
    self.tecnology_id = tecnology_id
    self.is_main_tech = is_main_tech
  
class CandidateTecnologySchema(ma.Schema):
  class Meta:
    fields = ('id','candidate_id', 'tecnology_id', 'is_main_tech')
    
candidate_tecnologies_share_schema = CandidateTecnologySchema()
candidates_tecnologies_share_schema = CandidateTecnologySchema(many=True)