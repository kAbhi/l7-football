from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from models import db
from routes.matches import matches_bp
from routes.teams import teams_bp
from routes.players import players_bp
from routes.areas import areas_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# Initialize Swagger
swagger = Swagger(app)

app.register_blueprint(matches_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(players_bp)
app.register_blueprint(areas_bp)

# Initialize DB with sample data
def seed_data():
    from models import Team, Match, Player
    teams = [Team(name="Barcelona", country="Spain"), Team(name="Real Madrid", country="Spain")]
    matches = [Match(team1="Barcelona", team2="Real Madrid", date="2025-04-15", location="Spain")]
    players = [Player(name="Lionel Messi", team="Barcelona", position="Forward")]
    db.session.bulk_save_objects(teams + matches + players)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
