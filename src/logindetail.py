import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required


from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from src.database import logindetail, db
from flasgger import swag_from

logind = Blueprint("logindetail", __name__, url_prefix="/api/v1/login")

@logind.post('/logindetail')
@jwt_required()
@swag_from('./docs/login/logindetail.yaml')
def addLoginDetail():
    userid = request.json['userid']
    browser = request.environ['HTTP_USER_AGENT']
    logindate = datetime.datetime.utcnow()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']  # if behind a proxy

    login = logindetail(userid=userid, logoutdate = None, browser= browser, ip_address = ip_address, logindate = logindate)
    db.session.add(login)
    db.session.commit()

    return jsonify({
        'message': "User details added successfully in system",
        'user': {
            'userId': userid
        }
    }), HTTP_200_OK

@logind.post('/logout')
@jwt_required()
@swag_from('./docs/login/logout.yaml')
def logout():
    loginid = request.json['loginid']
    logoutdate = datetime.datetime.utcnow()
    loginobj = logindetail.query.filter_by(loginid=loginid).first()
    loginobj.logoutdate = logoutdate
    db.session.commit()

    return jsonify({
        'message': "User successfully logout from system",
        'user': {
            'loginid': loginid
        }
    }), HTTP_200_OK
