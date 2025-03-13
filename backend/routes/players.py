from flask import Blueprint, jsonify, request
from models import db, Player
from flasgger import swag_from

players_bp = Blueprint('players', __name__)

@players_bp.route('/players', methods=['GET'])
@swag_from({
    'summary': 'Fetch players with optional team filter',
    'description': 'Retrieve a list of players. You can filter results by team.',
    'tags': ['Players'],
    'parameters': [
        {
            'name': 'team',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter players by team name. Example: "Barcelona"'
        }
    ],
    'responses': {
        200: {
            'description': 'List of players',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer', 'description': 'Player ID'},
                        'name': {'type': 'string', 'description': 'Player Name'},
                        'team': {'type': 'string', 'description': 'Team Name'},
                        'position': {'type': 'string', 'description': 'Player Position'}
                    }
                }
            }
        }
    }
})
def get_players():
    """
    Fetch all players with an optional team filter.
    ---
    tags:
      - Players
    parameters:
      - name: team
        in: query
        type: string
        required: false
        description: Filter players by team name (Example "Barcelona").
    produces:
      - application/json
    responses:
      200:
        description: List of players
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: Player ID
              name:
                type: string
                description: Player Name
              team:
                type: string
                description: Team Name
              position:
                type: string
                description: Player Position
    """
    team = request.args.get("team", None)

    query = Player.query
    if team:
        query = query.filter(Player.team == team)
    players = query.all()
    return jsonify([{"id": p.id, "name": p.name, "team": p.team, "position": p.position} for p in players])

@players_bp.route('/players', methods=['POST'])
@swag_from({
    'summary': 'Add a new player',
    'description': 'Create a new football player entry with name, team, and position.',
    'tags': ['Players'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Lionel Messi'},
                    'team': {'type': 'string', 'example': 'Barcelona'},
                    'position': {'type': 'string', 'example': 'Forward'}
                },
                'required': ['name', 'team', 'position']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Player added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Player added successfully'}
                }
            }
        },
        400: {
            'description': 'Invalid request data',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Invalid input data'}
                }
            }
        }
    }
})
def add_player():
    """
    Add a new player to the system.
    ---
    tags:
      - Players
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Lionel Messi
              description: Full name of the player.
            team:
              type: string
              example: Barcelona
              description: Team the player belongs to.
            position:
              type: string
              example: Forward
              description: Position the player plays in.
          required:
            - name
            - team
            - position
    produces:
      - application/json
    responses:
      201:
        description: Player added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Player added successfully
      400:
        description: Validation error (duplicate player name)
        schema:
          type: object
          properties:
            error:
              type: string
              example: Player with this name already exists.
    """
    data = request.json

    # Check if the player name already exists
    existing_player = Player.query.filter_by(name=data["name"]).first()
    if existing_player:
        return jsonify({"error": "Player with this name already exists."}), 400

    # Create new player
    player = Player(name=data["name"], team=data["team"], position=data["position"])
    db.session.add(player)
    db.session.commit()

    return jsonify({"message": "Player added successfully"}), 201
