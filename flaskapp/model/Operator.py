from flaskapp import db
from sqlalchemy import ForeignKey
import bcrypt
from flaskapp.model.User import User

class Operator(User):

    # Set table name
    __tablename__ = 'operator'

    __mapper_args__ = {
        'polymorphic_identity':'operator',
    }

    #Overriding the db.Model constructor
    
    
    operatorid = db.Column(db.Integer, ForeignKey('user.uid'), primary_key=True)

    def getClaimsOfUser(self):
        return{
            "id":self.operatorid,
            'role': 'operator'
        }