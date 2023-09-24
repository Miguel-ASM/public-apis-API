from db import db
from pgvector.sqlalchemy import Vector

class Api(db.Model):
  __tablename__ = 'apis'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  category = db.Column(db.String())
  description = db.Column(db.String())
  url = db.Column(db.String())
  cors = db.Column(db.String())
  https = db.Column(db.String())
  auth = db.Column(db.String())
  embedding = db.Column(Vector(1536))