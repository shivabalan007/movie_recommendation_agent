# Datasets Used

This project uses two different datasets for building a hybrid movie recommendation system.

---

# Dataset 1: Latest Movies Dataset

## Purpose

Used for the Semantic Recommendation Engine.

The dataset contains movie metadata and plot descriptions, which are converted into embeddings to find movies with similar content and themes.

## Shape

| Metric   | Value |
| -------- | ----- |
| Movies   | 7,397 |
| Features | 7     |

## Columns

| Column              | Description                 |
| ------------------- | --------------------------- |
| title               | Movie title                 |
| overview            | Movie plot summary          |
| release_date        | Movie release date          |
| vote_average        | Average user rating         |
| popularity          | Popularity score            |
| release_year        | Extracted release year      |
|combined_text        | Processed movie information |

## Example

| title        | overview                                                                       |
| ------------ | ------------------------------------------------------------------------------ |
| Interstellar | The adventures of a group of explorers who travel through a wormhole in space. |

## Usage

This dataset is used to:

* Generate sentence embeddings from movie overviews
* Compute semantic similarity between movies
* Recommend movies with similar storylines and themes

## Generated Artifacts

### movie_embeddings.pkl

Stores precomputed embeddings generated using Sentence Transformers.

### similarity_matrix.pkl

Stores cosine similarity scores between all movies.

7397 x 7397

## Recommendation Example

Input:

Interstellar

Output:

* Prometheus
* Stargate
* Lost in Starlight
* Atlantis: The Lost Empire

These movies are recommended because they share similar themes such as space exploration, science fiction, and extraterrestrial concepts.

---

# Dataset 2: MovieLens Latest Small

## Purpose

Used for the Collaborative Filtering Engine.

The dataset contains real user ratings and enables recommendations based on user behavior.

## Shape

| Metric  | Value   |
| ------- | ------- |
| Users   | 610     |
| Movies  | 9,742   |
| Ratings | 100,836 |
| Tags    | 3,683   |

## Files

### ratings.csv

Contains movie ratings given by users.

| Column    |
| --------- |
| userId    |
| movieId   |
| rating    |
| timestamp |

Example:

| userId | movieId | rating |
| ------ | ------- | ------ |
| 1      | 1       | 4.0    |

---

### movies.csv

Contains movie information.

| Column  |
| ------- |
| movieId |
| title   |
| genres  |

Example:

| movieId | title            | genres                     |
| ------- | ---------------- | -------------------------- |
| 1       | Toy Story (1995) | Adventure|Animation|Comedy |

---

### tags.csv

Contains user-generated tags.

| Column    |
| --------- |
| userId    |
| movieId   |
| tag       |
| timestamp |

Example:

| userId | movieId | tag   |
| ------ | ------- | ----- |
| 2      | 60756   | funny |

## Usage

This dataset is used to:

* Build the movie-user rating matrix
* Compute movie similarity using user behavior
* Generate collaborative recommendations

## Recommendation Example

Input:

Interstellar (2014)

Output:

* Inception (2010)
* The Martian (2015)
* Dark Knight Rises (2012)
* Guardians of the Galaxy (2014)

These recommendations are based on users who rated similar movies highly.

---

# Why Two Datasets?

The project combines two recommendation approaches:

## Semantic Recommendation

Uses movie content.

Movie → Overview → Embeddings → Similar Movies

## Collaborative Filtering

Uses user behavior.

Movie → User Ratings → Similar User Preferences → Similar Movies

Combining both approaches helps improve recommendation quality and reduces the weaknesses of using only one recommendation method.

## Hybrid Recommendation

## Semantic

Movie Overview
↓
Embedding Vector (384 dimensions)
↓
Cosine Similarity

## Collaborative

User Ratings
↓
Movie Rating Vector (610 dimensions)
↓
Cosine Similarity

---------------------------------
Semantic:
"What is this movie about?"

+

Collaborative:
"What do people with similar tastes like?"

= 
Hybrid Recommendation
----------------------------------