"""
Vector store implementation for LlamaVector
"""
import numpy as np
import os
import pickle
from typing import Dict, List, Any, Optional, Union, Tuple

from .embedding import Embedding
from .index import Index
from .query import Query


class VectorStore:
    """Storage and retrieval engine for vector embeddings"""
    
    def __init__(self, dimension: int = 768, index_type: str = "hnsw"):
        """Initialize vector store with embedding dimension and index type"""
        self.dimension = dimension
        self.index_type = index_type
        self.embeddings = {}
        self.metadata = {}
        self.index = Index(dimension, index_type)
        
    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add vector embedding to the store with optional metadata"""
        if len(vector) != self.dimension:
            raise ValueError(f"Vector dimension mismatch. Expected {self.dimension}, got {len(vector)}")
            
        self.embeddings[id] = np.array(vector, dtype=np.float32)
        if metadata:
            self.metadata[id] = metadata
            
        self.index.add(id, self.embeddings[id])
        
    def add_batch(self, ids: List[str], vectors: List[List[float]], metadatas: Optional[List[Dict[str, Any]]] = None) -> None:
        """Add batch of vector embeddings to the store"""
        if len(ids) != len(vectors):
            raise ValueError("Number of IDs and vectors must match")
            
        if metadatas and len(ids) != len(metadatas):
            raise ValueError("Number of IDs and metadata items must match")
            
        for i, (id, vector) in enumerate(zip(ids, vectors)):
            metadata = metadatas[i] if metadatas else None
            self.add(id, vector, metadata)
            
    def search(self, query_vector: List[float], k: int = 10, include_metadata: bool = True) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        if len(query_vector) != self.dimension:
            raise ValueError(f"Query vector dimension mismatch. Expected {self.dimension}, got {len(query_vector)}")
            
        query_vec = np.array(query_vector, dtype=np.float32)
        results = self.index.search(query_vec, k)
        
        if include_metadata:
            return [
                {
                    "id": id,
                    "score": score,
                    "metadata": self.metadata.get(id, {})
                }
                for id, score in results
            ]
        else:
            return [
                {
                    "id": id,
                    "score": score
                }
                for id, score in results
            ]
            
    def delete(self, id: str) -> bool:
        """Delete vector by ID"""
        if id in self.embeddings:
            del self.embeddings[id]
            if id in self.metadata:
                del self.metadata[id]
                
            self.index.delete(id)
            return True
        return False
        
    def save(self, path: str) -> None:
        """Save vector store to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'dimension': self.dimension,
                'index_type': self.index_type,
                'embeddings': self.embeddings,
                'metadata': self.metadata
            }, f)
            
    @classmethod
    def load(cls, path: str) -> 'VectorStore':
        """Load vector store from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            
        store = cls(dimension=data['dimension'], index_type=data['index_type'])
        store.embeddings = data['embeddings']
        store.metadata = data['metadata']
        
        # Rebuild index
        for id, vector in store.embeddings.items():
            store.index.add(id, vector)
            
        return store
