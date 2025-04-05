import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from translator import DeepSeekTranslator

app = FastAPI()
translator = DeepSeekTranslator()

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "korean"
    target_lang: str = "chinese"

@app.get("/")
def read_root():
    return {"message": "DeepSeek Translator MCP API"}

@app.get("/mcp_config.json")
def get_mcp_config():
    try:
        with open("mcp_config.json", "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load MCP config: {str(e)}")

@app.post("/translate")
def translate_text(request: TranslationRequest):
    try:
        translated_text = translator.translate(
            request.text, 
            source_lang=request.source_lang, 
            target_lang=request.target_lang
        )
        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

# MCP 함수 호출을 위한 엔드포인트
@app.post("/mcp/translate")
def translate_mcp(data: dict):
    try:
        text = data.get("text", "")
        if not text:
            raise ValueError("No text provided for translation")
        
        translated_text = translator.translate(text)
        return {"result": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MCP translation failed: {str(e)}")

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=4000)

if __name__ == "__main__":
    start_server() 