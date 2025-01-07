# Indexify

A powerful semantic search engine that combines traditional text search with vector similarity using Elasticsearch and machine learning embeddings.

## Overview

Indexify is a comprehensive search solution that leverages Google Custom Search API, Elasticsearch, and transformer-based embeddings to provide intelligent search capabilities. It combines traditional keyword search with semantic understanding to deliver more relevant results.

## Features

- 🔍 Hybrid search combining text and vector similarity
- 🤖 Machine learning-powered text embeddings using sentence-transformers
- 📊 Search statistics and trending queries tracking
- 💡 Smart search suggestions based on user behavior
- 🔄 Automatic content fetching from Google Custom Search when needed
- 🎯 Advanced search with multiple criteria (title, author, date, keywords)

## Architecture

### Backend Structure

```sh
backend/
├── app/
│   ├── api/routes/
│   │   └── routes.py
│   ├── core/
│   │   ├── models.py
│   │   ├── elasticsearch.py
│   │   ├── suggestion.py
│   │   ├── custom_search.py
│   │   ├── utils.py
│   │   ├── client.py
│   │   ├── index.py
│   │   └── documents.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

### Frontend Structure

```sh
frontend/indexify/
├── src/app/
├── components/
├── types/
├── config/
├── hooks/
├── .env
├── config.ts
└── README.md
```

## Technical Details

### Elasticsearch Index Mapping

The system uses a sophisticated index mapping with the following fields:

- title: Text field with keyword and completion sub-fields
- author: Keyword field for exact matching
- publication_date: Date field
- abstract: Text field with custom analyzer
- keywords: Keyword field with text sub-field
- content: Text field with custom analyzer
- vector: Dense vector field for semantic search
- search_count: Long field for tracking popularity

## Embedding Process

Indexify uses the sentence-transformers/all-MiniLM-L6-v2 model to generate text embeddings that capture semantic meaning. The process involves:

1. Text preprocessing and tokenization
2. Vector generation using the transformer model
3. Storage in Elasticsearch's dense vector field
4. Similarity calculation during search using cosine similarity

## Search Features

1. Vector Text Search

- Combines traditional text matching with vector similarity
- Uses script scoring for hybrid ranking
- Supports fuzzy matching and field boosting

2. Advanced Search

- Multi-criteria search (title, author, date range, keywords)
- Customizable result size
- Sort by relevance and date

3. Search Suggestions

- Based on previous searches and trending queries
- Tracks and updates search statistics
- Provides real-time completion suggestions

## API Routes

The FastAPI application provides the following endpoints:

GET /: Health check endpoint
Additional routes defined in api/routes/routes.py

## Contributing

- Fork the repository
- Create your feature branch
- Commit your changes
- Push to the branch
- Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
