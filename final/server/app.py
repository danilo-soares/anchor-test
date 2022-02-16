from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask import Flask, render_template
from server.controller.photoAlbumController import photoAlbum
from server.controller.userController import users

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'SDFS321656cs1d65165CD'
jwt = JWTManager(app)

app.register_blueprint(users)
app.register_blueprint(photoAlbum)

app.config["MONGO_URI"] = ("mongodb+srv://admin:admin@anchor.pkl8s.mongodb.net/users?retryWrites=true&w=majority")
mongo = PyMongo(app, connect=False)
db = mongo.db

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
