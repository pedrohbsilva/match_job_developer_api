from app import db, ma
from app.models.candidate import Candidate

class Tecnology(db.Model):
  __tablename__ = 'tecnologies'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(84), nullable=False)

  def __init__(self, name):
    self.name = name
  
class TecnologySchema(ma.Schema):
  class Meta:
    fields = ('id','name')
    
tecnology_share_schema = TecnologySchema()
tecnologies_share_schema = TecnologySchema(many=True)