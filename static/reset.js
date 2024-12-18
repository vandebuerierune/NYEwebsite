const express = require('express');
const app = express();
const port = 3000;

// Assuming you have a database connection set up
const db = require('./db'); // Replace with your actual database module

app.post('/reset-database', async (req, res) => {
    try {
        // Update the scores and wins to 0
        await db.query('UPDATE NYE.team SET score = 0, wins = 0');
        
        // If you have a matches table, you might want to clear it as well
        await db.query('DELETE FROM NYE.match');
        
        res.json({ message: 'Database reset successfully' });
    } catch (error) {
        console.error('Error resetting database:', error);
        res.status(500).json({ message: 'Failed to reset the database' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});