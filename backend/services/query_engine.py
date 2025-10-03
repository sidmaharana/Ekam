import re
from cachetools import TTLCache
from sqlalchemy import text
import numpy as np
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai

from backend.config import settings
from backend.models.database import SessionLocal, Document
from backend.services.schema_discovery import SchemaDiscovery

import chromadb

# Configure the generative AI model with the key from settings
genai.configure(api_key=settings.GOOGLE_API_KEY)

class QueryEngine:
    def __init__(self, connection_string: str):
        self.schema_discovery = SchemaDiscovery()
        self.schema = self.schema_discovery.analyze_database(connection_string)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache = TTLCache(maxsize=100, ttl=300)
        self.gen_model = genai.GenerativeModel('models/gemini-pro-latest')
        
        # Initialize ChromaDB client and get the collection
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_collection(name="documents")

    def process_query(self, user_query: str) -> dict:
        if user_query in self.cache:
            return {"result": self.cache[user_query], "cache_hit": True}

        query_type = self.classify_query(user_query)
        
        if query_type == 'sql':
            result = self.generate_and_run_sql(user_query)
        else:
            result = self.search_documents(user_query)
        
        self.cache[user_query] = result

        # Generate follow-up suggestions
        try:
            suggestions = self._get_followup_suggestions(user_query, result)
        except Exception:
            suggestions = [] # Don't fail the whole query if suggestions fail

        return {"result": result, "cache_hit": False, "query_type": query_type, "suggestions": suggestions}

    def _get_followup_suggestions(self, user_query: str, result: dict) -> list:
        """Generates follow-up questions based on the original query and its result."""
        # We don't need suggestions for errors or empty results
        if result.get("error") or not result.get("results"):
            return []

        # Create a concise summary of the result to include in the prompt
        result_summary = str(result["results"][:2]) # Summary of top 2 results

        prompt = f"""
        Given the original question: "{user_query}"
        And the answer which started with: "{result_summary}"

        Suggest 3 brief, insightful follow-up questions a user might ask next. Return them as a JSON list of strings. For example: ["Question 1?", "Question 2?", "Question 3?"]
        
        Do not include any other text or markdown.
        
        JSON List:
        """

        response = self.gen_model.generate_content(prompt)
        # Clean up the response to get a valid JSON list
        clean_response = response.text.strip().replace('```json', '').replace('```', '')
        
        import json
        try:
            suggestions = json.loads(clean_response)
            return suggestions
        except json.JSONDecodeError:
            return [] # Return empty list if JSON is malformed

    def classify_query(self, user_query: str) -> str:
        """
        Classifies the user query as 'sql' or 'document'.
        A query is considered 'sql' if it contains keywords matching table or column names.
        """
        if not self.schema or self.schema.get("error"):
            return 'document'

        # Clean the query by removing punctuation and making it lowercase
        clean_query = re.sub(r'[^\w\s]', '', user_query.lower())
        query_tokens = set(clean_query.split())

        schema_words = set()
        for table_name, table_info in self.schema.items():
            schema_words.add(table_name.lower())
            for column_info in table_info.get('columns', []):
                col_name = column_info['name'].lower()
                schema_words.add(col_name)
                schema_words.update(col_name.split('_'))

        # Expanded list of keywords
        sql_keywords = {
            'average', 'total', 'sum', 'count', 'max', 'min', 'top', 'bottom', 
            'hired', 'joined', 'many', 'list', 'show', 'who', 'what', 'when', 'where'
        }
        
        if query_tokens.intersection(schema_words) or query_tokens.intersection(sql_keywords):
            return 'sql'

        return 'document'

    def generate_and_run_sql(self, user_query: str) -> dict:
        if self.schema.get("error"):
            return {"error": f"Invalid database schema: {self.schema.get('error')}"}

        prompt = f"""
        Given the following database schema:
        {self.schema}

        Generate a single, executable SQL query to answer the following question. Do not use any markdown or other formatting; just return the raw SQL.
        
        Question: "{user_query}"
        
        SQL Query:
        """

        try:
            # Generate the SQL query
            response = self.gen_model.generate_content(prompt)
            sql_query = response.text.strip().replace('```sql', '').replace('```', '')

            # Execute the query
            db = SessionLocal()
            try:
                result = db.execute(text(sql_query))
                
                # Fetch column names and rows
                columns = result.keys()
                rows = result.fetchall()
                
                # Convert rows to a list of dictionaries
                results_as_dict = [dict(zip(columns, row)) for row in rows]
                
                return {"generated_sql": sql_query, "results": results_as_dict}
            finally:
                db.close()

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    def search_documents(self, user_query: str) -> dict:
        """Searches for relevant documents in the ChromaDB collection."""
        try:
            # Generate embedding for the user query
            query_embedding = self.embedding_model.encode(user_query).tolist()

            # Query the collection to find the 5 most similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5
            )

            # Format the results
            formatted_results = []
            if results and results['documents'][0]:
                for i, doc_text in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "document_name": results['metadatas'][0][i]['source'],
                        "chunk_text": doc_text,
                        "similarity": 1 - results['distances'][0][i] # Chroma returns distance, convert to similarity
                    })
            
            return {"results": formatted_results}
        except Exception as e:
            return {"error": f"An error occurred during document search: {str(e)}"}

    def optimize_sql_query(self, sql: str) -> str:
        # Placeholder for SQL optimization logic
        return sql
