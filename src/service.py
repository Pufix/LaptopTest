#create a rest api without a database
from copy import deepcopy
import os
import random
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from faker import Faker
import pymongo
from pymongo.server_api import ServerApi

from cryptography.fernet import Fernet
import datetime
from dotenv import load_dotenv


uri = "mongodb+srv://alexboldas:p1tKU13PXRAvQ6oY@cluster0.jtaudyl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


fake = Faker()
myclient = pymongo.MongoClient(uri, server_api=ServerApi('1'))
mydb = myclient["Electronics"]

class Laptop:
    def __init__(self, id, name, cpu, gpu, ram, storage, price, manufacturer_id):
        self.id = id
        self.name = name
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.storage = storage
        self.price = price
        self.manufacturer_id = manufacturer_id


class Manufacturer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tokens = [] 

def validate_laptop(laptop):
    if laptop.id < 0 or laptop.price < 0:
        return False
    if laptop.name == '' or laptop.cpu == '' or laptop.gpu == '' or laptop.ram == '' or laptop.storage == '':
        return False
    return True

def getLaptopsFromDatabase():
    mycol = mydb["Laptops"]
    laptops = []
    for x in mycol.find():
        laptops.append(Laptop(x['id'], x['name'], x['cpu'], x['gpu'], x['ram'], x['storage'], x['price'], x['manufacturer_id']))
    return laptops

def getManufacturersFromDatabase():
    mycol = mydb["Manufacturers"]
    manufacturers = []
    for x in mycol.find():
        manufacturers.append(Manufacturer(x['id'], x['name']))
    return manufacturers

fernet = Fernet(b'JcdfJo6V6QThLpPAXQlzGkzcPuc3EDSjhFtrptf2WmM=')
tokens = {}

def get_users_from_db():
    mycol = mydb["Users"]
    userss = []
    for x in mycol.find():
        userss.append(User(fernet.decrypt(x['username']).decode(), fernet.decrypt(x['password']).decode()))
    return userss
    

laptops = getLaptopsFromDatabase()
manufacturers = getManufacturersFromDatabase()
app = Flask(__name__)

users=get_users_from_db()


@app.route("/createFakes", methods=['POST'])
def create_fakes():
    mycol = mydb["Laptops"]
    for i in range(10):
        laptops.append(Laptop(len(laptops)+1, fake.company(), fake.name(), fake.name(), fake.name(), fake.name(), random.randint(100, 2000), random.randint(1, len(manufacturers))))
        mycol.insert_one(deepcopy(laptops[-1]).__dict__)
    return 'Fakes created', 200


@app.route("/laptops", methods=['GET'])
def get_laptops():
    return jsonify([laptop.__dict__ for laptop in laptops]),200

@app.route("/manufacturers", methods=['GET'])
def get_manufacturers():
    return jsonify([manufacturer.__dict__ for manufacturer in manufacturers]),200

@app.route("/laptops/<int:id>", methods=['GET'])
def get_laptop(id):
    laptop = next((laptop for laptop in laptops if laptop.id == id), None)
    if laptop:
        return jsonify(laptop.__dict__), 200
    return 'Laptop not found', 404

@app.route("/manufacturers/<int:id>", methods=['GET'])
def get_manufacturer(id):
    manufacturer = next((manufacturer for manufacturer in manufacturers if manufacturer.id == id), None)
    if manufacturer:
        return jsonify(manufacturer.__dict__), 200
    return 'Manufacturer not found', 404

@app.route("/test")
def test():
    return 'Test', 200

@app.route("/laptops", methods=['POST'])
def add_laptop():
    try:
        data = request.get_json()
        new_laptop = Laptop(int(data['id']), data['name'], data['cpu'], data['gpu'], data['ram'], data['storage'], int(data['price']), int(data['manufacturer_id']))
        if not validate_laptop(new_laptop):
            return 'Invalid data', 400
        if new_laptop.id in [laptop.id for laptop in laptops]:
            return 'Laptop already exists', 400
        laptops.append(new_laptop)
        mycol = mydb["Laptops"]
        mycol.insert_one(deepcopy(new_laptop).__dict__)
        return 'ok', 201
     
    except Exception as e:
        print
        return e, 400
    
@app.route("/manufacturers", methods=['POST'])
def add_manufacturer():
    try:
        data = request.get_json()
        idd = int(data['id'])
        namee = data['name']
        new_manufacturer = Manufacturer(idd, namee)
        if new_manufacturer.id in [manufacturer.id for manufacturer in manufacturers]:
            return 'Manufacturer already exists', 400
        manufacturers.append(new_manufacturer)
        mycol = mydb["Manufacturers"]
        mycol.insert_one(deepcopy(new_manufacturer).__dict__)
        return 'ok', 201
    except:
        return 'Invalid data', 400

