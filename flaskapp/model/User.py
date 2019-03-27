from flaskapp import db
import bcrypt
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)  
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    mobilePhone = db.Column(db.String(8), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)

    #Overriding the db.Model constructor
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        # do custom initialization here
        plainpass = bytes(kwargs['password'], encoding='utf-8')
        self.password = bcrypt.hashpw(plainpass, bcrypt.gensalt())

    @staticmethod
    def findUserByIC(userICQuery):
        return User.query.filter_by(userIC=userICQuery).first()