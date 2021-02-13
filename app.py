from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from keys import MAPQUEST_API_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)  
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route("/")
def list_pets():
    """ shows a list of all the pets in the db """
    pets = Pet.query.all()
    return render_template('lists.html', pets=pets)

@app.route('/', methods=["POST"])
def create_pet():
    name = request.form["name"]
    species = request.form["species"]
    hunger = request.form['hunger']
    hunger = int(hunger) if hunger else None
    new_pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)
    db.session.commit()
    return redirect(f"/{new_pet.id}")

@app.route('/<int:pet_id>')
def show_pet(pet_id):
    """ show deatils about a single pet """
    pet = Pet.query.get_or_404(pet_id)
    return render_template('details.html', pet=pet)

@app.route('/species/<species_id>')
def show_pets_by_species(species_id):
    pets = Pet.get_by_species(species_id)
    return render_template('species.html', pets=pets, species=species_id)

