from flask import Blueprint, jsonify, request
from models import db, Match
from flasgger import swag_from

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/matches', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of matches',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'team1': {'type': 'string'},
                        'team2': {'type': 'string'},
                        'date': {'type': 'string', 'format': 'date'},
                        'location': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_matches():
    """Fetch all matches
    ---
    tags:
      - Matches
    produces:
      - application/json
    responses:
      200:
        description: List of matches
    """
    matches = Match.query.all()
    return jsonify([{"id": m.id, "team1": m.team1_id, "team2": m.team2_id, "date": m.date, "location": m.location} for m in matches])

@matches_bp.route('/matches', methods=['POST'])
@swag_from({
    'summary': 'Add a new match',
    'description': 'Create a new football match entry with team names, match date, and location.',
    'tags': ['Matches'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'team1': {'type': 'string', 'example': 'Barcelona'},
                    'team2': {'type': 'string', 'example': 'Real Madrid'},
                    'date': {'type': 'string', 'format': 'date', 'example': '2025-04-15'},
                    'location': {'type': 'string', 'example': 'Madrid'}
                },
                'required': ['team1', 'team2', 'date', 'location']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Match added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Match added successfully'}
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
def add_match():
    """Add a new football match
    ---
    summary: Add a new match
    description: Create a new football match entry with team names, match date, and location.
    tags:
      - Matches
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            team1:
              type: string
              example: "Barcelona"
            team2:
              type: string
              example: "Real Madrid"
            date:
              type: string
              format: date
              example: "2025-04-15"
            location:
              type: string
              example: "Madrid"
          required:
            - team1
            - team2
            - date
            - location
    responses:
      201:
        description: Match added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Match added successfully"
      400:
        description: Invalid request data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid input data"
    """
    data = request.json
    match = Match(team1_id=data["team1"], team2_id=data["team2"], date=data["date"], location=data["location"])
    db.session.add(match)
    db.session.commit()
    return jsonify({"message": "Match added successfully"}), 201
