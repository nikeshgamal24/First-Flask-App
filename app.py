from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

# create instance of flask app
app = Flask(__name__)

# connection to the db 
app.config['SQlALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy (app)

# making models --> tables
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integers, primary=True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)

def json(self):
    return {"id":self.id, "username":self.username, "email":self.email}

# initialize databse
db.create_all()

# creating routes to populate and manipulate the tables 
# creating a test route to check only whether the route apis are up or not
@app.route('/test',method=['GET'])
def test():
    return make_response(jsonify({'message':'test route working'}),200)

#create user route
@app.route('/user/create',method=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username = data["username"],email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message":"User created successfully","user":new_user}),201)
    except e:
        return make_response(jsonify({"message":"Error creating user"}),400)

#get all user route
@app.route('/user/users',method=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({"users":[user.json for user in users]}),201)
    except  e:
        return make_response(jsonify({"message":"Error getting users"}),400)
    
#get user by id route
@app.route('/user/<int:id>',method=['GET'])
def get_users():
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({"user":user}),200)
        return make_response(jsonify({"message":"user not found"}),404)
    except  e:
        return make_response(jsonify({"message":"Error getting users"}),400)