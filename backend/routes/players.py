from flask import Blueprint, jsonify, request
from models import db, Player
from flasgger import swag_from

players_bp = Blueprint('players', __name__)

@players_bp.route('/players', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of players',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'team': {'type': 'string'},
                        'position': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_players():
    """Fetch all players
    ---
    tags:
      - Players
    produces:
      - application/json
    responses:
      200:
        description: List of players
    """
    players = Player.query.all()
    return jsonify([{"id": p.id, "name": p.name, "team": p.team, "position": p.position} for p in players])

@players_bp.route('/players', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'team': {'type': 'string'},
                    'position': {'type': 'string'}
                },
                'required': ['name', 'team', 'position']
            }
        }
    ],
    'responses': {
        201: {'description': 'Player added successfully'},
        400: {'description': 'Invalid input data'}
    }
})
def add_player():
    """Add a new player
    ---
    tags:
      - Players
    requestBody:
      description: Player details
      required: true
    responses:
      201:
        description: Player added successfully
    """
    data = request.json
    player = Player(name=data["name"], team=data["team"], position=data["position"])
    db.session.add(player)
    db.session.commit()
    return jsonify({"message": "Player added successfully"}), 201
