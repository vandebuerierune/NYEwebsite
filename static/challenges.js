function selectWinner(round, match, winner) {
    fetch('/select_winner', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ round: round, match: match, winner: winner }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

function updateChallenge() {
    const challengeText = document.getElementById('challenge-input').value;
    fetch('/update_challenge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ challenge_text: challengeText }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}