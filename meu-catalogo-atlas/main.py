# main.py

from atlas_client import AtlasClient
from postgres_extractor import PostgreSQLExtractor
from postgres_cataloger import PostgresCataloger
from discovery_report import DiscoveryReport

from config import (
    ATLAS_URL,
    ATLAS_USERNAME,
    ATLAS_PASSWORD,
    DISCOVERY_REPORT_JSON,
    DISCOVERY_REPORT_CSV,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    TARGET_DATABASE_NAME
)


def main():
    # 1️⃣ Instanciar AtlasClient
    atlas = AtlasClient(
        url=ATLAS_URL,
        username=ATLAS_USERNAME,
        password=ATLAS_PASSWORD
    )

    # 2️⃣ Conexão com PostgreSQL
    extractor = PostgreSQLExtractor(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    # 3️⃣ Catalogador
    cataloger = PostgresCataloger(atlas, extractor)

    # 4️⃣ Gerador de relatório
    reporter = DiscoveryReport(atlas, cataloger)

    # Catalogar database
    print("Catalogando database...")
    db_guid = cataloger.catalog_database(TARGET_DATABASE_NAME)
    print(f"Database catalogado com GUID: {db_guid}")

    # Catalogar tabelas e colunas
    print("Catalogando tabelas e colunas...")
    tables_summary = cataloger.catalog_all_tables()
    print(f"Tabelas catalogadas: {len(tables_summary['tables_cataloged'])}")

    # Gerar relatório
    print("Gerando relatório de descoberta...")
    reporter.build_report(
        report_json_path=DISCOVERY_REPORT_JSON,
        report_csv_path=DISCOVERY_REPORT_CSV
    )
    print("Relatório gerado com sucesso!")

    # Encerrar PostgreSQL
    extractor.close()
    print("Conexão com PostgreSQL encerrada.")


if __name__ == "__main__":
    main()
