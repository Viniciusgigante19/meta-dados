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
    def __init__(self, atlas_client, cataloger):
        """
        atlas_client: instância do AtlasClient
        cataloger: instância do PostgresCataloger
        """
        self.atlas_client = atlas_client
        self.cataloger = cataloger

    def build_report(self, report_json_path=DISCOVERY_REPORT_JSON, report_csv_path=DISCOVERY_REPORT_CSV):
        """
        Monta o relatório com databases, tabelas, colunas e relacionamentos.
        Salva em JSON e CSV.
        """
        report_data = []

        # Itera pelas tabelas catalogadas
        for table_name, table_guid in self.cataloger.table_guids.items():
            columns_info = []
            for col_key, col_guid in self.cataloger.column_guids.items():
                if col_key.startswith(f"{table_name}."):
                    columns_info.append(col_key.split(".", 1)[1])

            # Linhagem opcional: buscar inputs/outputs via Atlas
            try:
                lineage = self.atlas_client.get_lineage(table_guid)
                relationships = [
                    f"{edge['fromEntity']}{LINEAGE_RELATIONSHIP_SEPARATOR}{edge['toEntity']}"
                    for edge in lineage.get("edges", [])
                ]
            except Exception:
                relationships = []

            report_data.append({
                "database_name": self.cataloger.db_guid,
                "table_name": table_name,
                "columns": columns_info,
                "num_columns": len(columns_info),
                "relationships": relationships
            })

        # Estatísticas
        total_databases = 1 if self.cataloger.db_guid else 0
        total_tables = len(report_data)
        total_columns = sum(r["num_columns"] for r in report_data)
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
