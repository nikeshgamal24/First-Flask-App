from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

# create instance of flask app
app = Flask(__name__)

# connection to the db
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# making models --> tables
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}

# initialize database
with app.app_context():
    db.create_all()

# creating routes to populate and manipulate the tables
# creating a test route to check only whether the route apis are up or not
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route working'}), 200)

# create user route
@app.route('/user/create', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "User created successfully", "user": new_user.json()}), 201)
    except Exception as e:
        return make_response(jsonify({"message": "Error creating user"}), 400)

# get all users route
@app.route('/user/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({"users": [user.json() for user in users]}), 200)
    except Exception as e:
        return make_response(jsonify({"message": "Error getting users"}), 400)

# get user by id route
@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "Error getting user"}), 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
