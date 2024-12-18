from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__, template_folder='front')

teams = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F", "Team G", "Team H"]
rounds = []
challenge_text = "Initial Challenge Text"
selected_team = None

def generate_bracket(teams):
    global rounds
    rounds = []
    num_teams = len(teams)
    num_rounds = math.ceil(math.log2(num_teams))
    
    for i in range(num_rounds):
        round_matches = []
        for j in range(0, len(teams), 2):
            if j + 1 < len(teams):
                round_matches.append((teams[j], teams[j + 1]))
            else:
                round_matches.append((teams[j], "Bye"))
        rounds.append(round_matches)
        teams = ["Winner of Match {}".format(k + 1) for k in range(len(round_matches))]
    
    return rounds

@app.route('/')
def bracket():
    generate_bracket(teams)
    indexed_rounds = [(round_index, [(match_index, match) for match_index, match in enumerate(round)]) for round_index, round in enumerate(rounds)]
    return render_template('bracket.html', rounds=indexed_rounds, challenge_text=challenge_text)

@app.route('/control')
def control():
    return render_template('control.html', teams=teams)

@app.route('/select_team', methods=['POST'])
def select_team():
    global selected_team
    data = request.json
    selected_team = data['team']
    return jsonify(success=True)

@app.route('/report_win', methods=['POST'])
def report_win():
    global rounds
    data = request.json
    team = data['team']
    
    print('Received data:', data)  # Debugging line
    
    # Find the match and round where the team is currently playing
    for round_index, round in enumerate(rounds):
        for match_index, match in enumerate(round):
            if team in match:
                winner = team
                rounds[round_index][match_index] = (winner, match[1]) if match[0] == team else (match[0], winner)
                
                print(f'Updated round {round_index}, match {match_index} with winner {winner}')  # Debugging line
                
                # Propagate the winner to the next round
                if round_index < len(rounds) - 1:
                    next_match_index = match_index // 2
                    if match_index % 2 == 0:
                        rounds[round_index + 1][next_match_index] = (winner, rounds[round_index + 1][next_match_index][1])
                    else:
                        rounds[round_index + 1][next_match_index] = (rounds[round_index + 1][next_match_index][0], winner)
                    
                    print(f'Propagated winner to round {round_index + 1}, match {next_match_index}')  # Debugging line
                break
        else:
            continue
        break
    
    print('Updated rounds:', rounds)  # Debugging line
    
    return jsonify(success=True, rounds=rounds)

@app.route('/report_challenge', methods=['POST'])
def report_challenge():
    # Logic to handle reporting a completed challenge
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)