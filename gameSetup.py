from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify, current_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = "dbuser"
DB_PASSWORD = "PoppyJungle"
DB_NAME = "NYE"
DB_HOST = "91.180.11.226"


DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__, template_folder='front')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your models
class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.BigInteger, primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    team1_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)
    team2_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)
    winner_id = db.Column(db.BigInteger, db.ForeignKey('team.id'), nullable=True)

class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)

def add_team():
    name = input("Enter team name: ")
    team = Team(name=name)
    session.add(team)
    session.commit()
    print(f"Team '{name}' added.")

def add_match():
    round_number = int(input("Enter round number: "))
    team1_id = int(input("Enter team 1 ID: "))
    team2_id = int(input("Enter team 2 ID: "))
    match = Match(round=round_number, team1_id=team1_id, team2_id=team2_id)
    session.add(match)
    session.commit()
    print(f"Match between team {team1_id} and team {team2_id} added for round {round_number}.")

def add_challenge():
    description = input("Enter challenge description: ")
    challenge = Challenge(description=description)
    session.add(challenge)
    session.commit()
    print(f"Challenge '{description}' added.")

def main():
    while True:
        print("\nOptions:")
        print("1. Add Team")
        print("2. Add Match")
        print("3. Add Challenge")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_team()
        elif choice == '2':
            add_match()
        elif choice == '3':
            add_challenge()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()