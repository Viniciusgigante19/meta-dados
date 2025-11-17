# Apache Atlas DataOps Lab

> **Laboratório completo para aprendizado de catalogação de dados com Apache Atlas, PostgreSQL e Python**

## Sobre o Projeto

Este repositório fornece um ambiente completo de aprendizado para **Data Governance** e **DataOps** usando Apache Atlas como catálogo de dados. O projeto demonstra desde conceitos básicos até implementações avançadas de descoberta automática de metadados, linhagem de dados e integração com bancos relacionais.

### Objetivos de Aprendizado

- **Catalogação de Dados**: Criar e gerenciar catálogos de metadados
- **API Integration**: Integrar sistemas via REST APIs do Apache Atlas
- **Data Lineage**: Mapear origem e transformações de dados
- **Metadata Management**: Extrair e organizar metadados estruturais
- **DataOps Practices**: Automatizar descoberta e catalogação

## Arquitetura do Sistema

### Stack Tecnológica

| Componente | Tecnologia | Versão | Porta | Função |
|------------|------------|--------|-------|--------|
| **Catálogo** | Apache Atlas | 2.3.0 | 21000 | Governança e metadados |
| **Database** | PostgreSQL | 14.19 | 2001 | Dados de exemplo (Northwind) |
| **Analytics** | PySpark + Jupyter | Latest | 8888 | Análise e notebooks |
| **Storage** | HBase (embedded) | - | - | Persistência Atlas |
| **Search** | Apache Solr (embedded) | - | - | Indexação e busca |
| **Messaging** | Apache Kafka (embedded) | - | - | Eventos e notificações |

## 📁 Estrutura do Repositório

```
atlas-dataops-lab/
├── docker-compose.yml          # Orquestração dos serviços
├── Dockerfile                  # Atlas customizado
├── Dockerfile_Spark           # PySpark + Jupyter
├── wait-for-atlas.sh          # Script de inicialização
├── users-credentials.properties # Autenticação Atlas
│
├── 🗄️ Dados
│   ├── db/
│   │   └── northwind.sql          # Schema e dados PostgreSQL
│   └── data/                      # Datasets para análise
│
├── ├── lab/
│   │   ├── atlas_client.py        # Cliente Python para Atlas API
│   │   ├── requirements.txt       # Dependências Python
│   │   └── run_lab.sh            # Script de execução
│   │
│   └── notebooks/
│       ├── Lab_Catalogo_Postgres_no_Atlas_Documented_Fixed.ipynb
│       └── data/                  # Dados para notebooks
│
├── Exercícios
│   ├── EXERCICIO_ATLAS.md         # Exercício prático completo
│
├── README.md                  # Este arquivo
├── LICENSE                    # Licença do projeto
└── .gitignore                # Arquivos ignorados
```

## 🚀 Início Rápido

### 1. Pré-requisitos

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Python** >= 3.8 (opcional, para desenvolvimento local)
- **8GB RAM** disponível (recomendado)

### 2. Inicialização

```bash
# Clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd atlas-dataops-lab

# Iniciar todos os serviços
docker-compose up --build -d

# Aguardar inicialização (5-10 minutos)
./wait-for-atlas.sh

# Verificar status dos serviços
docker-compose ps
```

### 3. Acesso aos Serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Apache Atlas** | http://localhost:21000 | admin / admin |
| **Jupyter Notebook** | http://localhost:8888 | Token: tavares1234 |
| **PostgreSQL** | localhost:2001 | postgres / postgres |

## 🧪 Laboratórios Disponíveis

### Lab 1: Cliente Atlas Básico
```bash
cd lab
python atlas_client.py
```
**Aprenda**: Conexão com Atlas, busca de entidades, API REST

### Lab 2: Jupyter Notebook Interativo
```bash
# Acessar: http://localhost:8888 (token: tavares1234)
# Abrir: Lab_Catalogo_Postgres_no_Atlas_Documented_Fixed.ipynb
```
**Aprenda**: Extração de metadados, catalogação automática, visualização

### Lab 3: Exercício Prático Completo
```bash
# Seguir instruções em EXERCICIO_ATLAS.md
```
**Aprenda**: Implementação completa de catalogador de dados

## 🔧 Configurações Detalhadas

