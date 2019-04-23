from application import db
from application.models import Base

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

    def set_role(self, role):
        r = Role.findRole(role)
        self.role_id = r.id
        db.session().commit()

    def get_role(self):
        return Role.get_role(self.role_id)
    
class Role(Base):
    __tablename__ = "role"

    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = name
    
    def get_id(self):
        return self.id

    @staticmethod
    def get_role(role_id):
        r = Role.query.filter_by(id=role_id).first()
        return r.name

    @staticmethod
    def findRole(name):
        if not name:
            return
        name = name.lower().strip()
        r = Role.query.filter_by(name=name).first()

        if not r:
            r = Role(name)
            db.session().add(r)
            db.session().commit()
            return Role.findRole(name)
            
        return r
