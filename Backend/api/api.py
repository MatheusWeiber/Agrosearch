from fastapi import FastAPI, UploadFile, File, Form
from iaService import processAndDiagnose
from database.database import saveDiagnosticRecord 
import uvicorn

app = FastAPI(title="Agrosearch API")

@app.post("/diagnose")
async def diagnosePlant(
    # Agora a rota exige a foto E o ID do usuário
    file: UploadFile = File(...),
    user_id: str = Form(...) 
):
    # 1. Pega os bytes da foto
    fileContent = await file.read()
    
    # 2. Manda para a IA processar
    iaResult = processAndDiagnose(fileContent)
    
    # 3. Salva no banco de dados vinculando ao usuário!
    try:
        saveDiagnosticRecord(
            user_id=user_id, 
            diagnostic=iaResult["diagnostic"], 
            confidence=iaResult["confidence"]
        )
    except Exception as dbError:
        print(f" Falha ao salvar no banco: {dbError} ")
    
    # 4. Devolve a resposta
    return {
        "status": "success",
        "result": iaResult
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)