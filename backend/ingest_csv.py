import pandas as pd
from sqlalchemy import create_engine
import os

# Adjust the path to go up one level from the script's location to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(project_root, 'test.csv')
db_path = os.path.join(project_root, 'test.db') # Assuming SQLite for simplicity

def ingest_data():
    """Reads data from test.csv and ingests it into an SQLite database table."""
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    try:
        df = pd.read_csv(csv_path)
        
        # Using a file-based SQLite database as specified in the .env.example
        engine = create_engine(f'sqlite:///{db_path}')
        
        # Write the data to a table named 'employees'. If the table exists, it will be replaced.
        df.to_sql('employees', engine, if_exists='replace', index=False)
        
        print(f"Successfully ingested {len(df)} rows into the 'employees' table in {db_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ingest_data()
