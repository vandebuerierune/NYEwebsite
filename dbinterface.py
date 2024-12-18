import tkinter as tk
from tkinter import messagebox
import pandas as pd
import mysql.connector

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Database Viewer")

        # Create a frame for the buttons
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        # Button to load data from the database
        self.load_button = tk.Button(self.frame, text="Load Data", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=10)

        # Button to display the table
        self.display_button = tk.Button(self.frame, text="Display Table", command=self.display_table)
        self.display_button.pack(side=tk.LEFT, padx=10)

        # Text widget to display the table
        self.text = tk.Text(root, wrap=tk.NONE)
        self.text.pack(expand=True, fill=tk.BOTH)

    def load_data(self):
        try:
            # Connect to the database
            self.conn = mysql.connector.connect(
                host="91.180.11.226",
                user="dbuser",
                password="PoppyJungle",
                database="NYE"
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            self.table_names = [table[0] for table in tables]
            self.text.insert(tk.END, f"Tables in the database: {', '.join(self.table_names)}\n")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def display_table(self):
        if hasattr(self, 'table_names'):
            table_name = self.table_names[0]  # Display the first table for simplicity
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, df.to_string(index=False))
        else:
            self.text.insert(tk.END, "No data loaded.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()