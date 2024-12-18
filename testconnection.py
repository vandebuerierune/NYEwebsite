import mysql.connector

# Establish a connection to the database
conn = mysql.connector.connect(
    host="91.180.11.226",
    user="dbuser",  # Replace with your database username
    password="PoppyJungle",  # Replace with your database password
    database="NYE"  # Replace with your database name
)

# Create a cursor object
cursor = conn.cursor()

# Execute a simple query
cursor.execute("SELECT DATABASE();")

# Fetch the result
result = cursor.fetchone()

print("Connected to database:", result)

# Close the cursor and connection
cursor.close()
conn.close()