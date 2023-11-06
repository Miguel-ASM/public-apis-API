from db import db
from pgvector.sqlalchemy import Vector
from datetime import datetime

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

class ApisRepoCommit(db.Model):
  __tablename__ = 'apis_repo_commits'
  id = db.Column(db.Integer, primary_key=True)
  sha = db.Column(db.String(), nullable=False )
  created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)