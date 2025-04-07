import os
from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict

#custom imports
from .prompts import DEFAULT_PROMPT

#Defining everything globally for precision and loading----------------------------
_model_cache = {}
def clear_model_cache():
    """Removes all cached embedding models to free memory."""
    _model_cache.clear()

torch_DTYPE = torch.float32
#-----------------------------------------------------------------------------------

class RAGnarok:
    def __init__(self,model_name: str = "all-MiniLM-L6-v2"):
        if model_name not in _model_cache:
            _model_cache[model_name] = SentenceTransformer(model_name)
        self.model = _model_cache[model_name]
        self.documents = []
        self.embeddings = None

    def vectordb_from_document(self, chunks: List[str]) -> None:
        """
        Builds a vector database from text chunks.

        Args:
            chunks (List[str]): List of text segments to store as embeddings.
        """
        self._update_vectordb(chunks) 

    def _update_vectordb(self, texts: List[str]) -> None:
        """
        Internal function to update the vector database with new text embeddings.

        Args:
            texts (List[str]): New text data to encode and store.
        """
        if not texts:
            return
            
        self.documents.extend(texts)
        new_embeds = self.model.encode(texts, convert_to_tensor=True).to(torch_DTYPE)
        
        self.embeddings = (
            torch.cat([self.embeddings.to(torch_DTYPE), new_embeds]) 
            if self.embeddings is not None 
            else new_embeds
        )

    def saveDB_to_disk(self, path: str) -> None:
        """
        Saves the vector database to disk as a .pt file.

        Args:
            path (str): File path where the database should be saved (must end with '.pt').

        Raises:
            ValueError: If the file path is invalid.
        """
        if not isinstance(path, str) or not path.endswith('.pt'):
            raise ValueError("Path must be string ending with .pt")
            
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({
            "documents": self.documents,
            "embeddings": self.embeddings.cpu() # cuda may not exist in all devices 
        }, path)
    
    def loadDB_from_disk(self, path: str) -> None:
        """
        Loads a previously saved vector database from disk.

        Args:
            path (str): Path to a saved .pt file.

        Raises:
            ValueError: If the file does not exist or is not a valid .pt file.
        """
        if not os.path.isfile(path) or not path.endswith('.pt'):
            raise ValueError(f"Invalid file: {path} - must be existing .pt file")
            
        data = torch.load(path, map_location='cpu')
        self.documents = data["documents"]
        self.embeddings = data["embeddings"].to(torch_DTYPE)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieves the most relevant documents based on a query.

        Args:
            query (str): The input search query.
            top_k (int, optional): Number of top results to return (default: 3).

        Returns:
            List[Dict]: A list of retrieved documents with their rank and similarity score.

        Raises:
            ValueError: If no documents are available or if top_k is invalid.
        """
        if not self.documents:
            raise ValueError("No docs loaded - add data first")
            
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be positive integer")
            
        top_k = min(top_k, len(self.documents))
        query_embed = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embed, self.embeddings)[0]
        
        return [
            {"content": self.documents[i], "score": scores[i].item(), "rank": i+1}
            for i in torch.topk(scores, k=top_k).indices.cpu().numpy()
        ]
    
    def generate(self, model_pipeline, query: str, **kwargs) -> str:
        """
        Generates a response using retrieved documents as context.

        Args:
            model_pipeline: The language model pipeline for response generation.
            query (str): The input query.
            **kwargs: Additional parameters for the model pipeline.

        Returns:
            str: The generated response.
        """
        results = self.retrieve(query, top_k=kwargs.pop('top_k', 3))
        context = "\n".join(f"[{res['rank']}]: {res['content']}" for res in results)
        
        try:
            return model_pipeline(
                DEFAULT_PROMPT.format(context=context, query=query),
                **kwargs
            )
        except TypeError:
            return model_pipeline(DEFAULT_PROMPT.format(context=context, query=query)) #if kwargs have problem work without them