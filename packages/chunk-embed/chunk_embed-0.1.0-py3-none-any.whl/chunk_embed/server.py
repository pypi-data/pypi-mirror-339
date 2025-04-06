import os
import shutil
import argparse
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import logging
import psutil
from tqdm import tqdm
import time

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process documents and create embeddings.')
    
    parser.add_argument('--base_dir', 
                        type=str, 
                        required=True,
                        help='Directory containing your documents (MANDATORY)')
    
    parser.add_argument('--collection_name', 
                        type=str, 
                        required=True,
                        help='Name for the Chroma collection (MANDATORY)')
    
    parser.add_argument('--embedding_model_name', 
                        type=str, 
                        required=True,
                        help='Path to the sentence transformer model (MANDATORY)')
    
    parser.add_argument('--persist_dir', 
                        type=str, 
                        required=True,
                        help='Directory to persist the Chroma database (MANDATORY)')
    
    parser.add_argument('--chunk_size', 
                        type=int, 
                        default=500,
                        help='Size of text chunks (default: 500)')
    
    parser.add_argument('--chunk_overlap', 
                        type=int, 
                        default=50,
                        help='Overlap between text chunks (default: 50)')
    
    parser.add_argument('--batch_size', 
                        type=int, 
                        default=1000,
                        help='Batch size for processing (default: 1000)')
    
    parser.add_argument('--memory_threshold_mb', 
                        type=int, 
                        default=8000,
                        help='Memory threshold in MB (default: 8000)')
    
    parser.add_argument('--max_retries', 
                        type=int, 
                        default=3,
                        help='Maximum retries for embedding generation (default: 3)')
    
    args = parser.parse_args()
    
    # Validate base_dir exists
    if not os.path.isdir(args.base_dir):
        parser.error(f"ERROR: Base directory '{args.base_dir}' does not exist or is not accessible")
    
    # Additional validation for collection name
    if not args.collection_name or args.collection_name.isspace():
        parser.error("ERROR: Collection name cannot be empty")
        
    # Validate embedding_model_name exists
    if not os.path.exists(args.embedding_model_name):
        parser.error(f"ERROR: Embedding model '{args.embedding_model_name}' does not exist or is not accessible")
    
    # Check if persist_dir can be created if it doesn't exist
    persist_parent = os.path.dirname(args.persist_dir)
    if not os.path.exists(args.persist_dir) and not os.path.isdir(persist_parent):
        parser.error(f"ERROR: Parent directory for persist_dir '{persist_parent}' does not exist or is not accessible")
    
    return args

############################################
# Configuration
############################################
# Constants for file extensions
FILE_EXTENSIONS = ('.c', '.cc', '.cjs', '.coffee', '.cs', '.css', '.d', '.ejs', '.flow', '.h', '.html', '.iml', '.java', '.js', '.jst', '.less', '.njs', '.php', '.py', '.scss', '.sh', '.sql', '.ts', '.tsx', '.conf', '.yml', '.toml', '.xml', '.gyp', '.gypi', '.lock', '.tf', '.tfvars', '.Makefile', '.mk', '.md', '.markdown', '.DOCS', '.txt', '.LICENSE', '.MIT', '.asm', '.s', '.cpp', '.hpp', '.hxx', '.cxx', '.jsx', '.vue', '.svelte', '.rb', '.erb', '.haml', '.slim', '.lua', '.pl', '.pm', '.t', '.perl', '.go', '.rs', '.dart', '.kt', '.scala', '.clj', '.elm', '.ex', '.exs', '.erl', '.fs', '.fsx', '.groovy', '.hs', '.swift', '.m', '.mm', '.cmake', '.gradle', '.bazel', '.bzl', '.ninja', '.dockerfile', '.dockerignore', '.editorconfig', '.gitignore', '.env', '.yaml', '.properties', '.json', '.bat', '.cmd', '.component', '.csv', '.db', '.db-journal', '.def', '.el', '.htm', '.impex', '.in', '.jsp', '.log', '.map', '.nix', '.patch', '.prefs', '.raml', '.svn-base', '.tag', '.template', '.test', '.tld', '.tmpl', '.tpl', '.vm', '.xmi', '.xsd', '.xsl')

CHECKPOINT_FILE = "embedding_checkpoint.txt"
############################################

# Configure logging to display informational messages
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_memory_usage(memory_threshold_mb):
    """Monitor memory usage and return True if above threshold."""
    memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    if memory > memory_threshold_mb:
        logger.warning(f"High memory usage: {memory:.2f} MB")
        return True
    return False

def load_files(base_dir, file_extensions):
    """Load files with error handling and progress tracking."""
    documents = []
    all_files = []
    
    # First, collect all files
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(file_extensions):
                all_files.append(os.path.join(root, file))
    
    # Process files with progress bar
    for filepath in tqdm(all_files, desc="Loading files"):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            if text.strip():  # Only add non-empty documents
                documents.append((filepath, text))
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            continue
    
    return documents

def chunk_text(text, chunk_size=500, overlap=50):
    """chunking with handling of code structures."""
    chunks = []
    start = 0
    length = len(text)
    
    while start < length:
        end = start + chunk_size
        
        # Adjust chunk end to avoid breaking in the middle of a line
        if end < length:
            # Try to find the nearest newline
            newline_pos = text.find('\n', end)
            if newline_pos != -1 and newline_pos - end < 50:  # Within reasonable distance
                end = newline_pos + 1
        
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks

