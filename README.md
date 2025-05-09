# Assessment Recommendation System

This project implements a RAG (Retrieval-Augmented Generation) powered multi-agent Q&A assistant that recommends SHL assessments based on user queries or job descriptions. The system intelligently retrieves relevant assessment information from SHL's product catalog and provides personalized recommendations.

## 📋 Project Overview

Rolewise addresses the challenge faced by hiring managers in finding appropriate assessments for roles they're hiring for. Instead of relying on keyword searches and filters, this intelligent system uses natural language processing to understand queries and match them with relevant assessments from SHL's product catalog.

### 🎯 Key Features

- **Natural Language Query Processing**: Accepts both plain text queries and job descriptions
- **Intelligent Assessment Matching**: Uses RAG and LLM to find the most relevant assessments
- **Agentic Workflow**: Routes queries to different tools based on intent
- **Clean Web Interface**: Simple, user-friendly Streamlit frontend
- **API Access**: RESTful API for programmatic access

## 🏗️ Architecture

The project follows a clean, modular architecture:

```
├── .devcontainer/       # Development container configuration
├── backend/            
│   ├── agentic_model.py  # Handles query routing based on intent
│   ├── api.py           # FastAPI implementation of REST API
│   ├── llm_utils.py     # Integration with LLM services
│   ├── make_embeddings.py # Generates vector embeddings from scraped data
│   ├── rag_agent.py     # Core RAG implementation for retrieval
│   ├── schemas.py       # Data models
│   ├── scrape_as_json.py # Data acquisition from SHL website
│   └── requirements.txt # Backend dependencies
├── frontend/
│   └── app.py           # Streamlit web interface
├── context/             # Where scraped data and vector DB are stored
├── README.md            # This documentation
└── requirements.txt     # Project-level dependencies
```

## 💡 How It Works

The system implements the four key components :

### 1. Data Ingestion

- **Web Scraping**: `scrape_as_json.py` extracts assessment data from SHL's product catalog
- **Data Processing**: Assessment information is structured and saved in JSONL format with:
  - Assessment name and URL
  - Remote testing support
  - Adaptive/IRT support
  - Duration and test type
  - Additional metadata like descriptions and job levels

### 2. Vector Store & Retrieval

- **Vector Indexing**: `make_embeddings.py` processes the scraped data and creates embeddings
- **ChromaDB Integration**: Embeddings are stored in a persistent ChromaDB collection
- **Semantic Search**: When a query is received, the system retrieves the top 3 most semantically relevant assessment chunks

### 3. LLM Integration

- **Azure AI Integration**: The system uses Azure's AI inference client to access advanced LLMs
- **Context-Aware Responses**: The LLM is given both the user query and retrieved assessment context
- **Concise Answers**: Responses are optimized to be brief but informative, focusing on relevance to the user's query

### 4. Agentic Workflow

- **Intent Recognition**: The system identifies query intent (e.g., general questions about SHL vs. assessment queries)
- **Route Selection**: Based on intent, queries are routed to appropriate handlers:
  - General SHL information queries → Direct response
  - Assessment queries → RAG pipeline
  - Other queries → Fallback response
- **Decision Logging**: Each routing decision and processing step is tracked

### 5. Demo Interface

- **Streamlit UI**: Clean, simple interface for entering queries and viewing results
- **Results Display**:
  - Shows which processing route was taken
  - Displays the retrieved assessment information
  - Presents the final LLM-generated answer
- **API Endpoint**: For programmatic access via HTTP requests

## 🔗 Access

The application is available online at the following URL:

[RoleWise](https://rolewise.streamlit.app/)

You can directly query the system through this interface without any setup required.

### API Usage

The system exposes a simple REST API:

- **Health Check**: `POST /health`
- **Query Endpoint**: `POST /query`
  ```json
  {
    "query": "I need assessment for Java developers who can collaborate effectively with my business teams."
  }
  ```



## 🛠️ Implementation Details

### Technologies Used

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Vector Database**: ChromaDB
- **LLM Integration**: Azure AI Inference
- **Web Scraping**: BeautifulSoup, Requests
- **Data Processing**: JSON, Python standard library

### Key Design Choices

1. **RAG over Fine-tuning**: Using RAG allows the system to work with up-to-date assessment information without retraining models
2. **ChromaDB**: Selected for its ease of use, performance, and persistence capabilities
3. **Agentic Routing**: Improves efficiency by handling different query types with specialized processors
4. **Streamlit**: Enables rapid development of a clean, functional UI
5. **FastAPI**: Provides high-performance API endpoints
   
## 🔄 Future Improvements

- **Enhanced Evaluation Framework**: Implement robust evaluation metrics such as Mean Recall@K and Mean Average Precision@K (MAP@K) to quantitatively assess recommendation quality
- **Improved Intent Recognition**: Enhance the agentic model to better understand and process the intent behind user queries
- **Advanced Routing Capabilities**: Expand the agentic workflow with more specialized tools for different query types
- **Expanded Knowledge Base**: Increase the scope of assessment information and metadata
- **Query History**: Allow users to view and refer back to previous queries and recommendations
- **Custom Filtering Options**: Enable users to refine recommendations based on specific criteria like assessment duration or test type
