# Chunk Embed Store

A powerful tool for chunking, embedding, and storing documents in a vector database for efficient retrieval and semantic search capabilities.

## 🔍 Overview

Chunk Embed Store is a Python tool designed to process, chunk, and embed text documents into a vector database. It analyzes your code base or documentation, breaks it into manageable chunks, generates semantic embeddings, and stores them in a ChromaDB vector database for later retrieval.

## ✨ Features

- **Intelligent Document Processing**: Supports a wide variety of file types (code files, documentation, text files, etc.)
- **Smart Chunking**: Breaks documents into optimal chunks while preserving context
- **High-Quality Embeddings**: Uses [Sentence Transformers](https://www.sbert.net/) to generate semantic embeddings
- **Efficient Storage**: Stores document chunks and embeddings in [ChromaDB](https://github.com/chroma-core/chroma) for fast retrieval
- **Memory-Aware Processing**: Dynamically adjusts batch size based on available memory
- **Resilient Operation**: Includes retry mechanisms and error handling
- **Progress Tracking**: Shows real-time progress with helpful statistics

## 📋 Prerequisites

- Python 3.10 or higher
- A pre-trained Sentence Transformer model 
- Sufficient disk space for the vector database
- Sufficient RAM for processing (8GB recommended)

## 🔧 Installation

### From PyPI

```bash
pip install chunk-embed
```

### From Source

```bash
git clone https://github.com/yourusername/chunk-embed-store.git
cd chunk-embed-store
pip install -e .
```

## 💻 Usage

### Basic Usage

```bash
chunk-embed \
  --base_dir "/path/to/your/documents" \
  --collection_name "your-collection" \
  --embedding_model_name "/path/to/embedding/model" \
  --persist_dir "/path/to/store/database"
```

### With UVX

You can also run the tool with [UVX](https://github.com/uvx-js/uvx) for an enhanced experience:

```bash
uvx chunk-embed \
  --base_dir "/path/to/your/documents" \
  --collection_name "your-collection" \
  --embedding_model_name "/path/to/embedding/model" \
  --persist_dir "/path/to/store/database"
```

### All Options

| Parameter | Required | Default | Description |
|------------|----------|---------|-------------|
| `--base_dir` | Yes | - | Directory containing documents to process |
| `--collection_name` | Yes | - | Name for the ChromaDB collection |
| `--embedding_model_name` | Yes | - | Path to Sentence Transformer model |
| `--persist_dir` | Yes | - | Directory to store the vector database |
| `--chunk_size` | No | 500 | Size of text chunks |
| `--chunk_overlap` | No | 50 | Overlap between text chunks |
| `--batch_size` | No | 1000 | Batch size for processing |
| `--memory_threshold_mb` | No | 8000 | Memory threshold in MB |
| `--max_retries` | No | 3 | Maximum retries for embedding generation |

## 📊 Example

Process a code repository and store embeddings in a local database:

```bash
chunk-embed \
  --base_dir "/Users/username/projects/my-repo" \
  --collection_name "my-repo-knowledge" \
  --embedding_model_name "/Users/username/models/all-MiniLM-L6-v2" \
  --persist_dir "/Users/username/vector-db/my-repo-db" \
  --chunk_size 600 \
  --chunk_overlap 75
```

## 📁 Supported File Types

The tool processes a wide variety of file types including:

- Code files: `.py`, `.js`, `.java`, `.cpp`, `.go`, etc.
- Documentation: `.md`, `.txt`, `.html`, etc.
- Configuration: `.yml`, `.json`, `.toml`, etc.
- And many more (over 100 file extensions supported)

## 🔄 How It Works

1. **Loading**: The tool recursively explores your specified directory and loads files with supported extensions.
2. **Chunking**: Each document is split into smaller chunks with configurable size and overlap, trying to respect natural boundaries like line breaks.
3. **Embedding**: The chunks are processed through a Sentence Transformer model to generate vector embeddings.
4. **Storage**: The chunks and their embeddings are stored in a ChromaDB vector database for efficient retrieval.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- Aditya Mishra (adi.mishra989@gmail.com)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Advanced Usage

### Customizing Embedding Model

The embedding model significantly impacts the quality of your vector database. By default, the tool works well with Sentence Transformer models. If you want to customize:

1. Download or train your preferred model
2. Specify the path using `--embedding_model_name`

### Memory Optimization

For large document collections, memory usage can be a concern. The tool includes automatic memory management:

- Monitors memory usage during processing
- Dynamically reduces batch size if memory threshold is exceeded
- Override the default threshold with `--memory_threshold_mb`

### Integration with Retrieval Systems

The ChromaDB collections created by this tool can be easily integrated with retrieval augmented generation systems. You can load the collection in your application:

```python
import chromadb

client = chromadb.PersistentClient(path="/path/to/your/database")
collection = client.get_collection(name="your-collection-name")

# Query for similar documents
results = collection.query(
    query_texts=["Your query text here"],
    n_results=5
)
```

## 📌 Development Roadmap

- [ ] Support for more embedding models
- [ ] Parallel processing for faster execution
- [ ] Incremental updates to existing collections
- [ ] Improved chunking strategies for code files
- [ ] Web UI for database exploration