### Apache Atlas
- **Modo**: Standalone com componentes embedded
- **Storage**: BerkeleyDB para grafos, HBase para metadados
- **Search**: Apache Solr embedded
- **Messaging**: Kafka embedded para eventos
- **Autenticação**: File-based (users-credentials.properties)
- **Memória**: 1GB heap, 512MB inicial
- **Persistência**: Volume Docker `atlas_data`

### PostgreSQL Northwind
- **Database**: northwind (carregado automaticamente)
- **Tabelas**: 14 tabelas relacionais completas
  - `customers`, `products`, `orders`, `order_details`
  - `employees`, `categories`, `suppliers`, `shippers`
  - `territories`, `region`, `employee_territories`
  - `customer_demographics`, `customer_customer_demo`
- **Dados**: ~3000 registros com relacionamentos
- **Persistência**: Volume Docker `postgres_data`

### PySpark + Jupyter
- **Base Image**: jupyter/pyspark-notebook:latest
- **Packages**: requests, psycopg2-binary, pandas, matplotlib, seaborn
- **Volumes**: notebooks/ e data/ mapeados
- **Spark UI**: http://localhost:4040 (quando jobs estão rodando)

## 📋 Comandos Úteis

### Gerenciamento de Serviços
```bash
# Ver logs específicos
docker-compose logs -f atlas
docker-compose logs -f postgres_erp
docker-compose logs -f pyspark-aula

# Reiniciar serviço específico
docker-compose restart atlas

# Parar todos os serviços
docker-compose down

# Limpar volumes (CUIDADO: perde dados)
docker-compose down -v

# Rebuild completo
docker-compose up --build --force-recreate
```

### Diagnóstico
```bash
# Testar conectividade Atlas
curl -u admin:admin http://localhost:21000/api/atlas/admin/version

# Testar PostgreSQL
docker exec -it postgres-erp psql -U postgres -d northwind -c "SELECT count(*) FROM customers;"

# Verificar recursos
docker stats
```

## 🎓 Casos de Uso Educacionais

### 1. **Data Discovery**
- Descoberta automática de esquemas de banco
- Catalogação de tabelas e colunas
- Busca e navegação no catálogo

### 2. **Metadata Management**
- Extração de metadados estruturais
- Criação de entidades no Atlas
- Relacionamentos entre entidades

### 3. **Data Lineage**
- Mapeamento de origem dos dados
- Rastreamento de transformações
- Visualização de fluxos de dados

### 4. **API Integration**
- Uso de REST APIs do Atlas
- Autenticação e autorização
- Operações CRUD em metadados

### 5. **DataOps Automation**
- Scripts de catalogação automática
- Integração com pipelines CI/CD
- Monitoramento de qualidade de dados

## 🔍 Troubleshooting

### Problemas Comuns

**Atlas não inicia**
```bash
# Verificar memória disponível
free -h

# Aguardar mais tempo (até 10 minutos)
docker-compose logs -f atlas

# Verificar se porta está livre
netstat -tlnp | grep 21000
```

**Erro de conexão PostgreSQL**
```bash
# Verificar se container está rodando
docker-compose ps postgres_erp

# Testar conexão direta
docker exec -it postgres-erp psql -U postgres -l
```

**Jupyter não carrega**
```bash
# Verificar logs do container
docker-compose logs pyspark-aula

# Acessar com token correto
# http://localhost:8888/?token=tavares1234
```

### Logs e Monitoramento
```bash
# Logs em tempo real
docker-compose logs -f

# Uso de recursos
docker stats --no-stream

# Espaço em disco
docker system df
```

## 🤝 Contribuição

Este é um projeto educacional. Contribuições são bem-vindas:

1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra** um Pull Request

### Áreas de Melhoria
- Novos conectores de dados
- Exemplos de classificação automática
- Integração com ferramentas de BI
- Testes automatizados
- Documentação adicional

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Apache Atlas Community** - Pela excelente ferramenta de governança
- **Northwind Database** - Pelo dataset educacional clássico
- **Docker Community** - Pela containerização simplificada
- **Jupyter Project** - Pelo ambiente interativo de análise

---

**📚 Para começar, acesse os laboratórios em ordem:**
1. [Lab Python Básico](LAB_ATLAS_PYTHON.md)
2. [Exercício Prático](EXERCICIO_ATLAS.md)
3. [Notebook Interativo](notebooks/Lab_Catalogo_Postgres_no_Atlas_Documented_Fixed.ipynb)