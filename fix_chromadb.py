#!/usr/bin/env python3
"""
Fix ChromaDB initialization issue

This script reinitializes ChromaDB with the correct schema and populates it
with EU AI Act legal documents.
"""

import sys
import shutil
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from rag.rag_pipeline import initialize_rag_system, LegalCorpusLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_chromadb():
    """Fix ChromaDB initialization"""
    
    print("=" * 80)
    print("ChromaDB Fix Script")
    print("=" * 80)
    
    # Step 1: Remove old ChromaDB data
    chroma_paths = [
        "./data/vector_store",
        "./data/euaiact_chroma"
    ]
    
    for path in chroma_paths:
        if Path(path).exists():
            print(f"\n[1] Removing old ChromaDB data: {path}")
            try:
                shutil.rmtree(path)
                print(f"    ✓ Removed {path}")
            except Exception as e:
                print(f"    ⚠ Could not remove {path}: {e}")
        else:
            print(f"\n[1] Path does not exist: {path}")
    
    # Step 2: Initialize fresh ChromaDB with legal documents
    print("\n[2] Initializing fresh ChromaDB with EU AI Act documents...")
    
    try:
        # Initialize RAG system (this will create new ChromaDB)
        rag = initialize_rag_system(
            persist_directory="./data/vector_store",
            embedding_backend="sentence-transformers",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            use_euaiact_data=False  # Don't try to use old data
        )
        
        print("    ✓ ChromaDB initialized successfully")
        
        # Step 3: Verify documents were loaded
        stats = rag.get_collection_stats()
        print(f"\n[3] Verification:")
        print(f"    Collection: {stats['collection_name']}")
        print(f"    Documents: {stats['document_count']}")
        print(f"    Directory: {stats['persist_directory']}")
        
        if stats['document_count'] > 0:
            print("\n✓ ChromaDB fix complete!")
            print("\nYou can now restart the backend:")
            print("  docker compose restart backend")
        else:
            print("\n⚠ Warning: No documents loaded")
            print("  The system will still work but may have limited legal references")
        
    except Exception as e:
        print(f"\n✗ Error initializing ChromaDB: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = fix_chromadb()
    sys.exit(0 if success else 1)

# Made with Bob
