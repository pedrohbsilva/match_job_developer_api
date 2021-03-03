from app import db, ma

class City(db.Model):
  __tablename__ = 'cities'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(84), nullable=False)

  def __init__(self, name):
    self.name = name
  
class CitySchema(ma.Schema):
  class Meta:
    fields = ('id', 'name')
    
city_share_schema = CitySchema()
cities_share_schema = CitySchema(many=True)