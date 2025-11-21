import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from postgres_extractor import PostgreSQLExtractor
import pandas as pd

class TestPostgreSQLExtractor(unittest.TestCase):
    def setUp(self):
        # USAR OS VALORES REAIS DO CONFIG
        self.config = {
            "host": "postgres_erp",  # ← CORRETO: nome do container
            "port": 5432,
            "database": "northwind", 
            "user": "postgres",
            "password": "postgres"
        }

        # Tabelas e colunas simuladas
        self.fake_tables = ["customers", "orders"]
        self.fake_columns = {
            "customers": [
                {"column_name": "customer_id", "data_type": "varchar", "is_nullable": "NO"},
                {"column_name": "customer_name", "data_type": "varchar", "is_nullable": "YES"}
            ],
            "orders": [
                {"column_name": "order_id", "data_type": "int", "is_nullable": "NO"},
                {"column_name": "order_date", "data_type": "date", "is_nullable": "YES"}
            ]
        }

    @patch("pandas.read_sql")
    @patch("psycopg2.connect")  # ← MOCKAR A CONEXÃO
    def test_list_tables(self, mock_connect, mock_read_sql):
        # Mock da conexão
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Mock do retorno da query
        mock_read_sql.return_value = pd.DataFrame({"table_name": self.fake_tables})

        extractor = PostgreSQLExtractor(**self.config)
        tables = extractor.list_tables()
        
        self.assertEqual(tables, self.fake_tables)
        mock_read_sql.assert_called_once()
        extractor.close()

    @patch("pandas.read_sql")
    @patch("psycopg2.connect")  # ← MOCKAR A CONEXÃO
    def test_get_columns(self, mock_connect, mock_read_sql):
        # Mock da conexão
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        extractor = PostgreSQLExtractor(**self.config)
        
        for table, columns in self.fake_columns.items():
            mock_read_sql.return_value = pd.DataFrame(columns)
            result = extractor.get_columns(table)
            self.assertEqual(result, columns)
            
        extractor.close()

    @patch("psycopg2.connect")
    def test_connection_failure(self, mock_connect):
        # Simular falha de conexão
        mock_connect.side_effect = Exception("Conexão falhou")
        with self.assertRaises(Exception):
            PostgreSQLExtractor(**self.config)

if __name__ == "__main__":
    unittest.main()