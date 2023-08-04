from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from typing import TYPE_CHECKING

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# Fix SQLAlchemy linting
if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    BaseModel = db.make_declarative_base(Model)
else:
    BaseModel = db.Model


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/all', methods=['GET'])
def all_cafes():
    pass


@app.route('/random', methods=['GET'])
def random_cafe():
    # Fetch a random entry by primary key / row ID
    rows = db.session.query(Cafe).count()
    rand_cafe_id = random.randint(1, rows)
    cafe = db.session.execute(db.select(Cafe).filter_by(id=rand_cafe_id)).scalar()
    # Can this be serialized to json in a simpler way? .__dict__ does not work on the object
    return jsonify(name=cafe.name,
                   map_url=cafe.map_url,
                   location=cafe.location,
                   seats=cafe.seats,
                   img_url=cafe.img_url,
                   id=cafe.id,
                   has_wifi=cafe.has_wifi,
                   has_toilet=cafe.has_toilet,
                   has_sockets=cafe.has_sockets,
                   coffee_price=cafe.coffee_price,
                   can_take_calls=cafe.can_take_calls
                   )


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
