# Exercício Prático: Catálogo de Dados com Apache Atlas

## Objetivo
Criar um sistema de catalogação de dados que integre PostgreSQL com Apache Atlas, implementando descoberta automática de metadados e criação de linhagem de dados.

## Competências Avaliadas
- Integração com APIs REST do Apache Atlas
- Extração de metadados de bancos de dados
- Criação de entidades no catálogo de dados
- Implementação de linhagem de dados (data lineage)
- Boas práticas de DataOps

## Pré-requisitos

### 1. Ambiente
```bash
# Clonar o repositório base
git clone https://github.com/AleTavares/atlas-dataops-lab.git
cd atlas-dataops-lab

# Iniciar ambiente
docker-compose up -d

# Aguardar inicialização (5-10 minutos)
docker-compose logs -f atlas
```

### 2. Verificar Serviços
- **Apache Atlas**: http://localhost:21000 (admin/admin)
- **PostgreSQL**: localhost:2001 (postgres/postgres)
- **Jupyter**: http://localhost:8888 (token: tavares1234)

## Tarefas do Exercício

### Tarefa 1: Cliente Atlas (25 pontos)
Implementar uma classe `AtlasClient` que:

**Requisitos:**
- Conecte com Apache Atlas via API REST
- Implemente autenticação HTTP Basic
- Tenha métodos para:
  - `search_entities(query)` - buscar entidades
  - `create_entity(entity_data)` - criar entidade
  - `get_entity(guid)` - obter entidade por GUID
  - `get_lineage(guid)` - obter linhagem de uma entidade

**Critérios de Avaliação:**
- Tratamento de erros HTTP
- Documentação dos métodos
- Uso correto da API do Atlas

### Tarefa 2: Extrator de Metadados (30 pontos)
Criar classe `PostgreSQLExtractor` que:

**Requisitos:**
- Conecte ao PostgreSQL Northwind
- Extraia metadados de todas as tabelas:
  - Nome da tabela
  - Colunas (nome, tipo, nullable)
  - Chaves primárias
  - Relacionamentos (foreign keys)
- Retorne dados estruturados (dicionário/DataFrame)

**Critérios de Avaliação:**
- Conexão segura com banco
- Extração completa de metadados
- Estrutura de dados organizada
- Tratamento de exceções

### Tarefa 3: Catalogador Automático (35 pontos)
Implementar classe `DataCatalogger` que:

**Requisitos:**
- Use `AtlasClient` e `PostgreSQLExtractor`
- Crie automaticamente no Atlas:
  - Database (northwind_postgres)
  - Tabelas com metadados completos
  - Colunas vinculadas às tabelas
- Implemente método `catalog_all_tables()`
- Crie linhagem entre tabelas relacionadas

**Critérios de Avaliação:**
- Integração correta entre componentes
- Criação de entidades hierárquicas
- Linhagem de dados implementada
- Logs informativos do processo

### Tarefa 4: Relatório de Descoberta (10 pontos)
Criar script `discovery_report.py` que:

**Requisitos:**
- Gere relatório das entidades catalogadas
- Mostre estatísticas:
  - Total de databases, tabelas, colunas
  - Tabelas com mais colunas
  - Relacionamentos encontrados
- Exporte relatório em JSON e CSV

**Critérios de Avaliação:**
- Relatório completo e informativo
- Múltiplos formatos de saída
- Apresentação clara dos dados

## Estrutura de Entrega

Seu repositório deve conter:

```
meu-catalogo-atlas/
├── README.md                 # Documentação do projeto
├── requirements.txt          # Dependências Python
├── config.py                # Configurações
├── atlas_client.py          # Tarefa 1
├── postgres_extractor.py    # Tarefa 2  
├── data_catalogger.py       # Tarefa 3
├── discovery_report.py      # Tarefa 4
├── main.py                  # Script principal
└── tests/                   # Testes unitários (opcional)
    ├── test_atlas_client.py
    ├── test_extractor.py
    └── test_catalogger.py
```

## Especificações Técnicas

