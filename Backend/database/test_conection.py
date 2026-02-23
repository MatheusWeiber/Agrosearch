# Importa direto do arquivo vizinho (database.py)
from database import client

response = client.table("diseases_catalog").select("*").execute()

print(" Conexão realizada! Dados recebidos:")
print(response.data)