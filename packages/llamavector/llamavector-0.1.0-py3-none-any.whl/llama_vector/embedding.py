"""
Embedding utilities for vector store
"""
import numpy as np
from typing import List, Dict, Any, Optional, Union
import hashlib
import json


class Embedding:
    """Embedding utility class"""
    
    @staticmethod
    def normalize(vector: List[float]) -> List[float]:
        """Normalize vector to unit length"""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return (np.array(vector) / norm).tolist()
    
    @staticmethod
    def cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        v1 = np.array(vector1)
        v2 = np.array(vector2)
        
        # Handle zero vectors
        if np.all(v1 == 0) or np.all(v2 == 0):
            return 0.0
            
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    @staticmethod
    def euclidean_distance(vector1: List[float], vector2: List[float]) -> float:
        """Calculate Euclidean distance between two vectors"""
        return np.linalg.norm(np.array(vector1) - np.array(vector2))
    
    @staticmethod
    def hash_vector(vector: List[float], precision: int = 5) -> str:
        """Create a hash of a vector for deduplication"""
        # Round to reduce floating point differences
        rounded = [round(v, precision) for v in vector]
        vector_bytes = json.dumps(rounded).encode('utf-8')
        return hashlib.sha256(vector_bytes).hexdigest()
