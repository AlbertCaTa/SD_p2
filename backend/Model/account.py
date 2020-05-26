from db import db

class AccountsModel(db.Model):
    __tablename__ = 'accounts'
    username = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = db.Column(db.Integer, nullable=False)
    available_money = db.Column(db.Integer)
    orders = db.relationship('OrdersModel', backref='orders', lazy=True)

    def json(self):
        return {"username":self.username, "available_money":self.available_money, "is_admin":self.is_admin}

    def save_to_db(self):
        if AccountsModel.query.get(self.username):
            db.session.commit()
            #raise UsernameTakenException("Username already taken, please choose another one")
        else:
            db.session.add(self)
            db.session.commit()

    def delete_from_db(self):
        if AccountsModel.query.get(self.username):
            db.session.delete(self)
            db.session.commit()
        else:
            raise Exception("Warning not in DB")



    @classmethod
    def find_by_username(cls, username):
        if username:
            return AccountsModel.query.filter_by(username=username).first()
        else:
            return None

    def __init__(self, username, available_money=200, is_admin=0):
        self.username = username
        self.available_money = available_money
        self.is_admin = is_admin
        self.password = 'test'

class UsernameTakenException(Exception):
    pass