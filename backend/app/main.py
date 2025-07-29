from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .chroma import collection as chroma_collection

app = FastAPI()

class Document(BaseModel):
    id: str
    text: str
    metadata: dict = None

@app.post("/add/")
async def add_document(doc: Document):
    """Add a document to ChromaDB"""
    try:
        chroma_collection.add(
            documents=[doc.text],
            metadatas=[doc.metadata] if doc.metadata else None,
            ids=[doc.id]
        )
        return {"status": "success", "id": doc.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get/{doc_id}")
async def get_document(doc_id: str):
    """Retrieve a document from ChromaDB"""
    try:
        result = chroma_collection.get(ids=[doc_id])
        if not result['documents']:
            raise HTTPException(status_code=404, detail="Document not found")
        return {
            "id": doc_id,
            "text": result['documents'][0],
            "metadata": result['metadatas'][0] if result['metadatas'] else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/search/")
async def search_documents(query: str, limit: int = 3):
    """Semantic search in ChromaDB"""
    try:
        results = chroma_collection.query(
            query_texts=[query],
            n_results=limit
        )
        return {
            "query": query,
            "results": [
                {
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "distance": results['distances'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else None
                }
                for i in range(len(results['ids'][0]))
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))