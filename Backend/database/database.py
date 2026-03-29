import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# 2. Cria a conexão com o seu banco
supabase: Client = create_client(url, key)

def saveDiagnosticRecord(user_id: str, diagnostic: str, confidence: float):
    
    try:
        dados_para_salvar = {
            "user_id": user_id,
            "diagnostic": diagnostic,
            "confidence": confidence
        }
        
        # Faz o INSERT na tabela prediction
        resposta = supabase.table("prediction").insert(dados_para_salvar).execute()
        
        print(f" Salvo no banco com sucesso: {diagnostic}")
        return True
    
    except Exception as e:
        print(f" Erro ao salvar no Supabase: {e}")
        return False