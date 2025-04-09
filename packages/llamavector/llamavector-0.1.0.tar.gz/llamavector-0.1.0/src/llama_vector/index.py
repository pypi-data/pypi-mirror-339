"""
Vector index implementation
"""
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import heapq


class Index:
    """Vector index for efficient similarity search"""
    
    def __init__(self, dimension: int, index_type: str = "hnsw"):
        """Initialize index with dimension and type"""
        self.dimension = dimension
        self.index_type = index_type
        self.vectors = {}  # id -> vector mapping
        
        # For advanced index types, we would initialize the appropriate index here
        # For now, we'll use a simple in-memory implementation
    
    def add(self, id: str, vector: np.ndarray) -> None:
        """Add vector to index"""
        if vector.shape[0] != self.dimension:
            raise ValueError(f"Vector dimension mismatch. Expected {self.dimension}, got {vector.shape[0]}")
            
        self.vectors[id] = vector
    
    def delete(self, id: str) -> bool:
        """Delete vector from index"""
        if id in self.vectors:
            del self.vectors[id]
            return True
        return False
    
    def search(self, query_vector: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """Search for similar vectors"""
        if len(self.vectors) == 0:
            return []
            
        if query_vector.shape[0] != self.dimension:
            raise ValueError(f"Query vector dimension mismatch. Expected {self.dimension}, got {query_vector.shape[0]}")
            
        # Calculate cosine similarity for all vectors
        # In a real implementation, we would use the appropriate index to make this efficient
        results = []
        for id, vector in self.vectors.items():
            # Calculate cosine similarity
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            results.append((id, float(similarity)))
            
        # Sort by similarity (descending) and return top k
        return sorted(results, key=lambda x: x[1], reverse=True)[:k]
    
    def get_nearest_neighbors(self, id: str, k: int = 10) -> List[Tuple[str, float]]:
        """Get nearest neighbors for a vector already in the index"""
        if id not in self.vectors:
            raise ValueError(f"Vector with ID {id} not found in index")
            
        query_vector = self.vectors[id]
        
        # Get results excluding the query vector itself
        results = []
        for other_id, vector in self.vectors.items():
            if other_id != id:
                # Calculate cosine similarity
                similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
                results.append((other_id, float(similarity)))
                
        # Sort by similarity (descending) and return top k
        return sorted(results, key=lambda x: x[1], reverse=True)[:k]
