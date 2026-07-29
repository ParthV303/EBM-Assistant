import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

def import_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "dataset", "EBM.csv")
    
    print("Loading CSV dataset using Pandas...")
    
    df = pd.read_csv(csv_path, sep=";")
    print(f"Dataset loaded. Shape: {df.shape}")
    
    df = df.where(pd.notnull(df), None)
    
    print("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(
        database="EBM",
        user="postgres",
        password="YOUR NAME",  
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    print("Creating 'papers' table...")
    cur.execute("""
    DROP TABLE IF EXISTS papers CASCADE;
    CREATE TABLE IF NOT EXISTS papers (
        id SERIAL PRIMARY KEY,
        paper_id INTEGER,
        title TEXT,
        source TEXT,
        published_date TEXT,
        link TEXT,
        summary TEXT,
        topics TEXT,
        row_idx INTEGER UNIQUE
    );
    """)
    conn.commit()
    
    print("Preparing data tuples for batch insert...")
    data_tuples = []
    for idx, row in df.iterrows():
        data_tuples.append((
            row['ID'],
            row['Title'],
            row['Source'],
            row['Published Date'],
            row['Link'],
            row['Summary'],
            row['Topics'],
            idx
        ))
        
    print("Inserting data into 'papers' table in batch...")
    insert_query = """
    INSERT INTO papers (paper_id, title, source, published_date, link, summary, topics, row_idx)
    VALUES %s
    ON CONFLICT (row_idx) DO UPDATE SET
        paper_id = EXCLUDED.paper_id,
        title = EXCLUDED.title,
        source = EXCLUDED.source,
        published_date = EXCLUDED.published_date,
        link = EXCLUDED.link,
        summary = EXCLUDED.summary,
        topics = EXCLUDED.topics;
    """
    
    execute_values(cur, insert_query, data_tuples)
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM papers;")
    count = cur.fetchone()[0]
    print(f"Data import completed! Total records in 'papers' table: {count}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_data()