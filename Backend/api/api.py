from fastapi import FastAPI, UploadFile, File
from iaService import processAndDiagnose  # Importando do seu arquivo de serviço
import uvicorn

app = FastAPI(title="Agrosearch API")

@app.get("/")
def checkStatus():
    return {"status": "Agrosearch API is online!"}

@app.post("/diagnose")
async def diagnosePlant(file: UploadFile = File(...)):
    # 1. Pega os bytes da foto
    fileContent = await file.read()
    
    # 2. Manda para o serviço processar
    iaResult = processAndDiagnose(fileContent)
    
    # 3. Devolve a resposta
    return {
        "receivedFile": file.filename,
        "status": "success",
        "result": iaResult
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)