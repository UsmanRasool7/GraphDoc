import chromadb

# New way to initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=".chromadb")  # For persistent storage
# OR for in-memory only:
# chroma_client = chromadb.EphemeralClient()

# Create/get collection
collection = chroma_client.get_or_create_collection(name="my_collection")