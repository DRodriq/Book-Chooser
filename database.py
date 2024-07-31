import sqlite3
import pandas as pd
import config

def create_db():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(config.DB_PATH)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table with the specified columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT NOT NULL,
        read_status TEXT,
        number_of_pages INTEGER,
        pages_read INTEGER,
        category TEXT,
        format TEXT
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and table created successfully.")

def update_db(frame):
    # Connect to the SQLite database
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    frame = format_df(frame)
    # Insert data into the database
    for index, row in frame.iterrows():
        cursor.execute('''
        INSERT INTO books (title, authors, read_status, number_of_pages, pages_read, category, format)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['title'], row['authors'], row['read_status'], row['number_of_pages'], row['pages_read'], row['category'], row['format']))

    # Commit the changes
    conn.commit()
    conn.close()

def fetch_all_books():
    # Connect to the SQLite database
    conn = sqlite3.connect(config.DB_PATH)
    query = "SELECT * FROM books"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def format_df(df):
    # Ensure the DataFrame has the required columns
    required_columns = ['Title', 'Authors', 'Format', 'Read Status', 'Tags', 'Owned?']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Fill NaN or empty values in 'Authors' with a default value
    df['Authors'] = df['Authors'].fillna(" ")

    # Create a new DataFrame with the required format
    formatted_df = pd.DataFrame({
        'title': df['Title'],
        'authors': df['Authors'],
        'read_status': df['Read Status'],
        'number_of_pages': 400,  # Default value
        'pages_read': 0,         # Default value
        'category': df['Tags'],
        'format': df['Format']
    })
    return formatted_df

def delete_entries_by_column_value(column, value):
    # Connect to the SQLite database
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Execute the DELETE statement
    cursor.execute(f"DELETE FROM books WHERE {column} = ?", (value,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Entries with {column} = {value} have been deleted successfully.")