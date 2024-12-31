let selectedTeam = null;

function selectTeam() {
    selectedTeam = document.getElementById('team-select').value;
    fetch('/select_team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team: selectedTeam }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('actions').style.display = 'block';
            document.getElementById('actions-heading').innerText = `${selectedTeam}, select your action`;
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function reportWin() {
    const button = document.getElementById('reportWinButton');
    button.disabled = true;  // Disable the button
    fetch('/report_win', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team: selectedTeam }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Win reported successfully!');
            updateBracketAndScoreboard(); // Update both the bracket and scoreboard
        } else {
            alert(`Error: ${data.error}`);
            button.disabled = false;  // Re-enable the button if there's an error
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.disabled = false;  // Re-enable the button if there's an error
    });
}

function reportChallenge() {
    const button = document.getElementById('reportChallengeButton');
    button.disabled = true;  // Disable the button
    fetch('/report_challenge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team: selectedTeam }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Challenge completed reported successfully!');
            updateBracketAndScoreboard(); // Update both the bracket and scoreboard
        } else {
            alert(`Error: ${data.error}`);
            button.disabled = false;  // Re-enable the button if there's an error
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.disabled = false;  // Re-enable the button if there's an error
    });
}

function updateBracketAndScoreboard() {
    fetch('/update_bracket_and_scoreboard')
        .then(response => response.json())
        .then(data => {
            updateBracket(data.rounds);
            document.getElementById('scoreboard').innerHTML = data.scoreboard_html;
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.getElementById('overlay');
    const actions = document.getElementById('actions');
    const selectHeading = document.getElementById('select-heading');
    const actionsHeading = document.getElementById('actions-heading');
    const teamSelect = document.getElementById('team-select');

    window.selectTeam = selectTeam;
    window.reportWin = reportWin;
    window.reportChallenge = reportChallenge;
});