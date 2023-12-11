from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement=True) 
    account = db.Column('account', db.String(20), unique = True)
    password = db.Column('password', db.String(20))

    def __init__(self, account, password):
        self.account = account
        self.password = password
        
    def check_password(self, password):
        if(self.password == password):
            return True
        return False
        
