from atlas_client import AtlasClient

def testar_buscas():
    client = AtlasClient()
    
    queries = [
        "*",
        "rdbms_db", 
        "rdbms_table",
        "rdbms_column",
        "meu_db_teste",
        "customers",
        "postgres_instance"
    ]
    
    for query in queries:
        print(f"\n🔍 Buscando: '{query}'")
        resultado = client.search_entities(query)
        entidades = resultado.get('entities', [])
        print(f"   Entidades encontradas: {len(entidades)}")
        
        for entity in entidades[:3]:  # Mostrar até 3
            tipo = entity.get('typeName', '')
            nome = entity.get('attributes', {}).get('name', 'N/A')
            print(f"   - {tipo}: {nome}")
        
        if len(entidades) > 3:
            print(f"   ... e mais {len(entidades) - 3} entidades")

if __name__ == "__main__":
    testar_buscas()