@app.route("/laptops", methods=['PUT'])
def update_laptop():
    try:
        data = request.get_json()
        new_laptop = Laptop(int(data['id']), data['name'], data['cpu'], data['gpu'], data['ram'], data['storage'], int(data['price']), int(data['manufacturer_id']))
        if not validate_laptop(new_laptop):
            return 'Invalid data', 400
        for laptop in laptops:
            if laptop.id == new_laptop.id:
                laptop.id = new_laptop.id
                laptop.name = new_laptop.name
                laptop.cpu = new_laptop.cpu
                laptop.gpu = new_laptop.gpu
                laptop.ram = new_laptop.ram
                laptop.storage = new_laptop.storage
                laptop.price = new_laptop.price
                laptop.manufacturer_id = new_laptop.manufacturer_id
                mycol = mydb["Laptops"]
                mycol.update_one({'id': laptop.id}, {"$set": laptop.__dict__})
                return jsonify(laptop.__dict__), 200
        return 'Laptop not found', 404
    except:
        return 'Invalid data', 400
    
@app.route("/manufacturers", methods=['PUT'])
def update_manufacturer():
    try:
        data = request.get_json()
        new_manufacturer = Manufacturer(int(data['id']), data['name'])
        for manufacturer in manufacturers:
            if manufacturer.id == new_manufacturer.id:
                manufacturer.id = new_manufacturer.id
                manufacturer.name = new_manufacturer.name
                mycol = mydb["Manufacturers"]
                mycol.update_one({'id': manufacturer.id}, {"$set": manufacturer.__dict__})
                return jsonify(manufacturer.__dict__), 200
        return 'Manufacturer not found', 404
    except:
        return 'Invalid data', 400

@app.route("/laptops/<int:id>", methods=['DELETE'])
def delete_laptop(id):
    for laptop in laptops:
        if laptop.id == id:
            laptops.remove(laptop)
            mycol = mydb["Laptops"]
            mycol.delete_one({'id': id})
            return 'Laptop deleted', 200
    return 'Laptop not found', 404

@app.route("/manufacturers/<int:id>", methods=['DELETE'])
def delete_manufacturer(id):
    for manufacturer in manufacturers:
        if manufacturer.id == id:
            manufacturers.remove(manufacturer)
            mycol = mydb["Manufacturers"]
            mycol.delete_one({'id': id})
            return 'Manufacturer deleted', 200
    return 'Manufacturer not found', 404

#push the local data to the mongodb database
@app.route("/push", methods=['POST'])
def push():
    mycol = mydb["Laptops"]
    mycol.delete_many({})
    for laptop in laptops:
        mycol.insert_one(laptop.__dict__)
    mycol = mydb["Manufacturers"]
    mycol.delete_many({})
    for manufacturer in manufacturers:
        mycol.insert_one(manufacturer.__dict__)
    return 'Data pushed to database', 200
    



#create an endpoint for login that takes username and password and return a random session key




@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    for user in users:
        if user.username == username and user.password == password:
            session_key = random.randint(1_000_000_000, 9_999_999_999)
            tokens[session_key] = datetime.datetime.now()
            user.tokens.append(session_key)
            return jsonify({'session_key': session_key}), 200
    return 'Invalid username or password', 400

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username == '' or password == '':
        return 'Invalid data', 400
    for user in users:
        if user.username == username:
            return 'Username already exists', 409
    users.append(User(username, password))
    #push to db
    mycol = mydb["Users"]
    mycol.insert_one({'username': fernet.encrypt(username.encode()), 'password': fernet.encrypt(password.encode())})

    return 'ok', 201


@app.route("/validate/<int:token>", methods=['GET'])
def validate(token):
    for user in users:
        for t in user.tokens:
            if tokens[t] + datetime.timedelta(minutes=30) < datetime.datetime.now():
                user.tokens.remove(t)
                del tokens[t]
            if t == token:
                return 'Valid', 200
    if token in tokens:
        return 'Valid', 200
    return 'Invalid', 400

@app.route("/dumpTokens", methods=['GET'])
def dumpTokens():
    return jsonify(tokens), 200

@app.route("/deleteTokens", methods=['GET'])
def deleteTokens():
    for user in users:
        user.tokens= []
    tokens.clear()
    return 'Tokens deleted', 200

@app.route('/editUser/<int:token>', methods=['PUT'])
def editUser(token):
    data = request.get_json()
    username = data['username']
    password = data['password']
    for user in users:
        for t in user.tokens:
            if t == token:
                if username == '':
                    return 'Invalid data', 400
                if password == '':
                    return 'Invalid data', 400
                mycol = mydb["Users"]
                mycol.delete_one({'username': fernet.encrypt(user.username.encode()), 'password': fernet.encrypt(user.password.encode())})
                mycol.insert_one({'username': fernet.encrypt(username.encode()), 'password': fernet.encrypt(password.encode())})
                
                user.username = username
                user.password = password

                return 'User edited', 200
    return 'Invalid token', 400





load_dotenv()
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')
CORS(app)
if __name__ == '__main__':
    get_users_from_db()
    app.run(port=5000)





































































