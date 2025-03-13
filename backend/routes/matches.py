from flask import Blueprint, jsonify, request
from models import db, Match
from flasgger import swag_from
from datetime import datetime

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/matches', methods=['GET'])
@swag_from({
    'summary': 'Fetch matches with optional filters',
    'description': 'Retrieve a list of football matches. You can filter results by team or month.',
    'tags': ['Matches'],
    'parameters': [
        {
            'name': 'team',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter matches where the specified team is playing. Example: "Barcelona"'
        },
        {
            'name': 'month',
            'in': 'query',
            'type': 'string',
            'format': 'YYYY-MM',
            'required': False,
            'description': 'Filter matches played in a specific month. Format: "YYYY-MM". Example: "2025-04"'
        }
    ],
    'responses': {
        200: {
            'description': 'List of matches',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'team1': {'type': 'string', 'description': 'Name of Team 1'},
                        'team2': {'type': 'string', 'description': 'Name of Team 2'},
                        'date': {'type': 'string', 'format': 'date', 'description': 'Match date (YYYY-MM-DD)'},
                        'location': {'type': 'string', 'description': 'Match venue'}
                    }
                }
            }
        },
        400: {
            'description': 'Invalid request parameters',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_matches():
    """
    Fetch matches with optional filtering by team and month.

    - If **team** is provided, returns matches where that team is playing.
    - If **month** is provided, returns matches played in that month.
    - If both **team** and **month** are provided, applies both filters.
    - If no filters are provided, returns all matches.

    **Query Parameters:**
    - `team` (optional) → Filters matches by team name.
    - `month` (optional) → Filters matches by month in `YYYY-MM` format.

    **Example Usage:**
    - `/matches` → Returns all matches.
    - `/matches?team=Barcelona` → Returns matches where "Barcelona" is playing.
    - `/matches?month=2025-04` → Returns matches played in April 2025.
    - `/matches?team=Barcelona&month=2025-04` → Returns Barcelona matches in April 2025.

    **Response:**
    - `200 OK` → Returns a list of matches.
    - `400 Bad Request` → If the `month` format is invalid.
    """
    team = request.args.get("team", None)
    month = request.args.get("month", None)

    query = Match.query
    if team:
        query = query.filter((Match.team1_id == team) | (Match.team2_id == team))
    if month:
        try:
            start_date = datetime.strptime(month, "%Y-%m").replace(day=1)
            end_date = datetime.strptime(month, "%Y-%m").replace(day=28)
            query = query.filter(Match.date >= start_date.strftime("%Y-%m-%d"),
                                 Match.date <= end_date.strftime("%Y-%m-%d"))
        except ValueError:
            return jsonify({"error": "Invalid month format. Use YYYY-MM"}), 400

    matches = query.all()
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
