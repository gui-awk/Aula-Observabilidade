import psycopg2
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'observability',
    'user': 'postgres',
    'password': 'postgres123'
}

def get_conn():
    for i in range(10):
        try:
            return psycopg2.connect(**DB_CONFIG)
        except:
            time.sleep(5)
    raise Exception("Cannot connect to PostgreSQL")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics_data (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            value INTEGER,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Table ready")

def insert_data():
    conn = get_conn()
    cur = conn.cursor()
    name = f"metric_{random.randint(1,100)}"
    val = random.randint(1,1000)
    cur.execute("INSERT INTO metrics_data (name, value) VALUES (%s, %s)", (name, val))
    conn.commit()
    cur.close()
    conn.close()
    logging.info(f"INSERT: {name}={val}")

def read_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM metrics_data ORDER BY RANDOM() LIMIT {random.randint(1,10)}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    logging.info(f"READ: {len(rows)} rows")

def update_data():
    conn = get_conn()
    cur = conn.cursor()
    val = random.randint(1,1000)
    cur.execute("UPDATE metrics_data SET value=%s WHERE id=(SELECT id FROM metrics_data ORDER BY RANDOM() LIMIT 1)", (val,))
    conn.commit()
    cur.close()
    conn.close()
    logging.info(f"UPDATE: {cur.rowcount} rows")

def delete_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM metrics_data WHERE id=(SELECT id FROM metrics_data ORDER BY RANDOM() LIMIT 1)")
    conn.commit()
    cur.close()
    conn.close()
    logging.info(f"DELETE: {cur.rowcount} rows")

if __name__ == "__main__":
    logging.info("Load Generator starting...")
    time.sleep(15)
    init_db()
    
    for _ in range(50):
        insert_data()
        time.sleep(0.1)
    
    ops = [insert_data, read_data, update_data, delete_data]
    weights = [5, 10, 3, 1]
    
    logging.info("Running load loop...")
    while True:
        try:
            op = random.choices(ops, weights=weights)[0]
            op()
            time.sleep(random.uniform(0.5, 3.0))
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(5)
