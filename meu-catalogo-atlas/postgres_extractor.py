# postgres_extractor.py

import psycopg2
import pandas as pd
from config import POSTGRES_SCHEMA


class PostgreSQLExtractor:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
    
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=self.password
        )

    def list_tables(self):
        query = f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{POSTGRES_SCHEMA}'
        """
        df = pd.read_sql(query, self.conn)
        return df['table_name'].tolist()

    def get_columns(self, table_name):
        query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s
        """
        df = pd.read_sql(query, self.conn, params=(table_name,))
        return df.to_dict(orient='records')

    def close(self):
        if self.conn:
            self.conn.close()
