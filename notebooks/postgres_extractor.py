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


if __name__ == "__main__":
    print("🧪 Testando PostgreSQLExtractor...")
    
    from config import (
        POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE,
        POSTGRES_USER, POSTGRES_PASSWORD
    )
    
    try:
        extractor = PostgreSQLExtractor(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT, 
            database=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        print("✅ Conectado ao PostgreSQL!")
        
        tables = extractor.list_tables()
        print(f"✅ {len(tables)} tabelas encontradas:")
        for table in tables:
            print(f"   - {table}")
            
        # Testar colunas de uma tabela
        if tables:
            columns = extractor.get_columns(tables[0])
            print(f"✅ Colunas da tabela '{tables[0]}': {len(columns)} colunas")
            for col in columns[:3]:  # Mostrar primeiras 3
                print(f"   - {col['column_name']} ({col['data_type']})")
            
        extractor.close()
        print("✅ Conexão fechada!")
        print("🎉 PostgreSQLExtractor TESTADO E APROVADO!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")