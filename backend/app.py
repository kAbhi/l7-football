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

    # Define 5 distinct teams with associated locations
    teams = [
        Team(name="Barcelona", country="Spain"),
        Team(name="Real Madrid", country="Spain"),
        Team(name="Manchester United", country="England"),
        Team(name="Bayern Munich", country="Germany"),
        Team(name="Juventus", country="Italy"),
    ]

    # Insert teams into the database
    db.session.bulk_save_objects(teams)
    db.session.commit()

    # Fetch the inserted teams from the database
    team_objects = Team.query.all()
    team_map = {team.name: team for team in team_objects}

    # Define 50 distinct players (10 per team)
    players = []
    positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]

    for team in team_objects:
        for i in range(10):
            players.append(Player(
                name=f"Player {i+1} - {team.name}",
                team=team.name,
                position=positions[i % len(positions)]
            ))

    db.session.bulk_save_objects(players)
    db.session.commit()

    # Define 5 distinct locations (matching team cities)
    locations = {
        "Barcelona": "Camp Nou",
        "Real Madrid": "Santiago Bernabéu",
        "Manchester United": "Old Trafford",
        "Bayern Munich": "Allianz Arena",
        "Juventus": "Allianz Stadium"
    }

    # Define 10 matches with the 5 locations
    matches = [
        Match(team1_id="Barcelona", team2_id="Real Madrid", date="2025-04-10", location=locations["Barcelona"]),
        Match(team1_id="Manchester United", team2_id="Bayern Munich", date="2025-04-11", location=locations["Manchester United"]),
        Match(team1_id="Juventus", team2_id="Barcelona", date="2025-04-12", location=locations["Juventus"]),
        Match(team1_id="Real Madrid", team2_id="Bayern Munich", date="2025-04-13", location=locations["Real Madrid"]),
        Match(team1_id="Manchester United", team2_id="Juventus", date="2025-04-14", location=locations["Manchester United"]),
        Match(team1_id="Bayern Munich", team2_id="Barcelona", date="2025-04-15", location=locations["Bayern Munich"]),
        Match(team1_id="Juventus", team2_id="Real Madrid", date="2025-04-16", location=locations["Juventus"]),
        Match(team1_id="Barcelona", team2_id="Manchester United", date="2025-04-17", location=locations["Barcelona"]),
        Match(team1_id="Real Madrid", team2_id="Manchester United", date="2025-04-18", location=locations["Real Madrid"]),
        Match(team1_id="Bayern Munich", team2_id="Juventus", date="2025-04-19", location=locations["Bayern Munich"]),
    ]

    db.session.bulk_save_objects(matches)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
