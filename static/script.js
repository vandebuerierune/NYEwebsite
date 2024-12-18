function selectWinner(roundIndex, matchIndex, teamIndex) {
    const match = document.querySelectorAll('.round')[roundIndex].querySelectorAll('.match')[matchIndex];
    const teams = match.querySelectorAll('.team');
    const winner = teams[teamIndex].textContent;
    
    teams.forEach((team, index) => {
        if (index === teamIndex) {
            team.classList.add('selected');
        } else {
            team.classList.remove('selected');
        }
    });

    fetch('/select_winner', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ round: roundIndex, match: matchIndex, winner: winner })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateBracket(data.rounds);
        }
    });
}

function updateBracket(rounds) {
    const bracket = document.querySelector('.bracket');
    bracket.innerHTML = ''; // Clear the existing bracket

    rounds.forEach((round, roundIndex) => {
        const roundDiv = document.createElement('div');
        roundDiv.classList.add('round');

        round.forEach((match, matchIndex) => {
            const matchDiv = document.createElement('div');
            matchDiv.classList.add('match');

            match.forEach((team, teamIndex) => {
                const teamDiv = document.createElement('div');
                teamDiv.classList.add('team');
                teamDiv.textContent = team;
                teamDiv.onclick = () => selectWinner(roundIndex, matchIndex, teamIndex);
                matchDiv.appendChild(teamDiv);
            });

            roundDiv.appendChild(matchDiv);
        });

        bracket.appendChild(roundDiv);
    });
}