from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
from flasgger import swag_from
import json

from sqlalchemy import text

from src.database import items, db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from src.datamodel.itemBo import itemcls
from src.utility.json_utility import json_default

item = Blueprint("item", __name__, url_prefix="/api/v1/item")

@item.get("/getItemList")
@jwt_required()
@swag_from('./docs/item/getItemList.yaml')
def getItemList():
    params = request.args
    categoryId = params.get("categoryid")
    if  categoryId != None:
        itemList = db.session.query(items).filter_by(categoryid=categoryId).all()
    else:
        itemList = db.session.query(items).from_statement(text("SELECT * FROM items where itemid>:value")).params(value=0).all()

    lst = []
    for x in itemList:
        obj = itemcls()
        obj.setObjFromOrMObj(x)
        lst.append(obj)

    jsonstr = json.dumps(lst, default=json_default, indent=4)
    return jsonstr, HTTP_200_OK


@item.post('/addItem')
@jwt_required()
@swag_from('./docs/item/addItem.yaml')
def addItem():
    categoryid = request.json['categoryid']
    qty = request.json['qty']
    imagename = request.json['imagename']
    price = request.json['price']
    itemname = request.json['itemname']

    if db.session.query(items).filter_by(itemname=itemname).first() is not None:
        return jsonify({'error': "item is already added in cart"}), HTTP_409_CONFLICT


    item = items(categoryid = categoryid, qty=qty, imagename = imagename, price = price, itemname = itemname)
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'message': "Item added in Cart",
        'item': {
            'item name': itemname
        }

    }), HTTP_201_CREATED

@item.post('/updateItem')
@swag_from('./docs/item/updateItem.yaml')
def updateItem():
    value = request.json['value']
    field = request.json['field']
    itemname = request.json['itemname']

    # here logic is that, if field is qty, it will update qty
    # and if field is price then it will update price of that item.

    if field != 'qty' and field != 'price':
        return jsonify({'error': "field property should have 'qty' or 'price' as it value"}), HTTP_409_CONFLICT

    if db.session.query(items).filter_by(itemname=itemname).first() is None:
        return jsonify({'error': "item does not exist in cart"}), HTTP_409_CONFLICT

    item = db.session.query(items).filter_by(itemname=itemname).first()
    if field == 'qty':
        item.qty = value
    elif field == 'price':
        item.price = value

    db.session.commit()

    return jsonify({
        'success': 'item updated successfully'
    }), HTTP_200_OK