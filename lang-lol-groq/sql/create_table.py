import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    return conn

# Function to create the 'conversation_history' table
def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS conversation_history (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Execute the table creation command
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'conversation_history' created successfully.")
        
        # Close the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

# Execute the table creation
if __name__ == "__main__":
    create_table()