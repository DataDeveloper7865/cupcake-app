"""Flask app for Cupcakes"""

from flask import Flask, redirect, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def display_homepage():
    """Render homepage"""

    return render_template("base.html")


@app.route("/api/cupcakes")
def get_all_cupcakes():
    """Return JSON for all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return JSON for a single cupcake by id"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<flavor>/<size>/<rating>/<image>", methods=["POST"])
def create_cupcake(flavor, size, rating, image):
    """Add a cupcake and return data about the new cupcake"""
    cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)
