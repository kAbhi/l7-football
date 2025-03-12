from flask import Blueprint, jsonify
from models import db, Match
from flasgger import swag_from

areas_bp = Blueprint('areas', __name__)

@areas_bp.route('/areas', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of unique match locations',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'city': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_areas():
    """Fetch all unique match locations
    ---
    tags:
      - Areas
    produces:
      - application/json
    responses:
      200:
        description: List of locations
    """
    locations = db.session.query(Match.location).distinct().all()
    unique_locations = [{"id": idx + 1, "city": loc[0]} for idx, loc in enumerate(locations)]
    return jsonify(unique_locations)
