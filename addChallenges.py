import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="91.180.11.226",
    user="dbuser",
    password="PoppyJungle",
    database="NYE"
)

# Create a cursor object
cursor = conn.cursor()

# Create the challenges table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS challenges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    completed BOOLEAN NOT NULL
)
''')

# Function to add a challenge to the database
def add_challenge(description, completed=False):
    cursor.execute('''
    INSERT INTO Challenges (description, completed)
    VALUES (%s, %s)
    ''', (description, completed))
    print(description)
    conn.commit()

# Read challenges from a text file and add them to the database
with open('challenges.txt', 'r') as file:
    for line in file:
        challenge_description = line.strip()
        if challenge_description:  # Ensure the line is not empty
            add_challenge(challenge_description)

# Close the connection
conn.close()

print("Challenges added to the database successfully.")