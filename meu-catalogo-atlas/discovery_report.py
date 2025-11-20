# meu-catalogo-atlas/discovery_report.py

import json
import pandas as pd
from config import (
    DISCOVERY_REPORT_JSON,
    DISCOVERY_REPORT_CSV,
    DISCOVERY_REPORT_TITLE,
    LINEAGE_RELATIONSHIP_SEPARATOR
)

class DiscoveryReport:
    def __init__(self, atlas_client):
        """
        atlas_client: instância do AtlasClient
        """
        self.atlas_client = atlas_client

    def build_report(self, report_json_path=DISCOVERY_REPORT_JSON, report_csv_path=DISCOVERY_REPORT_CSV):
        """
        Monta o relatório buscando entidades diretamente do Atlas
        """
        # Buscar entidades RDBMS por tipo
        search_result = {'entities': []}

        # Buscar e combinar todos os tipos RDBMS
        db_result = self.atlas_client.search_entities("rdbms_db")
        table_result = self.atlas_client.search_entities("rdbms_table")  
        column_result = self.atlas_client.search_entities("rdbms_column")

        # Combinar resultados
        search_result['entities'].extend(db_result.get('entities', []))
        search_result['entities'].extend(table_result.get('entities', []))
        search_result['entities'].extend(column_result.get('entities', []))

        print(f">>> DEBUG - Total entidades RDBMS: {len(search_result['entities'])}")
        
        report_data = []
        databases = []
        tables = []
        columns = []

        # Processar entidades encontradas
        for entity in search_result.get('entities', []):
            entity_type = entity.get('typeName', '')
            attributes = entity.get('attributes', {})
            
            if entity_type == 'rdbms_db':
                databases.append({
                    'guid': entity['guid'],
                    'name': attributes.get('name', ''),
                    'qualifiedName': attributes.get('qualifiedName', '')
                })
            elif entity_type == 'rdbms_table':
                tables.append({
                    'guid': entity['guid'],
                    'name': attributes.get('name', ''),
                    'db_guid': attributes.get('db', {}).get('guid', '') if attributes.get('db') else ''
                })
            elif entity_type == 'rdbms_column':
                columns.append({
                    'guid': entity['guid'],
                    'name': attributes.get('name', ''),
                    'data_type': attributes.get('data_type', ''),
                    'table_guid': attributes.get('table', {}).get('guid', '') if attributes.get('table') else ''
                })

        # Construir relatório por tabela
        for table in tables:
            # Encontrar colunas desta tabela
            table_columns = [col for col in columns if col['table_guid'] == table['guid']]
            column_names = [col['name'] for col in table_columns]
            
            # Encontrar database da tabela
            db_name = "Unknown"
            for db in databases:
                if db['guid'] == table['db_guid']:
                    db_name = db['name']
                    break

            # Tentar buscar linhagem
            relationships = []
            try:
                lineage = self.atlas_client.get_lineage(table['guid'])
                relationships = [
                    f"{edge['fromEntity']}{LINEAGE_RELATIONSHIP_SEPARATOR}{edge['toEntity']}"
                    for edge in lineage.get("edges", [])
                ]
            except Exception:
                relationships = []

            report_data.append({
                "database_name": db_name,
                "table_name": table['name'],
                "columns": column_names,
                "num_columns": len(column_names),
                "relationships": relationships
            })

        # Estatísticas
        total_databases = len(databases)
        total_tables = len(tables)
        total_columns = len(columns)
        table_most_columns = max(report_data, key=lambda x: x["num_columns"])["table_name"] if report_data else None
        tables_with_relationships = [r["table_name"] for r in report_data if r["relationships"]]

        # Mostrar resumo no console
        print(DISCOVERY_REPORT_TITLE)
        print(f"Total de databases: {total_databases}")
        print(f"Total de tabelas: {total_tables}")
        print(f"Total de colunas: {total_columns}")
        print(f"Tabela com mais colunas: {table_most_columns}")
        print(f"Tabelas com relacionamentos: {tables_with_relationships}")

        # Salvar JSON
        with open(report_json_path, "w") as f:
            json.dump(report_data, f, indent=4)

        # Salvar CSV
        df = pd.DataFrame([
            {
                "database_name": r["database_name"],
                "table_name": r["table_name"],
                "num_columns": r["num_columns"],
                "columns": ", ".join(r["columns"]),
                "relationships": ", ".join(r["relationships"])
            } for r in report_data
        ])
        df.to_csv(report_csv_path, index=False)

        return report_data

# -------------------------
# Bloco MAIN para testar
# -------------------------
if __name__ == "__main__":
    from atlas_client import AtlasClient
    
    print("🔄 Iniciando relatório de descoberta...")
    
    # Criar instância do AtlasClient
    atlas_client = AtlasClient()
    
    # Criar relatório
    report = DiscoveryReport(atlas_client)
    report_data = report.build_report()
    
    print("✅ Relatório gerado com sucesso!")
    print(f"📊 JSON: {DISCOVERY_REPORT_JSON}")
    print(f"📊 CSV: {DISCOVERY_REPORT_CSV}")
    print(f"📈 {len(report_data)} tabelas processadas")