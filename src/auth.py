import json
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
import datetime

from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from src.database import userdetail, db
from src.datamodel.userdetailBo import userdetailcls
from src.utility.json_utility import json_default
from src.utility import sendemail

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    name =  request.json['name']
    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if db.session.query(userdetail).filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if db.session.query(userdetail).filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = userdetail(username=username, password=pwd_hash, email=email, name=name, activeuser='Y',created_at = datetime.datetime.utcnow())
    db.session.add(user)
    msg = "User has registered successfully with username- " + username;
    sendemail.sendPlainTextEmail(email, msg)
    db.session.commit()
    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
        }
    }), HTTP_201_CREATED


@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    user = db.session.query(userdetail).filter_by(email=email, activeuser='Y').first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.userid)
            access = create_access_token(identity=user.userid)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email,
                    'userid' : user.userid
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED

@auth.post('/change_password')
@swag_from('./docs/auth/changePassword.yaml')
def change_password():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    new_password = request.json.get('new_password', '')

    user = db.session.query(userdetail).filter_by(email=email, activeuser='Y').first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            pwd_hash = generate_password_hash(new_password)
            user.password = pwd_hash
            user.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            return jsonify({
                'success': 'password changed successfully'
            }), HTTP_200_OK
        else:
            return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED
    else:
        return jsonify({'error': 'User Not Found with this email'}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.query(userdetail).filter_by(userid=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK

@auth.get("/getAllActiveUser")
@swag_from('./docs/auth/allactiveUser.yaml')
def getAllActiveUser():
    activeusers = db.session.query(userdetail).filter_by(activeuser='Y').all()
    lst = []
    for x in activeusers:
        obj = userdetailcls()
        obj.setObjFromOrMObj(x)
        lst.append(obj)

    jsonstr = json.dumps(lst, default=json_default, indent=4)
    return jsonstr, HTTP_200_OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK,
