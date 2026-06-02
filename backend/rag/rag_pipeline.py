"""
RAG (Retrieval-Augmented Generation) Pipeline

Retrieves relevant EU AI Act legal documents to ground LLM reasoning
in actual legal text, reducing hallucination and improving accuracy.

Enhanced to support both local sentence-transformers and Ollama embeddings.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import ollama
import os


logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    RAG pipeline for EU AI Act legal document retrieval.
    
    Supports multiple embedding backends:
    - sentence-transformers (local)
    - Ollama (nomic-embed-text)
    
    Can use pre-populated ChromaDB from EUAIAct_Assistant project.
    """
    
    def __init__(
        self,
        persist_directory: str = "./data/vector_store",
        collection_name: str = "eu_ai_act_legal_corpus",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        embedding_backend: str = "sentence-transformers",
        ollama_host: str = "http://localhost:11434",
        top_k: int = 5,
        use_euaiact_data: bool = True
    ):
        """
        Initialize RAG pipeline
        
        Args:
            persist_directory: Directory for ChromaDB persistence
            collection_name: Name of ChromaDB collection
            embedding_model: Model name (sentence-transformers or Ollama model)
            embedding_backend: 'sentence-transformers' or 'ollama'
            ollama_host: Ollama server URL
            top_k: Number of documents to retrieve
            use_euaiact_data: Use EUAIAct_Assistant ChromaDB data if available
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.top_k = top_k
        self.embedding_backend = embedding_backend
        self.ollama_host = ollama_host
        
        # Check if EUAIAct_Assistant data is available
        euaiact_chroma_path = "./data/euaiact_chroma"
        if use_euaiact_data and os.path.exists(euaiact_chroma_path):
            logger.info(f"Using EUAIAct_Assistant ChromaDB data from {euaiact_chroma_path}")
            self.persist_directory = euaiact_chroma_path
            self.collection_name = "eu_ai_act"  # EUAIAct_Assistant collection name
        
        # Initialize embedding model based on backend
        if embedding_backend == "ollama":
            logger.info(f"Using Ollama embeddings: {embedding_model}")
            self.embedding_model_name = embedding_model
            self.embedding_model = None  # Ollama doesn't need local model
            self.ollama_client = ollama.Client(host=ollama_host)
        else:
            logger.info(f"Loading sentence-transformers model: {embedding_model}")
            self.embedding_model = SentenceTransformer(embedding_model)
            self.embedding_model_name = embedding_model
        
        # Initialize ChromaDB client
        logger.info(f"Initializing ChromaDB at {self.persist_directory}")
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            count = self.collection.count()
            logger.info(f"Loaded existing collection: {self.collection_name} with {count} documents")
        except Exception as e:
            logger.warning(f"Collection not found: {e}")
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "EU AI Act legal corpus"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using configured backend
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        if self.embedding_backend == "ollama":
            try:
                response = self.ollama_client.embeddings(
                    model=self.embedding_model_name,
                    prompt=text
                )
                return response["embedding"]
            except Exception as e:
                logger.error(f"Ollama embedding error: {e}")
                raise
        else:
            # sentence-transformers
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
    
    def add_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> None:
        """
        Add documents to vector store
        
        Args:
            documents: List of document dictionaries with 'text', 'metadata'
        """
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        texts = [doc['text'] for doc in documents]
        metadatas = [doc.get('metadata', {}) for doc in documents]
        ids = [doc.get('id', f"doc_{i}") for i, doc in enumerate(documents)]
        
        # Generate embeddings
        if self.embedding_backend == "ollama":
            embeddings = [self._generate_embedding(text) for text in texts]
        else:
            embeddings_array = self.embedding_model.encode(texts, show_progress_bar=True)
            embeddings = embeddings_array.tolist()
        
        # Add to collection
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Successfully added {len(documents)} documents")
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve (overrides default)
            filter_metadata: Metadata filters
            
        Returns:
            List of retrieved documents with metadata and scores
        """
        k = top_k or self.top_k
        
        logger.info(f"Retrieving top {k} documents for query: {query[:100]}...")
        
        # Generate query embedding using configured backend
        query_embedding = self._generate_embedding(query)
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filter_metadata
        )
        
        # Format results
        documents = []
        for i in range(len(results['ids'][0])):
            doc = {
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if 'distances' in results else None
            }
            documents.append(doc)
        
        logger.info(f"Retrieved {len(documents)} documents")
        return documents
    
    def retrieve_for_classification(
        self,
        ai_metadata: Dict[str, Any]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Retrieve relevant legal documents for AI system classification
        
        Args:
            ai_metadata: AI system metadata
            
        Returns:
            Tuple of (formatted_context, retrieved_documents)
        """
        # Build query from metadata
        query_parts = []
        
        if 'sector' in ai_metadata:
            query_parts.append(f"sector: {ai_metadata['sector']}")
        
        if 'purpose' in ai_metadata:
            query_parts.append(f"purpose: {ai_metadata['purpose']}")
        
        if 'biometric_identification_system' in ai_metadata:
            query_parts.append("biometric identification")
        
        if 'used_in_law_enforcement' in ai_metadata:
            query_parts.append("law enforcement")
        
        if 'creditworthiness_assessment' in ai_metadata:
            query_parts.append("creditworthiness assessment financial services")
        
        query = " ".join(query_parts) if query_parts else "AI system classification"
        
        # Retrieve documents
        documents = self.retrieve(query)
        
        # Format context for LLM
        context = self._format_context(documents)
        
        return context, documents
    
    def _format_context(
        self,
        documents: List[Dict[str, Any]]
    ) -> str:
        """
        Format retrieved documents into context string for LLM
        
        Args:
            documents: Retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            metadata = doc.get('metadata', {})
            article = metadata.get('article_number', 'Unknown')
            section = metadata.get('section', '')
            
            context_parts.append(f"[{i}] {article}")
            if section:
                context_parts.append(f"Section: {section}")
            context_parts.append(doc['text'])
            context_parts.append("")  # Blank line
        
        return "\n".join(context_parts)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        
        return {
            'collection_name': self.collection_name,
            'document_count': count,
            'persist_directory': self.persist_directory
        }


class LegalCorpusLoader:
    """
    Loader for EU AI Act legal corpus.
    
    Processes legal documents and prepares them for vector storage.
    """
    
    def __init__(self, corpus_directory: str = "./data/legal_corpus"):
        """
        Initialize corpus loader
        
        Args:
            corpus_directory: Directory containing legal documents
        """
        self.corpus_directory = Path(corpus_directory)
        logger.info(f"Initialized corpus loader for {corpus_directory}")
    
    def load_eu_ai_act(self) -> List[Dict[str, Any]]:
        """
        Load EU AI Act documents
        
        Returns:
            List of document dictionaries
        """
        documents = []
        
        # Load main articles
        documents.extend(self._load_articles())
        
        # Load annexes
        documents.extend(self._load_annexes())
        
        # Load recitals
        documents.extend(self._load_recitals())
        
        logger.info(f"Loaded {len(documents)} legal documents")
        return documents
    
    def _load_articles(self) -> List[Dict[str, Any]]:
        """Load main articles"""
        # This is a simplified example. In production, you would parse actual PDF/HTML files
        articles = [
            {
                'id': 'article_5',
                'text': """Article 5 - Prohibited AI Practices
                
                1. The following artificial intelligence practices shall be prohibited:
                
                (a) the placing on the market, putting into service or use of an AI system that deploys subliminal techniques beyond a person's consciousness in order to materially distort a person's behaviour in a manner that causes or is likely to cause that person or another person physical or psychological harm;
                
                (b) the placing on the market, putting into service or use of an AI system that exploits any of the vulnerabilities of a specific group of persons due to their age, physical or mental disability, in order to materially distort the behaviour of a person pertaining to that group in a manner that causes or is likely to cause that person or another person physical or psychological harm;
                
                (c) the placing on the market, putting into service or use of AI systems by public authorities or on their behalf for the evaluation or classification of the trustworthiness of natural persons over a certain period of time based on their social behaviour or known or predicted personal or personality characteristics, with the social score leading to either or both of the following:
                    (i) detrimental or unfavourable treatment of certain natural persons or whole groups thereof in social contexts which are unrelated to the contexts in which the data was originally generated or collected;
                    (ii) detrimental or unfavourable treatment of certain natural persons or whole groups thereof that is unjustified or disproportionate to their social behaviour or its gravity;
                
                (d) the use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purpose of law enforcement, unless and in as far as such use is strictly necessary for specific purposes.""",
                'metadata': {
                    'article_number': 'Article 5',
                    'section': 'Prohibited AI Practices',
                    'category': 'prohibited',
                    'importance': 'critical'
                }
            },
            {
                'id': 'article_6',
                'text': """Article 6 - Classification Rules for High-Risk AI Systems
                
                1. Irrespective of whether an AI system is placed on the market or put into service independently from the products referred to in points (a) and (b), that AI system shall be considered high-risk where both of the following conditions are fulfilled:
                    (a) the AI system is intended to be used as a safety component of a product, or is itself a product, covered by the Union harmonisation legislation listed in Annex II;
                    (b) the product whose safety component is the AI system, or the AI system itself as a product, is required to undergo a third-party conformity assessment with a view to the placing on the market or putting into service of that product pursuant to the Union harmonisation legislation listed in Annex II.
                
                2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall also be considered high-risk.""",
                'metadata': {
                    'article_number': 'Article 6',
                    'section': 'Classification Rules',
                    'category': 'high_risk',
                    'importance': 'critical'
                }
            },
            {
                'id': 'article_52',
                'text': """Article 52 - Transparency Obligations for Certain AI Systems
                
                1. Providers shall ensure that AI systems intended to interact with natural persons are designed and developed in such a way that natural persons are informed that they are interacting with an AI system, unless this is obvious from the circumstances and the context of use.
                
                2. Users of an emotion recognition system or a biometric categorisation system shall inform of the operation of the system the natural persons exposed thereto.
                
                3. Users of an AI system that generates or manipulates image, audio or video content that appreciably resembles existing persons, objects, places or other entities or events and would falsely appear to a person to be authentic or truthful ('deep fake'), shall disclose that the content has been artificially generated or manipulated.""",
                'metadata': {
                    'article_number': 'Article 52',
                    'section': 'Transparency Obligations',
                    'category': 'limited_risk',
                    'importance': 'high'
                }
            }
        ]
        
        return articles
    
    def _load_annexes(self) -> List[Dict[str, Any]]:
        """Load annexes"""
        annexes = [
            {
                'id': 'annex_iii_5b',
                'text': """Annex III - High-Risk AI Systems (Article 6(2))
                
                5. Access to and enjoyment of essential private services and public services and benefits:
                
                (b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems put into service by small scale providers for their own use.""",
                'metadata': {
                    'article_number': 'Annex III',
                    'section': '5(b) - Creditworthiness Assessment',
                    'category': 'high_risk',
                    'importance': 'critical'
                }
            }
        ]
        
        return annexes
    
    def _load_recitals(self) -> List[Dict[str, Any]]:
        """Load recitals"""
        recitals = [
            {
                'id': 'recital_6',
                'text': """Recital 6
                
                The notion of AI system should be clearly defined to ensure legal certainty, while providing the flexibility to accommodate future technological developments. The definition should be based on the key functional characteristics of the software, in particular the ability, for a given set of human-defined objectives, to generate outputs such as content, predictions, recommendations, or decisions which influence the environment with which the system interacts, be it in a physical or digital dimension.""",
                'metadata': {
                    'article_number': 'Recital 6',
                    'section': 'Definition of AI System',
                    'category': 'definition',
                    'importance': 'medium'
                }
            }
        ]
        
        return recitals


def initialize_rag_system(
    corpus_directory: str = "./data/legal_corpus",
    persist_directory: str = "./data/vector_store",
    embedding_backend: str = "sentence-transformers",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ollama_host: str = "http://localhost:11434",
    use_euaiact_data: bool = True
) -> RAGPipeline:
    """
    Initialize RAG system with EU AI Act corpus
    
    Args:
        corpus_directory: Directory with legal documents
        persist_directory: Directory for vector store
        embedding_backend: 'sentence-transformers' or 'ollama'
        embedding_model: Model name for embeddings
        ollama_host: Ollama server URL
        use_euaiact_data: Use EUAIAct_Assistant ChromaDB if available
        
    Returns:
        Initialized RAG pipeline
    """
    logger.info("Initializing RAG system")
    
    # Initialize pipeline with configuration
    rag = RAGPipeline(
        persist_directory=persist_directory,
        embedding_backend=embedding_backend,
        embedding_model=embedding_model,
        ollama_host=ollama_host,
        use_euaiact_data=use_euaiact_data
    )
    
    # Check if collection is empty
    stats = rag.get_collection_stats()
    
    if stats['document_count'] == 0:
        logger.info("Collection is empty, loading legal corpus")
        
        # Load corpus
        loader = LegalCorpusLoader(corpus_directory)
        documents = loader.load_eu_ai_act()
        
        # Add to vector store
        rag.add_documents(documents)
        
        logger.info("RAG system initialized with legal corpus")
    else:
        logger.info(f"RAG system initialized with {stats['document_count']} existing documents")
    
    return rag


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Initialize RAG system
    rag = initialize_rag_system()
    
    # Test retrieval
    query = "creditworthiness assessment in banking"
    documents = rag.retrieve(query, top_k=3)
    
    print(f"\nRetrieved {len(documents)} documents for query: '{query}'\n")
    
    for i, doc in enumerate(documents, 1):
        print(f"[{i}] {doc['metadata'].get('article_number', 'Unknown')}")
        print(f"Distance: {doc.get('distance', 'N/A')}")
        print(f"Text: {doc['text'][:200]}...")
        print()
    
    # Test classification retrieval
    ai_metadata = {
        'sector': 'banking',
        'purpose': 'creditworthiness_assessment'
    }
    
    context, docs = rag.retrieve_for_classification(ai_metadata)
    print("\nFormatted context for LLM:")
    print(context[:500])

# Made with Bob
