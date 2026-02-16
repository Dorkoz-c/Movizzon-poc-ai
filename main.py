import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Diccionario global para compartir el motor de búsqueda entre peticiones
state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Cargando documentos internos...")
    loader = DirectoryLoader('./docs', glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    texts = text_splitter.split_documents(documents)
    
    db = Chroma.from_documents(texts, OpenAIEmbeddings())
    
    state["qa_chain"] = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3})
    )
    yield
    state.clear()

app = FastAPI(title="PoC IA Corporativa V2", lifespan=lifespan)

class Question(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('La consulta no puede estar vacía o contener solo espacios')
        # Limpieza básica manteniendo caracteres especiales y números
        return " ".join(v.split())

@app.post("/ask")
async def ask(question: Question):
    qa_chain = state.get("qa_chain")
    if not qa_chain:
        raise HTTPException(status_code=503, detail="El motor de IA no está listo")
    
    try:
        response = await qa_chain.ainvoke(question.text)
        return {
            "pregunta": question.text,
            "respuesta": response["result"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))