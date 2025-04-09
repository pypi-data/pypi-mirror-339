"""Tests for vector store functionality"""
import pytest
import numpy as np
import os
import tempfile
from llama_vector.vector_store import VectorStore
from llama_vector.embedding import Embedding


@pytest.fixture
def sample_vectors():
    """Sample vectors for testing"""
    return [
        [1.0, 0.0, 0.0],  # First basis vector
        [0.0, 1.0, 0.0],  # Second basis vector
        [0.0, 0.0, 1.0],  # Third basis vector
        [0.7, 0.7, 0.0],  # Vector in first quadrant
    ]


@pytest.fixture
def sample_store(sample_vectors):
    """Sample vector store for testing"""
    store = VectorStore(dimension=3)
    
    # Add vectors with metadata
    store.add("vec1", sample_vectors[0], {"name": "First vector", "category": "basis"})
    store.add("vec2", sample_vectors[1], {"name": "Second vector", "category": "basis"})
    store.add("vec3", sample_vectors[2], {"name": "Third vector", "category": "basis"})
    store.add("vec4", sample_vectors[3], {"name": "Fourth vector", "category": "derived"})
    
    return store


def test_vector_store_initialization():
    """Test vector store initialization"""
    store = VectorStore(dimension=128)
    assert store.dimension == 128
    assert store.index_type == "hnsw"
    assert len(store.embeddings) == 0
    assert len(store.metadata) == 0


def test_add_vector(sample_vectors):
    """Test adding vectors"""
    store = VectorStore(dimension=3)
    
    # Add a vector
    store.add("test", sample_vectors[0], {"test": "metadata"})
    
    assert "test" in store.embeddings
    assert "test" in store.metadata
    assert store.metadata["test"] == {"test": "metadata"}


def test_add_batch(sample_vectors):
    """Test adding vectors in batch"""
    store = VectorStore(dimension=3)
    
    # Add batch
    ids = ["vec1", "vec2", "vec3"]
    vectors = sample_vectors[:3]
    metadatas = [
        {"name": "First"},
        {"name": "Second"},
        {"name": "Third"}
    ]
    
    store.add_batch(ids, vectors, metadatas)
    
    assert len(store.embeddings) == 3
    assert len(store.metadata) == 3
    assert "vec1" in store.embeddings
    assert "vec2" in store.embeddings
    assert "vec3" in store.embeddings


def test_search(sample_store):
    """Test vector search"""
    # Search for a vector similar to [1.0, 0.1, 0.1]
    # This should be most similar to vec1 [1.0, 0.0, 0.0]
    results = sample_store.search([1.0, 0.1, 0.1], k=2)
    
    assert len(results) == 2
    assert results[0]["id"] == "vec1"  # Most similar should be vec1
    
    # Check that metadata is included
    assert "metadata" in results[0]
    assert results[0]["metadata"]["category"] == "basis"


def test_delete(sample_store):
    """Test deleting vectors"""
    # Delete a vector
    assert sample_store.delete("vec1") == True
    
    # Check it's gone
    assert "vec1" not in sample_store.embeddings
    assert "vec1" not in sample_store.metadata
    
    # Try to delete again (should return False)
    assert sample_store.delete("vec1") == False


def test_save_load():
    """Test saving and loading vector store"""
    # Create a vector store
    store = VectorStore(dimension=3)
    store.add("test", [1.0, 2.0, 3.0], {"name": "Test vector"})
    
    # Save it
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name
        
    try:
        store.save(temp_path)
        
        # Load it
        loaded_store = VectorStore.load(temp_path)
        
        # Check it loaded correctly
        assert loaded_store.dimension == 3
        assert "test" in loaded_store.embeddings
        assert "test" in loaded_store.metadata
        assert loaded_store.metadata["test"]["name"] == "Test vector"
        
        # Check the vector is the same
        np.testing.assert_array_almost_equal(
            loaded_store.embeddings["test"],
            np.array([1.0, 2.0, 3.0])
        )
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
