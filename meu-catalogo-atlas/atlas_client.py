import requests
from requests.auth import HTTPBasicAuth
from config import (
    ATLAS_URL,
    ATLAS_USERNAME,
    ATLAS_PASSWORD,
    ATLAS_HEADERS,
    LINEAGE_DEFAULT_DIRECTION,
    LINEAGE_DEFAULT_DEPTH
)


class AtlasClient:
    def __init__(self, url=ATLAS_URL, username=ATLAS_USERNAME, password=ATLAS_PASSWORD):
        self.url = url
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update(ATLAS_HEADERS)

    def search_entities(self, query):
        endpoint = f"{self.url}/api/atlas/v2/search/basic"
        params = {"query": query}
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def create_entity(self, entity_data):
        print(">>> Enviando payload para Atlas:")
        print(entity_data)  # log do JSON que vai no POST
        endpoint = f"{self.url}/api/atlas/v2/entity/bulk"  # ← MUDEI PARA /bulk
        response = self.session.post(endpoint, json=entity_data)
        
        # DEBUG: Mostrar resposta completa do erro
        if response.status_code != 200:
            print(f"!!! ERRO {response.status_code}:")
            print(f"!!! Response Headers: {response.headers}")
            print(f"!!! Response Text: {response.text}")
            print(f"!!! URL: {response.url}")
        
        response.raise_for_status()
        return response.json()

    def get_entity(self, guid):
        endpoint = f"{self.url}/api/atlas/v2/entity/guid/{guid}"
        response = self.session.get(endpoint)
        response.raise_for_status()
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()

    def get_lineage(self, guid, direction=LINEAGE_DEFAULT_DIRECTION, depth=LINEAGE_DEFAULT_DEPTH):
        endpoint = f"{self.url}/api/atlas/v2/lineage/{guid}"
        params = {"direction": direction, "depth": depth}
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
        else:
            raise ValueError(f"Resposta não é JSON: {response.text}")

# Adicione isto no final do arquivo atlas_client.py:

if __name__ == "__main__":
    print("🧪 Testando AtlasClient...")
    
    client = AtlasClient()
    
    try:
        # Testar conexão básica
        print("✅ AtlasClient criado com sucesso")
        
        # Testar busca
        result = client.search_entities("*")
        entities_count = len(result.get('entities', []))
        print(f"✅ Busca retornou {entities_count} entidades")
        
        # Testar get_entity (pegar primeira entidade se existir)
        if entities_count > 0:
            first_guid = result['entities'][0]['guid']
            entity = client.get_entity(first_guid)
            print(f"✅ Get_entity funcionou para GUID: {first_guid[:8]}...")
        
        print("🎉 AtlasClient TESTADO E APROVADO!")
        
    except Exception as e:
        print(f"❌ Erro no AtlasClient: {e}")