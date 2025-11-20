# tests/test_extractor.py

import unittest
from unittest.mock import patch, MagicMock
from postgres_extractor import PostgreSQLExtractor
import pandas as pd

class TestPostgreSQLExtractor(unittest.TestCase):
    def setUp(self):
        self.config = {
            "host": "localhost",
            "port": 5432,
            "database": "northwind",
            "user": "postgres",
            "password": "postgres"
        }
        self.extractor = PostgreSQLExtractor(**self.config)

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
    def test_list_tables(self, mock_read_sql):
        # Mock do retorno da query
        mock_read_sql.return_value = pd.DataFrame({"table_name": self.fake_tables})

        tables = self.extractor.list_tables()
        self.assertEqual(tables, self.fake_tables)
        mock_read_sql.assert_called_once()

    @patch("pandas.read_sql")
    def test_get_columns(self, mock_read_sql):
        for table, columns in self.fake_columns.items():
            mock_read_sql.return_value = pd.DataFrame(columns)
            result = self.extractor.get_columns(table)
            self.assertEqual(result, columns)
            mock_read_sql.assert_called()

    @patch("psycopg2.connect")
    def test_connection_failure(self, mock_connect):
        # Simular falha de conexão
        mock_connect.side_effect = Exception("Conexão falhou")
        with self.assertRaises(Exception):
            PostgreSQLExtractor(**self.config)

if __name__ == "__main__":
    unittest.main()
