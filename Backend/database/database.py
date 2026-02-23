import os
from dotenv import load_dotenv, find_dotenv
from supabase import create_client

# Carrega as variáveis
load_dotenv(find_dotenv())

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print(" Erro: Variáveis não encontradas no .env")
else:
    client = create_client(url, key)