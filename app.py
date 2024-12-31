from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import hashlib

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='front')

# Database configuration
DB_USER = "dbuser"
DB_PASSWORD = "PoppyJungle"
DB_NAME = "NYE"
DB_HOST = "192.168.1.100"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Team(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.BigInteger, default=0)
    wins = db.Column(db.Integer, default=0)

class Match(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)
    team2_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)
    winner_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Challenge {self.id}>"

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def bracket():
    rounds = get_rounds_data()
    teams = Team.query.order_by(Team.score.desc()).all()
    scoreboard = {team.name: team.score for team in teams}
    return render_template('bracket.html', rounds=rounds, enumerate=enumerate, scoreboard=scoreboard)

@app.route('/reset')
def reset_page():
    return render_template('reset.html')

@app.route('/control')
def control():
    # Get all teams from the database
    teams = Team.query.all()
    # Render the control page with the list of team names
    return render_template('control.html', teams=[team.name for team in teams])

@app.route('/tournament_bracket')
def tournament_bracket():
    # Fetch the first incomplete challenge
    challenge = Challenge.query.filter_by(completed=False).first()

    # If no challenge is incomplete
    challenge_text = challenge.description if challenge else "No challenges available."
    challenge_id = challenge.id if challenge else None

    return render_template('bracket.html', challenge_text=challenge_text, challenge_id=challenge_id)

@app.route('/complete_challenge', methods=['POST'])
def complete_challenge():
    # Get the challenge ID from the request
    data = request.json
    challenge_id = data.get('challenge_id')
    challenge = Challenge.query.get(challenge_id)

    if challenge:
        # Mark the challenge as completed
        challenge.completed = True
        db.session.commit()

        # Get the next challenge to show
        next_challenge = Challenge.query.filter_by(completed=False).first()
        next_challenge_text = next_challenge.description if next_challenge else "No more challenges."

        return jsonify(success=True, message="Challenge completed", next_challenge=next_challenge_text)
    
    return jsonify(success=False, error="Challenge not found"), 404

@app.route('/reset-database', methods=['POST'])
def reset_database():
    db.session.query(Team).update({Team.score: 0, Team.wins: 0})
    db.session.query(Match).delete()
    db.session.commit()
    return jsonify(success=True)

@app.route('/calculate-next-matches', methods=['POST'])
def calculate_next_matches():
    num_rounds = db.session.query(db.func.max(Match.round)).scalar() or 0
    create_next_round_matches(num_rounds)
    return jsonify(success=True, message="Next matches calculated successfully.")

import hashlib

@app.route('/check_updates')
def check_updates():
    # Query all teams ordered by their id
    teams = Team.query.order_by(Team.id).all()
    
    # Concatenate team data (id, score, wins) into a string
    teams_data = ''.join([f'{team.id}{team.score}{team.wins}' for team in teams])
    
    # Generate a hash of the concatenated data
    teams_hash = hashlib.md5(teams_data.encode()).hexdigest()
    
    # Return the hash as a response
    return jsonify(hash=teams_hash)

@app.route('/report_challenge', methods=['POST'])
def report_challenge():
    data = request.json
    team_name = data['team']

    team = Team.query.filter_by(name=team_name).first()
    
    if not team:
        return jsonify(success=False, error="Team not found"), 400

    # Mark challenge as completed
    challenge = Challenge.query.filter_by(completed=False).first()
    
    if not challenge:
        return jsonify(success=False, error="No incomplete challenges found."), 400

    challenge.completed = True  # Mark the challenge as completed
    db.session.commit()

    # Optionally, increment score for completing the challenge
    team.score += 1
    db.session.commit()

    return jsonify(success=True, message="Challenge reported successfully!")

@app.route('/update_bracket_and_scoreboard')
def update_bracket_and_scoreboard():
    rounds = get_rounds_data()  # Get the updated rounds data
    teams = Team.query.order_by(Team.score.desc()).all()  # Sorted by score
    scoreboard_html = render_template('scoreboard.html', teams=teams)
    
    return jsonify(rounds=rounds, scoreboard_html=scoreboard_html)





@app.route('/update_challenge', methods=['POST'])
def update_challenge():
    data = request.json
    challenge_text = data['challenge_text']
    
    # Assuming you only want to update the first incomplete challenge
    challenge = Challenge.query.filter_by(completed=False).first()
    
    if not challenge:
        return jsonify(success=False, error="No incomplete challenges to update."), 400
    
    challenge.description = challenge_text
    db.session.commit()
    
    return jsonify(success=True, message="Challenge updated successfully.")


@app.route('/report_win', methods=['POST'])
def report_win():
    data = request.json
    team_name = data['team']
    team = Team.query.filter_by(name=team_name).first()

    if not team:
        return jsonify(success=False, error="Team not found"), 400

    # Increment wins in the database directly
    team.wins += 1
    db.session.commit()

    # Update the winner for the match
    inferred_round = Match.query.filter_by(winner_id=team.id).count() + 1
    match = Match.query.filter(
        ((Match.team1_id == team.id) | (Match.team2_id == team.id)) & (Match.round == inferred_round)
    ).first()

    if not match:
        return jsonify(success=False, error="Match not found for inferred round"), 400

    match.winner_id = team.id
    db.session.commit()

    return jsonify(success=True, message=f"Win recorded for round {inferred_round}"), 200

# Utility Functions
def create_next_round_matches(current_round):
    next_round = current_round + 1
    existing_matches = Match.query.filter_by(round=next_round).all()
    if existing_matches:
        return existing_matches

    teams = Team.query.order_by(Team.wins.desc()).all()
    matches = []
    for i in range(0, len(teams), 2):
        team1 = teams[i]
        team2 = teams[i + 1] if i + 1 < len(teams) else None
        match = Match(round=next_round, team1_id=team1.id, team2_id=team2.id if team2 else None)
        matches.append(match)

    db.session.add_all(matches)
    db.session.commit()
    return matches

def get_rounds_data():
    rounds = []
    num_rounds = db.session.query(db.func.max(Match.round)).scalar() or 0
    for round_index in range(num_rounds + 1):
        matches = Match.query.filter_by(round=round_index).all()
        round_matches = [
            (
                Team.query.get(match.team1_id).name if match.team1_id else "TBD",
                Team.query.get(match.team2_id).name if match.team2_id else "TBD",
                Team.query.get(match.winner_id).name if match.winner_id else "TBD",
            )
            for match in matches
        ]
        rounds.append(round_matches)
    return rounds

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
