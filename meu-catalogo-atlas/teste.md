# Copia todos os arquivos da raiz do projeto
docker cp /workspaces/meta-dados/meu-catalogo-atlas/. pyspark_aula_container:/home/jovyan/work/

# Entra no ambiente que executa arquivos py
docker exec -it pyspark_aula_container bash

# Copia a pasta de testes inteira
docker cp /workspaces/meta-dados/meu-catalogo-atlas/tests pyspark_aula_container:/home/jovyan/work/
