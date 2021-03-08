from app import db, ma
from app.models.candidate import Candidate
from app.models.technology import Technology

class CandidateTechnology(db.Model):
  __tablename__ = 'candidate_technologies'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  candidate_id = db.Column(db.Integer, db.ForeignKey(Candidate.id), nullable=False)
  technology_id = db.Column(db.Integer, db.ForeignKey(Technology.id), nullable=False)
  is_main_tech = db.Column(db.Boolean, nullable=False)

  def __init__(self, candidate_id, technology_id, is_main_tech):
    self.candidate_id = candidate_id
    self.technology_id = technology_id
    self.is_main_tech = is_main_tech
  
class CandidateTechnologySchema(ma.Schema):
  class Meta:
    fields = ('id','candidate_id', 'technology_id', 'is_main_tech')
    
candidate_technologies_share_schema = CandidateTechnologySchema()
candidates_technologies_share_schema = CandidateTechnologySchema(many=True)