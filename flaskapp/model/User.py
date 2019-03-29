from flaskapp import db
import bcrypt
class User(db.Model): #all table need to extend db.Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)  #nullable = cannot be null
    userIC = db.Column(db.String(9), unique=True, nullable=False)
    mobilePhone = db.Column(db.String(8), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)

    #Overriding the db.Model constructor #init is a constructor in python
    def __init__(self, **kwargs): #kwargs the no. of parameter can be infinity, it must be in terms of dictionary. it must be key value pair
        super(User, self).__init__(**kwargs) #if is args den is a set

        # do custom initialization here
        plainpass = bytes(kwargs['password'], encoding='utf-8')
        self.password = bcrypt.hashpw(plainpass, bcrypt.gensalt())

    #read sqlalchemy documentation
    @staticmethod
    def findUserByIC(userICQuery):
        return User.query.filter_by(userIC=userICQuery).first()