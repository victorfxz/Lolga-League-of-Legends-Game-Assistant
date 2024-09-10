from prefect import task, Flow
import pandas as pd
import psycopg2

# Configuration for connecting to the LOLGA app database.
def get_lolga_db_connection():
    conn = psycopg2.connect(
        dbname='your_dbname',
        user='your_user',
        password='your_password',
        host='localhost',  # Assuming the database is local.
        port='5432'        # Default PostgreSQL port.
    )
    return conn

# Task to extract data from the LOLGA app database.
@task
def extract_data():
    conn = get_lolga_db_connection()
    query = "SELECT question, response FROM conversation_history;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Task to transform data.
@task
def transform_data(df):
    # Data transformation logic.
    df['question'] = df['question'].str.strip()  # Remove leading/trailing whitespace.
    df['response'] = df['response'].str.strip()  # Remove leading/trailing whitespace.
    return df

# Task to load data into the destination database.
@task
def load_data(df):
    conn = psycopg2.connect(
        dbname='your_destination_dbname',
        user='your_destination_user',
        password='your_destination_password',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            "INSERT INTO your_destination_table (question, response) VALUES (%s, %s)",
            (row['question'], row['response'])
        )
    conn.commit()
    cursor.close()
    conn.close()

# Defining the workflow
with Flow("LOLGA Data Ingestion Flow") as flow:
    df = extract_data()
    transformed_df = transform_data(df)
    load_data(transformed_df)

# Run the workflow locally for testing
if __name__ == "__main__":
    flow.run()