"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@127.0.0.1/cupcakes"

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
def homepage():
    """Renders the landing page"""

    return render_template("index.html")

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


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add a cupcake and return data about the new cupcake"""
    req = request.json
    cupcake = Cupcake(
        flavor=req["flavor"],
        size=req["size"],
        rating=req["rating"],
        image=req["image"] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)


#PATCH
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake and return data about the new cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    req = request.json

    cupcake.flavor=req["flavor"]
    cupcake.size=req["size"]
    cupcake.rating=req["rating"]
    cupcake.image=req["image"]
 
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()))

#DELETE
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Return JSON for a single cupcake by id"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
