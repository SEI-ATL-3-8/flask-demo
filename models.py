from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'    
  
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return f"User: {self.email}"

  def to_json(self):
    return {
      "id": self.id,
      "email": self.email
    }
