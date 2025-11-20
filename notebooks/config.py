# config.py

# URL do Apache Atlas
ATLAS_URL = "http://atlas:21000"

# Credenciais padrão
ATLAS_USERNAME = "admin"
ATLAS_PASSWORD = "admin"

# Configurações do PostgreSQL
POSTGRES_HOST = "postgres_erp"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "northwind"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

# Tipos para postgres - CORRIGIDOS para os tipos que EXISTEM no Atlas
ATLAS_TYPE_DATABASE = "rdbms_db"
ATLAS_TYPE_TABLE = "rdbms_table"
ATLAS_TYPE_COLUMN = "rdbms_column"
DEFAULT_DB_OWNER = "unknown"
DEFAULT_DB_DESCRIPTION = ""
DEFAULT_CLUSTER_NAME = "postgres_cluster"  # Adicionado - campo obrigatório

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

# Nome interno usado para registrar o database no Atlas
TARGET_DATABASE_NAME = "northwind_postgres"
POSTGRES_SCHEMA = "public"