### Configurações (config.py)
```python
ATLAS_CONFIG = {
    "url": "http://localhost:21000",
    "username": "admin", 
    "password": "admin"
}

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 2001,
    "database": "northwind",
    "user": "postgres",
    "password": "postgres"
}
```

### Dependências Mínimas
```txt
requests>=2.28.0
pandas>=1.5.0
psycopg2-binary>=2.9.0
```

## Exemplo de Uso Esperado

```python
# main.py
from atlas_client import AtlasClient
from postgres_extractor import PostgreSQLExtractor
from data_catalogger import DataCatalogger
from discovery_report import DiscoveryReport

def main():
    # Inicializar componentes
    atlas = AtlasClient(**ATLAS_CONFIG)
    extractor = PostgreSQLExtractor(**POSTGRES_CONFIG)
    catalogger = DataCatalogger(atlas, extractor)
    
    # Catalogar dados
    print("🔄 Iniciando catalogação...")
    results = catalogger.catalog_all_tables()
    print(f"✅ {results['tables_created']} tabelas catalogadas")
    
    # Gerar relatório
    report = DiscoveryReport(atlas)
    report.generate_report("discovery_report")
    print("📊 Relatório gerado!")

if __name__ == "__main__":
    main()
```

## Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Funcionalidade** | 40% | Código funciona conforme especificado |
| **Qualidade** | 25% | Estrutura, legibilidade, boas práticas |
| **Documentação** | 20% | README, comentários, docstrings |
| **Inovação** | 15% | Funcionalidades extras, melhorias |

### Pontuação Extra (até 20 pontos)
- **Testes unitários** (+10 pontos)
- **Interface web simples** (+10 pontos)  
- **Classificação automática de dados** (+5 pontos)
- **Detecção de dados sensíveis** (+5 pontos)

## Entrega

### 1. Criar Repositório
- Criar repositório público no GitHub
- Nome sugerido: `atlas-data-catalog-[SEU_NOME]`
- Incluir README.md detalhado

### 2. Submeter Solução
**Preencher formulário:** [Link do Google Forms]

**Informações necessárias:**
- Nome completo
- Email
- Link do repositório GitHub
- Vídeo demonstração (opcional, +5 pontos)

### 3. Prazo
**Data limite:** [DATA_LIMITE]  
**Horário:** 23:59

## Dicas de Implementação

### Atlas API Endpoints Úteis
```python
# Buscar entidades
GET /api/atlas/v2/search/basic?query={term}

# Criar entidade
POST /api/atlas/v2/entity/bulk
{
  "entities": [
    {
      "typeName": "hive_table",
      "attributes": {...}
    }
  ]
}

# Obter linhagem
GET /api/atlas/v2/lineage/{guid}
```

### Estrutura de Entidade Tabela
```python
table_entity = {
    "typeName": "hive_table",
    "attributes": {
        "name": "customers",
        "qualifiedName": "northwind.customers@cluster1",
        "db": {"guid": database_guid},
        "owner": "postgres",
        "description": "Tabela de clientes"
    }
}
```

### Estrutura de Entidade Coluna
```python
column_entity = {
    "typeName": "hive_column", 
    "attributes": {
        "name": "customer_id",
        "qualifiedName": "northwind.customers.customer_id@cluster1",
        "table": {"guid": table_guid},
        "type": "character varying",
        "position": 1
    }
}
```

## Suporte

### Recursos Disponíveis
- **Documentação Atlas**: https://atlas.apache.org/
- **Banco Northwind**: 14 tabelas com relacionamentos
- **Exemplos no repositório**: `/notebooks/` e `/lab/`

### Problemas Comuns
1. **Atlas não inicia**: Aguardar 5-10 minutos, verificar logs
2. **Erro de conexão**: Verificar se containers estão rodando
3. **Timeout API**: Implementar retry com backoff

## Bons Estudos!

**Lembre-se:** este exercício simula um cenário real de DataOps. Foque na qualidade, documentação e funcionalidade. Demonstre seu conhecimento em catalogação de dados e integração de sistemas!

