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

    - If **team** is provided, returns only players from that team.
    - If no filter is provided, returns all players.

    **Query Parameters:**
    - `team` (optional) → Filters players by team name.

    **Example Usage:**
    - `/players` → Returns all players.
    - `/players?team=Barcelona` → Returns players from "Barcelona".

    **Response:**
    - `200 OK` → Returns a list of players.
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
    Add a new football player.

    **Request Body:**
    - `name` (string) → Player's full name.
    - `team` (string) → The team the player belongs to.
    - `position` (string) → Player's position on the field.

    **Example Request Body:**
    ```json
    {
      "name": "Lionel Messi",
      "team": "Barcelona",
      "position": "Forward"
    }
    ```

    **Response:**
    - `201 Created` → Player added successfully.
    - `400 Bad Request` → Invalid input data.
    """
    data = request.json
    player = Player(name=data["name"], team=data["team"], position=data["position"])
    db.session.add(player)
    db.session.commit()
    return jsonify({"message": "Player added successfully"}), 201
