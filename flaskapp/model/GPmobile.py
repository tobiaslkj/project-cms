from flaskapp import db
from sqlalchemy.orm import relationship

class GPMobile(db.Model):
    __tablename__='gp_mobile'
    mobilePhone = db.Column(db.String(8), primary_key=True)
    postalCode = db.Column(db.String(10), unique=False, nullable=False)
    
    def __init__(self, **kwargs):
        super(GPMobile, self).__init__(**kwargs)