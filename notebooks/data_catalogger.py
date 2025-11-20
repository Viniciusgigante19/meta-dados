# meu-catalogo-atlas/data_catalogger.py

from config import (
    ATLAS_TYPE_DATABASE,
    ATLAS_TYPE_TABLE,
    ATLAS_TYPE_COLUMN,
    DEFAULT_DB_OWNER,
    DEFAULT_DB_DESCRIPTION,
    TABLE_QUALIFIED_NAME_TEMPLATE,
    COLUMN_QUALIFIED_NAME_TEMPLATE
)

from postgres_extractor import PostgreSQLExtractor  # import corrigido
from atlas_client import AtlasClient  # assumindo que AtlasClient está em atlas_client.py

class PostgresCataloger:
    def __init__(self, atlas_client, extractor):
        """
        Construtor da classe de catalogação.

        atlas_client: instância de AtlasClient
        extractor: instância de PostgreSQLExtractor
        """
        self.atlas_client = atlas_client
        self.extractor = extractor

        # Dicionários para armazenar GUIDs e metadados
        self.db_guid = None
        self.table_guids = {}
        self.column_guids = {}

    def catalog_database(self, db_name, owner=None, description=None):
        """
        Cria o database no Atlas e salva o GUID.
        Retorna o GUID do database criado.
        """
        db_entity = {
            "typeName": ATLAS_TYPE_DATABASE,
            "attributes": {
                "name": db_name,
                "qualifiedName": db_name,
                "owner": owner or DEFAULT_DB_OWNER,
                "description": description or DEFAULT_DB_DESCRIPTION
            }
        }
        result = self.atlas_client.create_entity({"entities": [db_entity]})
        self.db_guid = result['guidAssignments'][db_entity['attributes']['qualifiedName']]
        return self.db_guid

    def catalog_all_tables(self):
        """
        Lista tabelas do PostgreSQL e cria entidades no Atlas para tabelas e colunas.
        Retorna um resumo do processo.
        """
        tables = self.extractor.list_tables()
        cataloged_tables = []

        for table_name in tables:
            # Criar entidade da tabela
            table_entity = {
                "typeName": ATLAS_TYPE_TABLE,
                "attributes": {
                    "name": table_name,
                    "qualifiedName": TABLE_QUALIFIED_NAME_TEMPLATE.format(
                        table_name=table_name,
                        db_guid=self.db_guid
                    ),
                    "db": {"guid": self.db_guid}
                }
            }
            try:
                result = self.atlas_client.create_entity({"entities": [table_entity]})
                table_guid = result['guidAssignments'][table_entity['attributes']['qualifiedName']]
                self.table_guids[table_name] = table_guid

                # Criar colunas da tabela
                columns = self.extractor.get_columns(table_name)
                for col in columns:
                    col_entity = {
                        "typeName": ATLAS_TYPE_COLUMN,
                        "attributes": {
                            "name": col['column_name'],
                            "qualifiedName": COLUMN_QUALIFIED_NAME_TEMPLATE.format(
                                table_name=table_name,
                                column_name=col['column_name'],
                                db_guid=self.db_guid
                            ),
                            "data_type": col['data_type'],
                            "is_nullable": col['is_nullable'],
                            "table": {"guid": table_guid}
                        }
                    }
                    col_result = self.atlas_client.create_entity({"entities": [col_entity]})
                    col_guid = col_result['guidAssignments'][col_entity['attributes']['qualifiedName']]
                    self.column_guids[f"{table_name}.{col['column_name']}"] = col_guid

                cataloged_tables.append(table_name)
            except Exception as e:
                print(f"Falha ao catalogar tabela {table_name}: {e}")

        return {
            "database_guid": self.db_guid,
            "tables_cataloged": cataloged_tables,
            "table_guids": self.table_guids,
            "column_guids": self.column_guids
        }

# -------------------------
# Bloco MAIN para testar
# -------------------------
if __name__ == "__main__":
    # Criar instâncias dos clientes
    atlas_client = AtlasClient()            # configure com credenciais reais
    extractor = PostgreSQLExtractor()       # configure com conexão real ou mocks

    catalogger = PostgresCataloger(atlas_client, extractor)

    # Testar catalog_database
    db_guid = catalogger.catalog_database("meu_db_teste")
    print("Database criado!")
    print("GUID do database:", db_guid)
    print("db_guid armazenado no objeto:", catalogger.db_guid)
    print("-" * 50)

    # Testar catalog_all_tables
    resumo = catalogger.catalog_all_tables()
    print("Catalogação de tabelas finalizada!")
    print("Resumo completo da catalogação:")
    print(resumo)
