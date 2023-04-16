from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    # email = db.Column(db.String(50), unique=True)



def __repr__(self):
   
        return '<User %r>' % self.name


