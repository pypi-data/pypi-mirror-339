"""
Query utilities for vector store
"""
from typing import Dict, List, Any, Optional, Union
import numpy as np


class Query:
    """Query class for vector store"""
    
    def __init__(self, vector: Optional[List[float]] = None, filters: Optional[Dict[str, Any]] = None):
        """Initialize query with vector and filters"""
        self.vector = vector
        self.filters = filters or {}
        
    def set_vector(self, vector: List[float]) -> 'Query':
        """Set query vector"""
        self.vector = vector
        return self
        
    def set_filter(self, key: str, value: Any) -> 'Query':
        """Set filter key-value pair"""
        self.filters[key] = value
        return self
        
    def set_filters(self, filters: Dict[str, Any]) -> 'Query':
        """Set multiple filters"""
        self.filters.update(filters)
        return self
        
    def clear_filters(self) -> 'Query':
        """Clear all filters"""
        self.filters = {}
        return self
        
    def matches_filters(self, metadata: Dict[str, Any]) -> bool:
        """Check if metadata matches filters"""
        if not self.filters:
            return True
            
        for key, value in self.filters.items():
            if key not in metadata:
                return False
                
            if isinstance(value, list):
                # Filter by list of allowed values
                if metadata[key] not in value:
                    return False
            elif callable(value):
                # Filter by function
                if not value(metadata[key]):
                    return False
            else:
                # Filter by exact match
                if metadata[key] != value:
                    return False
                    
        return True
