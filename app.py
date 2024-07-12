from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from support import retriever, model, tokenizer
import torch

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Question(BaseModel):
    text: str

@app.post("/ask")
async def ask_question(question: Question):
    try:
        # Retrieve relevant documents
        docs = retriever.invoke(question.text)
        context = " ".join([doc.page_content for doc in docs])

        # Prepare input for the model
        input_text = f"Context: {context}\n\nQuestion: {question.text}\n\nAnswer:"
        inputs = tokenizer(input_text, max_length=1024, return_tensors="pt", truncation=True)

        # Generate response
        with torch.no_grad():
            summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, num_beams=4, early_stopping=True)
        
        response = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return JSONResponse(content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Diamante Chatbot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
