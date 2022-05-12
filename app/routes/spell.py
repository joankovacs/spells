from app import db
from app.models.spell import Spell
from flask import Blueprint, jsonify, make_response, request, abort

def validate_spell(spell_id):
    try:
        spell_id = int(spell_id)
    except:
        abort(make_response({"message":f"spell {spell_id} invalid"}, 400))

    spell = Spell.query.get(spell_id)
    if not spell:
        abort(make_response({"message":f"spell {spell_id} not found"}, 404))

    return spell


spells_bp = Blueprint("spells_bp", __name__, url_prefix="/spells")


@spells_bp.route("", methods=["GET", "POST"])
def triangulate_spell():
    if request.method == "GET":
        spells = Spell.query.all()
        spells_reaction = []
        for spell in spells:
            spells_reaction.append({
                "id":spell.id,
                "name":spell.name,
                "description":spell.description,
            })
        return jsonify(spells_reaction)

    elif request.method == "POST":
        request_body = request.get_json()

        new_spell = Spell(name=request_body["name"],
                    description=request_body["description"])

        db.session.add(new_spell)
        db.session.commit()

        return make_response(f'Spell {new_spell.name} triangulated successfully.')

@spells_bp.route("/<spell_id>", methods=["GET"])
def extract_spell(spell_id):
    target_spell = validate_spell(spell_id)

    return jsonify({
        "id":target_spell.id,
        "name":target_spell.name,
        "description":target_spell.description,
    })

@spells_bp.route("/<spell_id>", methods=["PUT"])
def update_spell(spell_id):
    spell = validate_spell(spell_id)

    request_body = request.get_json()

    spell.name = request_body["name"]
    spell.description = request_body["description"]

    db.session.commit()

    return make_response(f'Spell #{spell_id} successfully updated!')

@spells_bp.route("/<spell_id>", methods=["DELETE"])
def obliterate_spell(spell_id):
    spell = validate_spell(spell_id)

    db.session.delete(spell)
    db.session.commit()

    return make_response(f'Spell #{spell_id} is destroyed.')


'''
spells = [
    Spell(1, "Archaea", "Reveal hidden secrets from the past."),
    Spell(2, "Shatter", "Open that which should not even be."),
    Spell(3, "Lapis Lazuli", "So glamorous it hurts."),
    Spell(4, "Tomahawk", "Shock & assault."),
    Spell(5, "Elysium", "A lifetime of love in a single kiss."),
    Spell(6, "Breach Cement", "Closed that which you've opened - at a terrible price."),
#]
'''
