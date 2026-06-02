#!/usr/bin/env python3
"""
Test script for EUAIAct_Assistant integration
Tests the RAG pipeline with the imported ChromaDB data
"""

import sys
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.rag.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_rag_pipeline():
    """Test RAG pipeline with EUAIAct_Assistant data"""
    
    print("\n" + "="*80)
    print("Testing RAG Pipeline Integration with EUAIAct_Assistant Data")
    print("="*80 + "\n")
    
    # Test 1: Initialize with sentence-transformers
    print("Test 1: Initialize RAG with sentence-transformers embeddings")
    print("-" * 80)
    try:
        rag_st = RAGPipeline(
            embedding_backend="sentence-transformers",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            use_euaiact_data=True
        )
        
        stats = rag_st.get_collection_stats()
        print(f"✓ RAG initialized successfully")
        print(f"  Collection: {stats['collection_name']}")
        print(f"  Documents: {stats['document_count']}")
        print(f"  Directory: {stats['persist_directory']}")
        
        if stats['document_count'] == 0:
            print("  ⚠ Warning: No documents found in collection")
        
    except Exception as e:
        print(f"✗ Failed to initialize RAG: {e}")
        return False
    
    # Test 2: Test retrieval
    print("\nTest 2: Test document retrieval")
    print("-" * 80)
    try:
        test_queries = [
            "high-risk AI systems in banking",
            "prohibited AI practices",
            "biometric identification systems",
            "creditworthiness assessment"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            docs = rag_st.retrieve(query, top_k=3)
            print(f"  Retrieved: {len(docs)} documents")
            
            if docs:
                for i, doc in enumerate(docs[:2], 1):
                    metadata = doc.get('metadata', {})
                    article = metadata.get('article_number', 'Unknown')
                    doc_type = metadata.get('type', 'Unknown')
                    distance = doc.get('distance', 'N/A')
                    text_preview = doc['text'][:150].replace('\n', ' ')
                    
                    print(f"  [{i}] Article: {article}, Type: {doc_type}, Distance: {distance}")
                    print(f"      Preview: {text_preview}...")
            else:
                print("  ⚠ No documents retrieved")
        
        print("\n✓ Retrieval test completed")
        
    except Exception as e:
        print(f"✗ Retrieval test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Test classification retrieval
    print("\nTest 3: Test classification-specific retrieval")
    print("-" * 80)
    try:
        ai_metadata = {
            'sector': 'banking',
            'purpose': 'creditworthiness_assessment',
            'autonomy_level': 'fully_automated'
        }
        
        print(f"AI System Metadata: {ai_metadata}")
        context, docs = rag_st.retrieve_for_classification(ai_metadata)
        
        print(f"  Retrieved: {len(docs)} documents")
        print(f"  Context length: {len(context)} characters")
        
        if docs:
            print("\n  Top retrieved articles:")
            for i, doc in enumerate(docs[:3], 1):
                metadata = doc.get('metadata', {})
                article = metadata.get('article_number', 'Unknown')
                print(f"    [{i}] {article}")
        
        print("\n✓ Classification retrieval test completed")
        
    except Exception as e:
        print(f"✗ Classification retrieval test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*80)
    print("All tests completed successfully! ✓")
    print("="*80 + "\n")
    
    return True


def test_ollama_embeddings():
    """Test Ollama embeddings (optional - requires Ollama running)"""
    
    print("\n" + "="*80)
    print("Testing Ollama Embeddings (Optional)")
    print("="*80 + "\n")
    
    try:
        print("Attempting to initialize RAG with Ollama embeddings...")
        rag_ollama = RAGPipeline(
            embedding_backend="ollama",
            embedding_model="nomic-embed-text",
            ollama_host="http://localhost:11434",
            use_euaiact_data=True
        )
        
        stats = rag_ollama.get_collection_stats()
        print(f"✓ Ollama RAG initialized successfully")
        print(f"  Documents: {stats['document_count']}")
        
        # Test a simple query
        print("\nTesting Ollama embedding generation...")
        docs = rag_ollama.retrieve("high-risk AI systems", top_k=2)
        print(f"✓ Retrieved {len(docs)} documents with Ollama embeddings")
        
        return True
        
    except Exception as e:
        print(f"⚠ Ollama test skipped: {e}")
        print("  (This is optional - Ollama may not be running)")
        return None


if __name__ == "__main__":
    print("\n🚀 Starting Integration Tests\n")
    
    # Run main tests
    success = test_rag_pipeline()
    
    # Try Ollama test (optional)
    ollama_result = test_ollama_embeddings()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Main RAG Tests: {'✓ PASSED' if success else '✗ FAILED'}")
    if ollama_result is True:
        print(f"Ollama Tests: ✓ PASSED")
    elif ollama_result is False:
        print(f"Ollama Tests: ✗ FAILED")
    else:
        print(f"Ollama Tests: ⊘ SKIPPED")
    print("="*80 + "\n")
    
    sys.exit(0 if success else 1)

# Made with Bob
