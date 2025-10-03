from sentence_transformers import SentenceTransformer
import chromadb
import uuid
import pypdf
import docx
import csv
import io

class DocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        # Initialize ChromaDB client. It can be in-memory or persistent.
        # Using a persistent client is better for production.
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="documents")

    def process_documents(self, files: list, filenames: list):
        """
        Process and store documents in ChromaDB.
        """
        for file, filename in zip(files, filenames):
            file_extension = filename.split('.')[-1].lower()
            content = self.read_file(file, file_extension)
            chunks = self.dynamic_chunking(content, file_extension)
            
            if not chunks:
                continue

            embeddings = self.embedding_model.encode(chunks, batch_size=32).tolist()
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadata = [{'source': filename} for _ in chunks]

            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadata,
                ids=ids
            )
        print(f"Successfully processed and indexed {len(filenames)} documents into ChromaDB.")

    def read_file(self, file, file_extension):
        content = ""
        try:
            if file_extension == 'pdf':
                pdf_reader = pypdf.PdfReader(io.BytesIO(file))
                for page in pdf_reader.pages:
                    content += page.extract_text() or ''
            elif file_extension == 'docx':
                doc = docx.Document(io.BytesIO(file))
                for para in doc.paragraphs:
                    content += para.text + '\n'
            elif file_extension == 'txt':
                content = file.decode('utf-8')
            elif file_extension == 'csv':
                content = file.decode('utf-8')
        except Exception as e:
            print(f"Error reading file: {e}")
        return content

    def dynamic_chunking(self, content: str, doc_type: str) -> list:
        """
        Intelligent chunking based on document structure.
        """
        if doc_type == 'csv':
            # For CSVs, treat each row as a document
            lines = content.splitlines()
            reader = csv.reader(lines)
            # Skip header if it exists
            try:
                header = next(reader)
                return [", ".join(row) for row in reader if row]
            except StopIteration:
                return []
        else:
            # Simple paragraph-based chunking, ignoring very short paragraphs
            return [para.strip() for para in content.split('\n\n') if len(para.strip()) > 50]