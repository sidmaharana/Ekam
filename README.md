# Ekam: AI-Powered Conversational Data Analyst

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Ekam** (Sanskrit: एकम्) means "one" or "unity". This project unifies structured databases and unstructured documents, allowing you to query them as one, and now, converse with them.

Ekam is an advanced, AI-driven query engine that transforms raw data into actionable insights through natural language. It dynamically adapts to your database schema, processes unstructured documents, and provides a rich, interactive web interface. Beyond simple Q&A, Ekam now offers conversational follow-up suggestions and dynamic data visualizations, making data analysis intuitive and efficient.

---

## 🚀 Live Demo

[**Watch a 5-minute walkthrough of Ekam in action!**](https://www.loom.com/share/xxxxxxxx)

*(This is a placeholder. You should record a Loom video demonstrating the project as per the assignment requirements and replace this link.)*

---

## ✨ Key Features

### 🧠 Core Engine & AI Capabilities

-   **Dynamic Schema Discovery:** Automatically analyzes and understands your SQL database schema (tables, columns, relationships) without any hard-coding, adapting to diverse structures.
-   **Natural Language to SQL (LLM-Powered):** Leverages cutting-edge LLMs (Google Gemini) to translate complex English questions into precise, executable SQL queries.
-   **Hybrid Search:** Intelligently classifies queries to fetch data from structured SQL databases, unstructured documents, or a combination of both.
-   **Scalable Vector Search (ChromaDB):** Processes and indexes documents (PDF, DOCX, TXT, CSV) using sentence-transformer embeddings, storing them in a dedicated ChromaDB vector store for lightning-fast, semantically relevant retrieval. This replaces inefficient in-memory search.
-   **AI-Powered Follow-up Suggestions:** After every query, the Gemini model generates 3 contextually relevant follow-up questions, guiding users through deeper data exploration and analysis.
-   **Intelligent Caching:** In-memory caching for frequently asked questions to provide near-instantaneous results and optimize performance.

### 🖥️ User Interface & Experience

-   **Interactive Database Connector:** Connect to your database and instantly visualize the discovered schema.
-   **Drag-and-Drop Document Uploader:** Easily upload multiple documents with real-time progress indicators, indexing them into ChromaDB.
-   **Unified Query Panel:** A single input for natural language queries, now enhanced with auto-suggestions and query history (planned).
-   **Dynamic Results View:**
    -   **SQL results** are displayed in sortable, paginated tables.
    -   **Document results** are shown as cards with highlighted matches.
    -   **Hybrid results** are presented in a combined, easy-to-understand view.
    -   **Dynamic Chart Visualization:** For suitable SQL aggregation results (e.g., counts by category), the system automatically renders interactive bar charts, providing immediate visual insights.
-   **Conversational Flow:** Clickable follow-up suggestion buttons allow users to seamlessly explore related questions, transforming the UI into an analytical conversation.
-   **Performance Dashboard:** Real-time metrics on query response time, cache hit rate, and the number of indexed documents.
-   **Export Functionality:** Download query results as CSV or JSON.

---

## 🌟 Why Ekam Stands Out

Ekam is more than just a natural language query engine; it's a **conversational data analyst**. Its uniqueness lies in: 

-   **True Conversational AI:** The AI-powered follow-up suggestions elevate the user experience from a rigid Q&A to an interactive, guided analytical journey. This is a significant differentiator from typical NLP interfaces.
-   **Instant Visual Insights:** Automatically generating charts for suitable data transforms raw numbers into immediate, digestible visualizations, making data interpretation faster and more intuitive.
-   **Scalability & Performance:** The integration of ChromaDB for vector search ensures that document processing and retrieval remain fast and efficient, even with large volumes of unstructured data, a critical aspect for production-ready systems.
-   **Dynamic Adaptability:** No hard-coding of schema or data types means Ekam can be dropped into virtually any employee database structure and immediately provide value.
-   **Unified Data Access:** Seamlessly querying both structured and unstructured data sources through a single natural language interface simplifies complex data environments.

---

## 🏛️ Architecture

```
+-----------------+      +----------------------+      +--------------------+
|   React         |      |     FastAPI          |      |   PostgreSQL /     |
|   Frontend      |----->|     Backend          |----->|   MySQL            |
| (Vercel/Netlify)|      | (Docker Container)   |      | (SQL Database)     |
+-----------------+      +----------------------+      +--------------------+
       ^                      |
       |                      |
       |                      v
       |      +----------------------+      +--------------------+
       +------|   NLP / ML Models    |      |   ChromaDB         |
              | (SentenceTransformer,|      | (Vector Database)  |
              |   Google Gemini)     |      |                    |
              +----------------------+      +--------------------+
```

---

## 🛠️ Technology Stack

-   **Backend:**
    -   **Framework:** FastAPI
    -   **Database:** SQLAlchemy ORM, PostgreSQL, MySQL, SQLite
    -   **NLP/LLM:** Google Gemini (for Text-to-SQL & Suggestions), Sentence-Transformers (for Embeddings)
    -   **Vector Store:** ChromaDB (for scalable document search)
    -   **Configuration:** Pydantic-Settings (for `.env` management)
    -   **Async:** Uvicorn
-   **Frontend:**
    -   **Framework:** React.js
    -   **UI Components:** React-Table (for data grids), React-Chartjs-2 (for dynamic charts)
    -   **Styling:** CSS Modules
    -   **Data Fetching:** Fetch API
-   **Deployment:** Docker, Docker Compose (recommended)

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   Node.js v16+
-   Git
-   A Google AI API Key (from [Google AI Studio](https://aistudio.google.com/app/apikey))
-   A running PostgreSQL, MySQL, or SQLite database (SQLite is used by default for local development).

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ekam.git
cd ekam
```

### 2. Backend Setup

There are two ways to set up the backend. The **Recommended** method uses a virtual environment to keep project dependencies isolated, which is standard practice in Python development.

<details>
<summary><strong>✅ Recommended Setup (with Virtual Environment)</strong></summary>

```bash
# 1. From the project's ROOT directory, navigate to the backend folder
cd backend

# 2. Create and activate a virtual environment
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Go back to the project root
cd ..

# 5. Set up environment variables
# Create a file named .env in the project's ROOT directory.
# Add your database URL and Google API Key:
# DATABASE_URL=sqlite:///./test.db
# GOOGLE_API_KEY=YOUR_API_KEY_HERE

# 6. Run the backend server from the ROOT directory
# (You should see (venv) in your terminal if using venv)
uvicorn backend.main:app --reload
```

</details>

<details>
<summary><strong>Alternate Setup (without Virtual Environment)</strong></summary>

This method will install all packages globally on your system.

```bash
# 1. Make sure you are in the project's ROOT directory.

# 2. Install the required packages globally
pip install -r backend/requirements.txt

# 3. Set up environment variables
# Create a file named .env in the project's ROOT directory.
# Add your database URL and Google API Key:
# DATABASE_URL=sqlite:///./test.db
# GOOGLE_API_KEY=YOUR_API_KEY_HERE

# 4. Run the server from the ROOT directory using the python module flag
py -m uvicorn backend.main:app --reload
```

</details>

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the frontend application
npm start
```

### 4. Prepare Test Data

To test the SQL features, you need to load the `test.csv` data into your database. From the project root:

```bash
python backend/ingest_csv.py
```

### 5. Docker Setup (Recommended)

For a more production-like environment, you can use Docker Compose.

```bash
# Make sure you have a .env file in the project root as described above.
# Then, from the root of the project:
docker-compose up --build
```

---

## 📖 Usage

1.  **Connect to Data:**
    -   Navigate to the "Database Connector" panel.
    -   Enter your database connection string and click "Connect". The discovered schema will be visualized.
    -   Go to the "Document Uploader" panel and drag-and-drop your PDF, DOCX, or other documents. You'll see a real-time progress bar for the ingestion process into ChromaDB.
2.  **Query Your Data:**
    -   Go to the "Query Panel".
    -   Type a question in plain English, like `"Show me all Python developers in Engineering"` or `"What is the average salary by department?"`.
    -   Press "Submit Query".
3.  **View Results:**
    -   The results will appear in the "Results View".
    -   **SQL results** are displayed in sortable, paginated tables.
    -   **Document results** are shown as cards with highlighted matches.
    -   **Hybrid results** are presented in a combined view.
    -   **Dynamic Charts** will automatically appear for suitable aggregation queries.
    -   **Follow-up Suggestions** will appear as clickable buttons below the results. Click one to populate the query box with a new question!
    -   Check the "Metrics Dashboard" to see the query performance and cache status.
    -   Click "Export to CSV" to download your results.

---

## 🧪 Testing

To run the backend tests:

```bash
cd backend
pytest
```

---

## 🔮 Future Improvements

-   [ ] **Advanced Schema Insights:** Automatically infer and suggest relationships between tables that don't have explicit foreign keys.
-   [ ] **Support for More Data Sources:** Add connectors for NoSQL databases like MongoDB.
-   [ ] **User Authentication:** Implement user accounts and role-based access control.
-   [ ] **Real-time Ingestion:** Use WebSockets to provide real-time feedback on document processing without polling.
-   [ ] **Query History & Auto-suggestions:** Implement a persistent query history and intelligent auto-suggestions in the query panel.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.