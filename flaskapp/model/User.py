from flaskapp import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import with_polymorphic
import bcrypt
class User(db.Model): #all table need to extend db.Model
    __tablename__='user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)  #nullable = cannot be null
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    discriminator = db.Column('type', db.String(50))

    #Overriding the db.Model constructor 
    #init is a constructor in python
    #kwargs the no. of parameter can be infinity, it must be in terms of dictionary. it must be key value pair
    def __init__(self, **kwargs): 
        #if is args den is a set
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

    # read sqlalchemy documentation
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