def save_checkpoint(processed_count):
    """Save progress checkpoint."""
    with open(CHECKPOINT_FILE, 'w') as f:
        f.write(str(processed_count))

def load_checkpoint():
    """Load progress checkpoint."""
    try:
        with open(CHECKPOINT_FILE, 'r') as f:
            return int(f.read())
    except:
        return 0

def generate_embeddings(texts, embedding_model, max_retries):
    """Generate embeddings with retry mechanism."""
    for attempt in range(max_retries):
        try:
            embeddings = embedding_model.encode(
                texts, 
                convert_to_numpy=True, 
                show_progress_bar=True,
                batch_size=32  # Smaller batch size for embedding generation
            )
            return embeddings
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Embedding generation failed, attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(1)  # Wait before retry
            else:
                raise

def serve():    
    # Parse command-line arguments
    # If arguments are not provided, argparse will exit the program with an error message
    args = parse_arguments()
    
    # Use command-line arguments for mandatory parameters
    BASE_DIR = args.base_dir
    COLLECTION_NAME = args.collection_name
    EMBEDDING_MODEL_NAME = args.embedding_model_name
    PERSIST_DIR = args.persist_dir
    
    # Use command-line arguments or defaults for optional parameters
    CHUNK_SIZE = args.chunk_size
    CHUNK_OVERLAP = args.chunk_overlap
    BATCH_SIZE = args.batch_size
    MEMORY_THRESHOLD_MB = args.memory_threshold_mb
    MAX_RETRIES = args.max_retries
    
    logger.info(f"Processing documents from: {BASE_DIR}")
    logger.info(f"Using collection name: {COLLECTION_NAME}")
    logger.info(f"Using embedding model: {EMBEDDING_MODEL_NAME}")
    logger.info(f"Persisting database to: {PERSIST_DIR}")
    logger.info(f"Chunk size: {CHUNK_SIZE}, Chunk overlap: {CHUNK_OVERLAP}")
    logger.info(f"Batch size: {BATCH_SIZE}, Memory threshold: {MEMORY_THRESHOLD_MB} MB")
    logger.info(f"Max retries: {MAX_RETRIES}")
    
    try:
        # Part 1: Chunk Your Data
        logger.info("Step 1: Loading and chunking files...")
        documents = load_files(BASE_DIR, FILE_EXTENSIONS)
        all_chunks = []
        
        for doc_path, doc_text in tqdm(documents, desc="Chunking documents"):
            doc_chunks = chunk_text(doc_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
            for chunk in doc_chunks:
                all_chunks.append({"text": chunk, "source": doc_path})

        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

        # Part 2: Generate Embeddings
        logger.info("\nStep 2: Generating embeddings...")
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        texts = [c["text"] for c in all_chunks]
        
        embeddings = generate_embeddings(texts, embedding_model, MAX_RETRIES)
        logger.info(f"Generated embeddings with shape: {embeddings.shape}")

        # Part 3: Store in Vector Database
        logger.info("\nStep 3: Setting up ChromaDB...")
        
        if os.path.exists(PERSIST_DIR):
            logger.info(f"Old database directory exists: {PERSIST_DIR}")
            # shutil.rmtree(PERSIST_DIR)
        
        # Create persist directory if it doesn't exist (but don't delete if it does)
        os.makedirs(PERSIST_DIR, exist_ok=True)

        settings = Settings(
            persist_directory=PERSIST_DIR
        )

        client = chromadb.PersistentClient(path=PERSIST_DIR)

        # Delete collection if it exists, then create new one
        try:
            client.delete_collection(COLLECTION_NAME)
            logger.info(f"Deleted existing collection: {COLLECTION_NAME}")
        except ValueError:
            # Collection doesn't exist, which is fine
            pass

        collection = client.create_collection(COLLECTION_NAME)

        # Prepare data for storage
        all_texts = [c["text"] for c in all_chunks]
        all_embeddings = embeddings.tolist()
        all_metadatas = [{"source": c["source"]} for c in all_chunks]
        all_ids = [str(i) for i in range(len(all_chunks))]

        # Store in batches with memory monitoring
        num_docs = len(all_chunks)
        current_batch_size = BATCH_SIZE
        
        for i in tqdm(range(0, num_docs, current_batch_size), desc="Storing in ChromaDB"):
            if check_memory_usage(MEMORY_THRESHOLD_MB):
                current_batch_size = max(100, current_batch_size // 2)
                logger.info(f"Reduced batch size to {current_batch_size}")
            
            end = min(i + current_batch_size, num_docs)
            batch_texts = all_texts[i:end]
            batch_embeddings = all_embeddings[i:end]
            batch_metadatas = all_metadatas[i:end]
            batch_ids = all_ids[i:end]

            collection.add(
                documents=batch_texts,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            
            save_checkpoint(end)

        # Persist the database
        # client.persist()
        logger.info("ChromaDB setup and data persistence completed successfully.")
        logger.info(f"Vector database is ready at: {PERSIST_DIR}")
        
        # Clean up checkpoint file
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise