from sentence_transformers import SentenceTransformer
from config import settings  # Import the instance, not the class

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
        self.model_name = settings.embedding_model
        
    def generate_embedding(self, text: str) -> list:
        embedding = self.model.encode(text)
        return embedding.tolist()     

# Initialize the service
embedding_service = EmbeddingService()