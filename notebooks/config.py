# config.py

# URL do Apache Atlas
ATLAS_URL = "http://localhost:21000"

# Credenciais padrão
ATLAS_USERNAME = "admin"
ATLAS_PASSWORD = "admin"

# Tipos para postgres
ATLAS_TYPE_DATABASE = "postgres_db"
ATLAS_TYPE_TABLE = "postgres_table"
ATLAS_TYPE_COLUMN = "postgres_column"

# Valores default para banco
DEFAULT_DB_OWNER = "unknown"
DEFAULT_DB_DESCRIPTION = ""

# Templates para qualifiedName
TABLE_QUALIFIED_NAME_TEMPLATE = "{table_name}@{db_guid}"
COLUMN_QUALIFIED_NAME_TEMPLATE = "{table_name}.{column_name}@{db_guid}"

# Cabeçalhos padrão para requisições
ATLAS_HEADERS = {
    "Content-Type": "application/json"
}

# Valores default para métodos que podem ser configuráveis
LINEAGE_DEFAULT_DIRECTION = "BOTH"
LINEAGE_DEFAULT_DEPTH = 3


# Caminhos padrão dos relatórios
DISCOVERY_REPORT_JSON = "discovery_report.json"
DISCOVERY_REPORT_CSV = "discovery_report.csv"

# (Opcional) título do relatório no console
DISCOVERY_REPORT_TITLE = "=== Discovery Report ==="

# (Opcional) separador para relacionamentos de linhagem
LINEAGE_RELATIONSHIP_SEPARATOR = "_"

# Configurações do PostgreSQL
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "northwind"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

# Nome interno usado para registrar o database no Atlas
TARGET_DATABASE_NAME = "northwind_postgres"
POSTGRES_SCHEMA = "public"
