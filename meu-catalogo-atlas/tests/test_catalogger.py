# tests/test_postgres_cataloger.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from data_catalogger import PostgresCataloger

class TestPostgresCataloger(unittest.TestCase):
    def setUp(self):
        # Mock do AtlasClient
        self.mock_atlas = Mock()
        self.mock_atlas.create_entity.side_effect = self.mock_create_entity
        self.mock_atlas.get_lineage.return_value = {"nodes": [], "edges": []}

        # Mock do PostgreSQLExtractor
        self.mock_extractor = Mock()
        self.mock_extractor.list_tables.return_value = ["customers", "orders"]
        self.mock_extractor.get_columns.side_effect = self.mock_get_columns

        # Instância do cataloger
        self.cataloger = PostgresCataloger(self.mock_atlas, self.mock_extractor)

        # Database
        self.db_name = "northwind_postgres"

        # Contadores para gerar GUIDs simulados
        self.guid_counter = 1

    # Mock create_entity para retornar GUIDs únicos
    def mock_create_entity(self, entity_data):
        guid_assignments = {}
        for e in entity_data.get("entities", []):
            qname = e["attributes"]["qualifiedName"]
            guid = f"guid-{self.guid_counter}"
            self.guid_counter += 1
            guid_assignments[qname] = guid
        return {"guidAssignments": guid_assignments}

    # Mock get_columns para cada tabela
    def mock_get_columns(self, table_name):
        fake_columns = {
            "customers": [
                {"column_name": "customer_id", "data_type": "varchar", "is_nullable": "NO"},
                {"column_name": "customer_name", "data_type": "varchar", "is_nullable": "YES"}
            ],
            "orders": [
                {"column_name": "order_id", "data_type": "int", "is_nullable": "NO"},
                {"column_name": "order_date", "data_type": "date", "is_nullable": "YES"}
            ]
        }
        return fake_columns.get(table_name, [])

    def test_catalog_database(self):
        # Mock da criação da instância primeiro
        instance_guid = "guid-instance-1"
        self.cataloger.catalog_instance = Mock(return_value=instance_guid)
        
        db_guid = self.cataloger.catalog_database(self.db_name, instance_guid=instance_guid)
        self.assertIsNotNone(db_guid)
        self.assertTrue(db_guid.startswith("guid-"))

    def test_catalog_all_tables(self):
        # Mock da criação da instância primeiro
        instance_guid = "guid-instance-1"
        self.cataloger.catalog_instance = Mock(return_value=instance_guid)
        
        self.cataloger.catalog_database(self.db_name, instance_guid=instance_guid)
        result = self.cataloger.catalog_all_tables()

        # Verificações básicas
        self.assertIn("database_guid", result)
        self.assertEqual(set(result["tables_cataloged"]), {"customers", "orders"})
        self.assertEqual(set(result["table_guids"].keys()), {"customers", "orders"})
        self.assertEqual(set(result["column_guids"].keys()),
                         {"customers.customer_id", "customers.customer_name",
                          "orders.order_id", "orders.order_date"})

    def test_catalog_all_tables_with_exception(self):
        # Mock da criação da instância primeiro
        instance_guid = "guid-instance-1"
        self.cataloger.catalog_instance = Mock(return_value=instance_guid)

        # Simular exceção ao criar uma tabela
        def raise_exception(entity_data):
            if entity_data["entities"][0]["attributes"]["name"] == "orders":
                raise Exception("Erro simulado")
            return self.mock_create_entity(entity_data)

        self.mock_atlas.create_entity.side_effect = raise_exception
        self.cataloger.catalog_database(self.db_name, instance_guid=instance_guid)
        result = self.cataloger.catalog_all_tables()

        # customers deve ser catalogada, orders falhar
        self.assertIn("customers", result["tables_cataloged"])
        self.assertNotIn("orders", result["tables_cataloged"])

if __name__ == "__main__":
    unittest.main()