from flaskapp import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import with_polymorphic
import bcrypt
from flask import jsonify

class User(db.Model):
    # Set table name
    __tablename__ = 'user'

    userid = db.Column(db.Integer, primary_key=True)
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    discriminator = db.Column('type', db.String(50))

       #Overriding the db.Model constructor
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        # do custom initialization here
        plainpass = bytes(kwargs['password'], encoding='utf-8')
        self.password = bcrypt.hashpw(plainpass, bcrypt.gensalt())

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':discriminator
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def findUserByIC(userICQuery):
        from .Operator import Operator
        entity = with_polymorphic(User, Operator)
        return db.session.query(entity).filter_by(userIC = userICQuery).first()
    
    @staticmethod
    def authenticate(userIC, password):
        user = User.findUserByIC(userIC)
        if user and bcrypt.checkpw(bytes(password,encoding='utf-8'), bytes(user.password,encoding='utf-8')):
            return user
        else:
            return False