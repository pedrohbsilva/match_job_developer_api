from app import db, ma
from app.models.candidate import Candidate
from app.models.city import City

class CandidatesInCity(db.Model):
  __tablename__ = 'candidates_in_city'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  candidate_id = db.Column(db.Integer, db.ForeignKey(Candidate.id), nullable=False)
  city_id = db.Column(db.Integer, db.ForeignKey(City.id), nullable=False)

  def __init__(self, candidate_id, city_id):
    self.candidate_id = candidate_id
    self.city_id = city_id
  
class CandidatesInCitySchema(ma.Schema):
  class Meta:
    fields = ('id','candidate_id', 'city_id')
    
candidate_in_city_share_schema = CandidatesInCitySchema()
candidates_in_city_share_schema = CandidatesInCitySchema(many=True)