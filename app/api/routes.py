from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Whiskey, whiskey_schema, whiskeys_schema

api = Blueprint('api',__name__, url_prefix='/api')   

@api.route('/getdata')
def getdata():
    return {'yee':'haa'}

@api.route('/collection',methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    type = request.json['type']
    age = request.json['age']
    region = request.json['region']
    user_token = current_user_token.token
    
    print(f'BIG TESTER: {current_user_token.token}')
    
    car = Whiskey(name,type,age,region,user_token=user_token)
    
    db.session.add(car)
    db.session.commit()
    
    response = whiskey_schema.dump(car)
    return jsonify(response)

@api.route('/collection', methods =['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    cars = Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskeys_schema.dump(cars)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    car = Whiskey.query.get(id)
    response = whiskey_schema.dump(car)
    return jsonify(response)


#Updating

@api.route('/collection/<id>',methods = ['POST','PUT'])
@token_required
def update_contact (current_user_token, id):
    car = Whiskey.query.get(id)
    car.name = request.json['name']
    car.type = request.json['type']
    car.age = request.json['age']
    car.region = request.json['region']
    car.user_token = current_user_token.token
    
    db.session.commit()
    response = whiskey_schema.dump(car)
    return jsonify(response)




#Delete
@api.route('/collection/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    car = Whiskey.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = whiskey_schema.dump(car)
    return jsonify(response)