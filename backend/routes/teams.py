from flask import Blueprint, jsonify, request
from models import db, Team
from flasgger import swag_from

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of teams',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'country': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_teams():
    """Fetch all teams
    ---
    tags:
      - Teams
    produces:
      - application/json
    responses:
      200:
        description: List of teams
    """
    teams = Team.query.all()
    return jsonify([{"id": t.id, "name": t.name, "country": t.country} for t in teams])

@teams_bp.route('/teams', methods=['POST'])
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
                    'country': {'type': 'string'}
                },
                'required': ['name', 'country']
            }
        }
    ],
    'responses': {
        201: {'description': 'Team added successfully'},
        400: {'description': 'Invalid input data'}
    }
})
def add_team():
    """Add a new team
    ---
    tags:
      - Teams
    requestBody:
      description: Team details
      required: true
    responses:
      201:
        description: Team added successfully
    """
    data = request.json
    team = Team(name=data["name"], country=data["country"])
    db.session.add(team)
    db.session.commit()
    return jsonify({"message": "Team added successfully"}), 201
