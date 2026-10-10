# AI Movie Recommendation Agent - Development Journey

## Project Vision

The goal of this project is **not just to recommend movies**.

The final objective is to build an **AI Movie Recommendation Agent** capable of:

* Understanding user preferences
* Generating personalized movie recommendations
* Explaining recommendations
* Using LangChain and LangGraph agents
* Maintaining user memory
* Serving recommendations through an API and UI

Current Phase:
Recommendation Engine Development

---

# Project Flow

```
User
   │
Liked Movies
   │
Semantic Recommender
   │
Collaborative Filtering
   │
Hybrid Recommendation
   │
Personalized Recommendation
   │
Genre Re-ranking
   │
Final Recommendation
```

---

# File-by-File Documentation

---

## semantic_recommender.py

### Purpose

Recommend movies based on movie content.

### Dataset Used

latest_movies_final.csv

### Method

* Load similarity_matrix.pkl
* Search movie title
* Find cosine similarity
* Return Top-N similar movies

### Returns

```python
{
    "title": "...",
    "rating": ...,
    "year": ...,
    "similarity_score": ...
}
```

### Why Built

Content-based recommendation.

Useful when users like movies with similar stories or themes.

### Current Limitation

Only uses movie overview embeddings.

### Future Improvement

Replace TF-IDF with Sentence Transformers.

---

## collaborative_filter_v2.py

### Purpose

Recommend movies liked by users with similar tastes.

### Dataset Used

MovieLens ratings dataset

### Method

* Build user-movie matrix
* Compute cosine similarity
* Find similar users
* Recommend movies

### Returns

```python
{
    "title": "...",
    "cf_score": ...
}
```

### Flow

Read ratings.csv
        ↓
Merge
        ↓
Pivot Table
        ↓
9719 × 610 Matrix
        ↓
Cosine Similarity for ALL movies
        ↓
9719 × 9719 Matrix = 94 Million similarity values
        ↓
Pandas DataFrame

### Why Built

Learns from community behaviour instead of movie content.

### Current Limitation

Only MovieLens movies.

### Future Improvement

Support larger datasets.

---
## collaborative_filter_v3.py

### Purpose

load movie_user_matrix.pkl and justt compute only one movie like 1 x 9719

Import

↓

Load Model

↓

Inference
---

## hybrid_recommender.py

### Purpose

Combine Semantic and Collaborative recommendations.

### Method

* Get Semantic recommendations
* Get CF recommendations
* Merge duplicate movies
* Preserve both scores

### Output

```python
{
    "title": "...",
    "semantic_score": ...,
    "cf_score": ...,
    "source": [...]
}
```

### Why Built

Hybrid recommendations are more robust than using only one algorithm.

### Current Limitation

No ranking strategy yet.

### Future Improvement

Weighted hybrid ranking.

---

## user_profile.py

### Purpose

Maintain user information.

### Stores

* Username
* Liked Movies
* Genre Profile

### Why Built

Acts as the memory for each user.

### Future Improvement

Move storage from JSON to PostgreSQL.

---

## genre_service.py

### Purpose

Fetch movie genres using TMDB API.

### Why Built

MovieLens genres are incomplete.

TMDB supports almost every movie.

### Returns

```python
[
    "Science Fiction",
    "Adventure"
]
```

### Current Limitation

Every request calls TMDB.

### Future Improvement

Implement local caching.

---

## genre_profile.py

### Purpose

Build user's favourite genres.

### Example

Liked Movies

* Interstellar
* Arrival
* Predator

Produces

```python
{
    "Science Fiction":3,
    "Adventure":2,
    "Drama":2,
    "Action":1
}
```

### Why Built

Represents long-term user interests.

### Future Improvement

Decay old preferences over time.

---

## personalized_recommenderv2.py

### Purpose

Recommend movies using multiple liked movies.

### Process

For every liked movie

↓

Semantic Recommendation

↓

Collaborative Recommendation

↓

Merge Results

↓

Frequency Count

↓

Top Recommendations

### Why Built

Single liked movie is not enough.

Multiple liked movies capture broader user interests.

### Output

```python
{
    "title": "...",
    "rating": ...,
    "year": ...,
    "semantic_score": ...,
    "cf_score": ...,
    "recommendation_score": ...
}
```

### Future Improvement

Add popularity and user feedback.

---

## reranker.py

### Purpose

Re-rank personalized recommendations.

### Process

Take Personalized V2 Output

↓

Fetch Genres

↓

Compare with User Genre Profile

↓

Calculate Genre Match

↓

Re-order Recommendations

### Why Built

Two users can receive the same recommendations.

Genre re-ranking personalizes the final order.

### Current Limitation

Simple genre matching.

### Future Improvement

Weighted genre similarity.

---

# Current System

```
User

↓

Liked Movies

↓

Semantic

↓

Collaborative

↓

Hybrid

↓

Personalized

↓

Genre Re-ranking

↓

Final Recommendation
```

---

# Future Roadmap

## Phase 2

* LangChain Tools
* Tool Calling

## Phase 3

* LangGraph Agent

## Phase 4

* Conversation Memory

## Phase 5

* FastAPI

## Phase 6

* Streamlit

## Phase 7

* PostgreSQL

## Phase 8

* Redis Cache

## Phase 9

* Recommendation Explanation

## Phase 10

* Deployment

---

# Lessons Learned

* Semantic recommendations capture movie similarity.
* Collaborative filtering captures community behaviour.
* Hybrid recommendations improve robustness.
* Personalization uses multiple liked movies.
* Genre re-ranking adjusts recommendation order based on user taste.
* Build a working system first, then optimize each component.

---

# Guiding Principle

> Make it work.
>
> Make it right.
>
> Make it fast.
