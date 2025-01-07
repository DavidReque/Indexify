# Backend - Search Engine

This project aims to build an efficient search system. The backend is built using FastAPI.

The backend is responsible for handling the core search functionalities and data processing.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python (>=3.7)
- pip

### Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/yourrepository.git
```

2. Navigate to the backend directory:

```sh
cd yourrepository/backend
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. The backend requires specific environment variables to be configured. Create a .env file in the backend directory and add the following:

```sh
ELASTICSEARCH_CLOUD_ID=your_elasticsearch_cloud_id
ELASTICSEARCH_API_KEY=your_elasticsearch_api_key
INDEX_NAME=your_index_name
SEARCH_ENGINE_ID=your_search_engine_id
GOOGLE_API_KEY=your_google_api_key
FRONTEND_URL=your_frontend_url
FRONTEND_URL_LOCAL=your_frontend_local_url
```

5. Running the Backend Server

```sh
uvicorn main:app --reload --port 8000
```
