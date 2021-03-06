from app import db, ma
from app.models.city import City 

class Candidate(db.Model):
  __tablename__ = 'candidates'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(84), nullable=False)
  city_id = db.Column(db.Integer, db.ForeignKey(City.id), nullable=False)
  minimum_experience_time = db.Column(db.Integer, nullable=False)
  maximum_experience_time = db.Column(db.Integer, nullable=False)
  photo_url = db.Column(db.String(400), nullable=False)
  accept_remote = db.Column(db.Boolean, nullable=False)
  
  def __init__(self, id, name, city_id, minimum_experience_time, maximum_experience_time, photo_url, accept_remote):
    self.id = id
    self.name = name
    self.city_id = city_id
    self.minimum_experience_time = minimum_experience_time
    self.maximum_experience_time = maximum_experience_time
    self.photo_url = photo_url
    self.accept_remote = accept_remote
  
class CandidateSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'city_id', 'minimum_experience_time', 'maximum_experience_time', 'photo_url', 'accept_remote')
    
candidate_share_schema = CandidateSchema()
candidates_share_schema = CandidateSchema(many=True)