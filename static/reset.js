document.getElementById('resetButton').addEventListener('click', function() {
    fetch('/reset-database', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert('Database reset successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to reset the database.');
    });
});

document.getElementById('calculateMatchesButton').addEventListener('click', function() {
    fetch('/calculate-next-matches', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert('Next matches calculated successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to calculate matches.');
    });
});
