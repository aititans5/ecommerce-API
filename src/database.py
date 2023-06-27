from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class userdetail(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.Date, onupdate=datetime.datetime.utcnow())
    activeuser = db.Column(db.String(1), unique=True, nullable=False)




class logindetail(db.Model):
    loginid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    logindate = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    logoutdate = db.Column(db.DateTime, nullable= True)
    browser = db.Column(db.String(250), nullable = False)
    ip_address = db.Column(db.String(250), nullable = False)

# class to define item table.
class items(db.Model):
    itemid = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    imagename = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Double, nullable=False)
    itemname = db.Column(db.String(500), unique=True, nullable=False)
