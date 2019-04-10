from flaskapp import db
from sqlalchemy import ForeignKey
import bcrypt
from flaskapp.model.User import User

class GovernmentOfficial(User):

    # Set table name
    __tablename__ = 'governmentofficial'

    __mapper_args__ = {
        'polymorphic_identity':'government',
    }

    #Overriding the db.Model constructor
    
    
    governmentid = db.Column(db.Integer, ForeignKey('user.uid'), primary_key=True)

    def getClaimsOfUser(self):
        parentClaim = super().getClaimsOfUser()
        childClaim = {
            "governmentid":self.governmentid,
            'type': super().discriminator
        }
        return {**parentClaim, **childClaim}