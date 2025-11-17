# Apache Atlas - Catálogo de Dados

## 🚀 Início Rápido

```bash
# Construir e iniciar Apache Atlas 2.3.0
docker-compose up --build -d

# Aguardar inicialização (5-10 minutos)
docker-compose logs -f atlas

# Acessar Atlas
# URL: http://localhost:21000
# Usuário: admin
# Senha: admin
```

## 📋 Comandos Úteis

```bash
# Ver logs
docker-compose logs atlas

# Parar serviços
docker-compose down

# Reiniciar
docker-compose restart atlas

# Status
docker-compose ps
```

## 🔧 Configuração

- **Versão**: Apache Atlas 2.3.0
- **Porta**: 21000
- **Modo**: Standalone (embedded HBase, Kafka, Solr)
- **Autenticação**: Arquivo (admin/admin)
- **Dados**: Persistidos em volumes Docker
- **Memória**: 1GB heap, 512MB inicial
- **PostgreSQL**: Porta 2001 (banco Northwind carregado)
  - Host: localhost:2001
  - Database: northwind
  - User: postgres
  - Password: postgres
  - Tabelas: 14 tabelas com dados completos (customers, products, orders, employees, etc.)

## 🧪 Lab Python

Para demonstrações práticas com Python:

```bash
# Executar lab interativo
cd lab
./run_lab.sh

# Ou acessar Jupyter Notebook
# URL: http://localhost:8888
# Token: tavares1234
# Notebook: Lab_Atlas_Python.ipynb
```