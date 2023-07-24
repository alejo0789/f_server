from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    #email = db.Column(db.String(50))
    password = db.Column(db.String(150))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date_time = db.Column(db.TIMESTAMP, nullable=False)
    description = db.Column(db.Text)

def __repr__(self):
   
        return '<User %r>' % self.name


