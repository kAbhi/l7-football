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
    Fetch all matches with optional filtering by team and month.
    ---
    tags:
      - Matches
    parameters:
      - name: team
        in: query
        type: string
        required: false
        description: Filter matches where the specified team is playing. Example "Barcelona".
      - name: month
        in: query
        type: string
        format: YYYY-MM
        required: false
        description: Filter matches played in a specific month. Format "YYYY-MM". Example "2025-04".
    produces:
      - application/json
    responses:
      200:
        description: List of matches
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: Match ID
              team1:
                type: string
                description: Name of Team 1
              team2:
                type: string
                description: Name of Team 2
              date:
                type: string
                format: date
                description: Match date in YYYY-MM-DD format
              location:
                type: string
                description: Match venue
      400:
        description: Invalid month format
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid month format. Use YYYY-MM
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
    """
    Add a new match.
    ---
    tags:
      - Matches
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            team1:
              type: string
              example: Barcelona
              description: Name of the first team.
            team2:
              type: string
              example: Real Madrid
              description: Name of the second team.
            date:
              type: string
              format: date
              example: 2025-04-15
              description: Match date in YYYY-MM-DD format.
            location:
              type: string
              example: Camp Nou
              description: Location where the match is played.
          required:
            - team1
            - team2
            - date
            - location
    produces:
      - application/json
    responses:
      201:
        description: Match added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Match added successfully
      400:
        description: Validation error (duplicate match for team/date or location/date)
        schema:
          type: object
          properties:
            error:
              type: string
              example: A team already has a match on this date.
    """
    data = request.json

    # Check if the same team already has a match on the same date
    existing_team_match = Match.query.filter(
        ((Match.team1_id == data["team1"]) | (Match.team2_id == data["team1"]) |
         (Match.team1_id == data["team2"]) | (Match.team2_id == data["team2"])) &
        (Match.date == data["date"])
    ).first()

    if existing_team_match:
        return jsonify({"error": "A team already has a match on this date."}), 400

    # Check if a match is already scheduled at the same location on the same date
    existing_location_match = Match.query.filter_by(date=data["date"], location=data["location"]).first()
    if existing_location_match:
        return jsonify({"error": "A match is already scheduled at this location on this date."}), 400

    # Create and save new match
    match = Match(team1_id=data["team1"], team2_id=data["team2"], date=data["date"], location=data["location"])
    db.session.add(match)
    db.session.commit()

    return jsonify({"message": "Match added successfully"}), 201
