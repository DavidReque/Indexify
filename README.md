# Indexify

A powerful semantic search engine that combines traditional text search with vector similarity using Elasticsearch and machine learning embeddings.

[Indexify Video](https://github.com/user-attachments/assets/4e4668a6-6904-4ed0-8cc6-4b9a380e94eb)

## Overview

Indexify is a comprehensive search solution that leverages Google Custom Search API, Elasticsearch, and transformer-based embeddings to provide intelligent search capabilities. It combines traditional keyword search with semantic understanding to deliver more relevant results.

## ✨ Features

- 🔍 **Hybrid Search**: Combining text and vector similarity
- 🤖 **ML-Powered**: Text embeddings using sentence-transformers
- 📊 **Analytics**: Search statistics and trending queries tracking
- 💡 **Smart Suggestions**: Based on user behavior
- 🔄 **Auto-Fetch**: Content from Google Custom Search when needed
- 🎯 **Advanced Search**: Multiple criteria (title, author, date, keywords)

## Built with

- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Elastic Search](https://www.elastic.co/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Custom Search](https://developers.google.com/custom-search?hl=es-419)
- [FastAPI](https://fastapi.tiangolo.com/)

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
├── .next/
├── node_modules/
├── public/
├── src/
│   └── app/
│       ├── globals.css
│       ├── layout.tsx
│       └── page.tsx
├── components/
├── └── SearchBar.tsx
├── config/
│   └── constants.ts
├── hooks/
│   ├── useSearch.ts
│   └── useSuggestions.ts
├── types/
│   └── index.ts
├── .env
├── .gitignore
├── eslint.config.mjs
├── next-env.d.ts
├── next.config.ts
├── package-lock.json
├── package.json
├── postcss.config.mjs
├── README.md
├── tailwind.config.ts
└── tsconfig.json
```

## Technical Details

### Elasticsearch Index Mapping

The system uses a sophisticated index mapping with the following fields:

```sh
"mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "custom_text_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "completion": {
                                "type": "completion",
                                "analyzer": "custom_text_analyzer"
                            }
                        }
                    },
                    "author": {"type": "keyword"},
                    "publication_date": {"type": "date"},
                    "abstract": {"type": "text", "analyzer": "custom_text_analyzer"},
                    "keywords": {
                        "type": "keyword",
                        "fields": {
                            "text": {
                                "type": "text",
                                "analyzer": "custom_text_analyzer"
                            }
                        }
                    },
                    "content": {"type": "text", "analyzer": "custom_text_analyzer"},
                    "vector": {"type": "dense_vector", "dims": vector_dims},
                    "search_count": {"type": "long"}
                }
            }
```

- `title`: Text field with keyword and completion sub-fields
- `author`: Keyword field for exact matching
- `publication_date`: Date field
- `abstract`: Text field with custom analyzer
- `keywords`: Keyword field with text sub-field
- `content`: Text field with custom analyzer
- `vector`: Dense vector field for semantic search
- `search_count`: Long field for tracking popularity

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

Core Endpoints

```sh
POST /api/search
POST /api/advanced-search
GET /api/suggestions
```

## Interested in Contributing?

If you're interested, please see [Backend](https://github.com/DavidReque/Indexify/blob/main/backend/README.md) and [Frontend](https://github.com/DavidReque/Indexify/blob/main/frontend/indexify/README.md) Guidelines.

## License

This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.
