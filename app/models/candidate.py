from app import db, ma

class Candidate(db.Model):
  __tablename__ = 'candidates'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(84), nullable=False)
  photo_url = db.Column(db.String(400), nullable=False)
  experience = db.Column(db.String(84), nullable=False)
  accept_remote = db.Column(db.Boolean, nullable=False)


  def __init__(self, id, name, photo_url, experience, accept_remote):
    self.id = id
    self.name = name
    self.photo_url = photo_url
    self.experience = experience
    self.accept_remote = accept_remote
  
class CandidateSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'photo_url', 'experience', 'accept_remote')
    
candidate_share_schema = CandidateSchema()
candidates_share_schema = CandidateSchema(many=True)