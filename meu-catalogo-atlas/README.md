# Como testar os arquivos.py.

## 1- Copia todos os arquivos da raiz do projeto
Use o comando a seguir no caminho ilustrado dentro do projeto para 
copiar toda a pasta /meu-catalogo-atlas para o conteiner pyspark.



```
PATH : .../meta-dados
docker cp /workspaces/meta-dados/meu-catalogo-atlas/. pyspark_aula_container:/home/jovyan/work/
```


## 2-  Entra no ambiente que executa arquivos py 
Para executar os testes use o comando indicado no caminho ilustrado.



```
PATH : .../meta-dados
docker exec -it pyspark_aula_container bash
```

## 3- Área de testes:

Após o passo 2 você estará em  "jovyan@32b9d79df5f9:~/work$" no terminal e aqui rode 
os comandos a seguir para rodar cada arquivo do projeto

### TESTE 

```
python atlas_client.py
python data_catalogger.py
python discovery_report.py
python postgres_extractor.py
```
E para arquivos dentro de /tests faça:
```
cd tests   

python test_atlas_client.py
python test_catalogger.py
python test_extractor.py
```


# Catálogo de Dados com Apache Atlas

## Visão Geral
Este projeto implementa um sistema de catalogação de dados que integra **PostgreSQL** com **Apache Atlas**, permitindo:

- Descoberta automática de metadados
- Criação de entidades no catálogo de dados
- Implementação de linhagem de dados (data lineage)
- Geração de relatórios de descoberta

O projeto foi desenvolvido seguindo boas práticas de **DataOps** e usa Python para a integração com a API do Atlas.

---

## Estrutura do Projeto

meu-catalogo-atlas/
├── README.md # Este arquivo: documentação do projeto
├── requirements.txt # Dependências Python
├── config.py # Configurações de conexão com Atlas e PostgreSQL
├── atlas_client.py # Tarefa 1: cliente Python para conectar com Apache Atlas
├── postgres_extractor.py # Tarefa 2: extrator de metadados do PostgreSQL
├── postgres_cataloger.py # Tarefa 3: catalogador automático de database, tabelas e colunas
├── discovery_report.py # Tarefa 4: gera relatórios de descoberta (JSON e CSV)
├── main.py # Script principal para executar todo o fluxo
└── tests/ # Testes unitários opcionais
├── test_atlas_client.py
├── test_extractor.py
└── test_catalogger.py



---

## Descrição dos Arquivos

### `config.py`
Armazena todas as configurações do projeto:
- **ATLAS_CONFIG**: URL do Apache Atlas, usuário e senha.
- **POSTGRES_CONFIG**: host, porta, database, usuário e senha do PostgreSQL.
- **DATABASE_NAME**: nome do database a ser catalogado.

---

### `atlas_client.py`
Classe **`AtlasClient`**: cliente para interagir com a API REST do Apache Atlas.

Principais funções:
- Conexão com Apache Atlas usando **HTTP Basic Auth**
- Métodos:
  - `search_entities(query)` → busca entidades pelo termo
  - `create_entity(entity_data)` → cria entidades no Atlas
  - `get_entity(guid)` → obtém entidade específica pelo GUID
  - `get_lineage(guid)` → retorna linhagem (data lineage) da entidade

---

### `postgres_extractor.py`
Classe **`PostgreSQLExtractor`**: extrai metadados do PostgreSQL.

Principais funções:
- Conecta ao banco PostgreSQL
- Métodos:
  - `list_tables()` → retorna todas as tabelas do schema `public`
  - `get_columns(table_name)` → retorna colunas de uma tabela com tipo e nullable
  - `close()` → fecha a conexão com o banco

---

### `postgres_cataloger.py`
Classe **`PostgresCataloger`**: catalogador automático de banco de dados, tabelas e colunas.

Principais funções:
- Recebe instâncias de `AtlasClient` e `PostgreSQLExtractor`
- Métodos:
  - `catalog_database(db_name)` → cria entidade do database no Atlas e salva GUID
  - `catalog_all_tables()` → cria entidades de tabelas e colunas no Atlas e retorna resumo

---

### `discovery_report.py`
Classe **`DiscoveryReport`**: gera relatórios de descoberta do catálogo.

Principais funções:
- Recebe instâncias de `AtlasClient` e `PostgresCataloger`
- Método `build_report(report_json_path, report_csv_path)`:
  - Lista tabelas catalogadas e suas colunas
  - Busca relacionamentos (linhagem) das tabelas
  - Salva relatório em **JSON** e **CSV**
  - Mostra estatísticas no console:
    - Total de databases, tabelas, colunas
    - Tabela com mais colunas
    - Tabelas com relacionamentos

---

### `main.py`
Script principal que integra todos os componentes:

Fluxo de execução:
1. Carrega configurações do `config.py`
2. Inicializa `AtlasClient`, `PostgreSQLExtractor`, `PostgresCataloger` e `DiscoveryReport`
3. Catalogação do database
4. Catalogação de todas as tabelas e colunas
5. Geração de relatório de descoberta
6. Fecha conexão com o PostgreSQL

---

### `tests/`
Contém testes unitários (opcionais):
- `test_atlas_client.py` → testes para métodos do AtlasClient
- `test_extractor.py` → testes para métodos do PostgreSQLExtractor
- `test_catalogger.py` → testes para métodos do PostgresCataloger
