# AI Dating Profile Search

A prototype AI learning project that explores semantic search of the [59k Dating Profiles dataset](https://huggingface.co/datasets/SpiceeChat/OkCupid-59k-Anonymized-Profiles) using vector embeddings.

The goal is to build a simple search engine for dating profiles that combines traditional filters with natural language queries to find relevant matches.

## Overview

This project uses **Hugging Face** to generate vector embeddings for dating profiles and **Qdrant** as the vector database for storing and searching those embeddings.

Users can search profiles using a combination of:

- **Hard filters:** Structured criteria such as age, location, interests, and preferences.
- **Natural language search:** Queries describing the kind of person someone is looking for, expressed in plain English.
- **Semantic ranking:** Profiles are ranked by how closely their information and preferences match the meaning of the query.

The objective is to build an end-to-end semantic search application, from embedding generation to a searchable web interface.

## How It Works

The application follows a simple data-processing and search pipeline.

```text
┌────────────────────────┐
│  Dating Profile Data   │
│  ~59,000 Profiles      │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   Data Processing      │
│ Normalize & Structure  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Hugging Face Model    │
│ Generate Embeddings    │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   Qdrant Database      │
│ Vectors + Metadata     │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│      Search API        │
│ Filters + Similarity   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│       Web UI           │
│ Ranked Profile Results │
└────────────────────────┘