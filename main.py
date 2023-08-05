from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from typing import TYPE_CHECKING

app = Flask(__name__)

##Connect to sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# Fix SQLAlchemy linting...
if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    BaseModel = db.make_declarative_base(Model)
else:
    BaseModel = db.Model


# Cafe table configuration
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'map_url': self.map_url,
            'img_url': self.img_url,
            'location': self.location,
            'seats': self.seats,
            'has_toilet': self.has_toilet,
            'has_wifi': self.has_wifi,
            'has_sockets': self.has_sockets,
            'can_take_calls': self.can_take_calls,
            'coffee_price': self.coffee_price
        }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/all', methods=['GET'])
def get_all_cafes():
    all_cafes = db.session.execute(db.select(Cafe)).scalars()
    cafe_list = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=cafe_list)


@app.route('/random', methods=['GET'])
def random_cafe():
    # Fetch a random entry by primary key / row ID
    rows = db.session.query(Cafe).count()
    rand_cafe_id = random.randint(1, rows)
    cafe = db.session.execute(db.select(Cafe).filter_by(id=rand_cafe_id)).scalar()
    return jsonify(cafe.to_dict())


@app.route('/search', methods=['GET'])
def search_cafes():
    loc = request.args.get('loc')
    found_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == loc.title())).scalars()
    found_cafe_list = [cafe.to_dict() for cafe in found_cafes]

    # Check if any results were found
    if found_cafe_list == []:
        return jsonify(error={"Not Found": "Sorry, a cafe was not found at that location"})
    else:
        return jsonify(cafes=found_cafe_list)


@app.route('/add', methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.args.get('name'),
        map_url=request.args.get('map_url'),
        img_url=request.args.get('img_url'),
        location=request.args.get('location'),
        seats=request.args.get('seats'),
        has_toilet=bool(request.args.get('has_toilet')),
        has_wifi=bool(request.args.get('has_wifi')),
        has_sockets=bool(request.args.get('has_sockets')),
        can_take_calls=bool(request.args.get('can_take_calls')),
        coffee_price=request.args.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={'success': 'Successfully added the new cafe.'})


@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    # TODO: Find a cleaner way to handle this.
    try:
        cafe = db.get_or_404(Cafe, cafe_id)
    except Exception as e:
        return jsonify(errror={"Not found": "That cafe ID was not found."}), 404
    else:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(success={"Success": "Successfully updated the price."}), 200


if __name__ == '__main__':
    app.run(debug=True)
