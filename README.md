# 🎸 Modal — A Guitar-Focused Music Assistant Powered by RAG

**Modal** is an AI-powered music assistant built around chord progressions, song metadata, and rich vector search. It’s designed specifically for **guitar-focused musical discovery**, theory exploration, and intelligent follow-up suggestions — powered by OpenAI and real song data.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Running Locally](#running-locally)
- [Suggested Queries](#suggested-queries)
- [Limitations](#limitations)
- [Coming Soon](#coming-soon)

---

## Features

- Natural language queries about songs, progressions, solos, and musical structure
- RAG architecture combining OpenAI GPT-4o with a searchable vector database
- Chord-focused enrichment, tailored for guitarists at all levels
- Animated chat interface with chunked message reveal
- Shareable conversation URLs using conversation ID

---

## How It Works

Modal uses a FastAPI backend to:

- Accept user queries and route them through OpenAI's `responses.create` API
- Enrich responses with structured data pulled from:
  - [Ultimate Guitar](https://www.ultimate-guitar.com/) (live chord progression scraping)
  - [Spotify 12M Songs Dataset (Kaggle)](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)
- Upload missing song entries to the OpenAI Native Vector Store API
- Format output with markdown and suggestions for further exploration

The frontend uses Next.js and Tailwind CSS to render a responsive chat interface with animated chunked message reveal using custom `@theme` keyframe animations.

---

## Tech Stack

### Frontend
- Next.js 14 (App Router, Client Components)
- Tailwind CSS v4.1
- ShadCN UI
- Zustand (`useChatStore`)
- `react-markdown`

### Backend
- FastAPI
- OpenAI GPT-4o 
- OpenAI Vector Store API
- Ultimate Guitar + Spotify metadata for chord enrichment

---

## Running Locally

### Frontend
```bash
cd frontend
npm install
npm run dev
