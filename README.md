# Movie and Series Recommendation System - Neo4j

## Overview

This project implements a **movie and series recommendation system** using **Neo4j**, a graph database. The system models relationships between users, movies, and series to provide personalized recommendations based on preferences, ratings, and similarity scores.

---

## Nodes and Labels

The following **nodes and labels** are defined:

### **User (User)**
Represents each registered user in the system.

**Properties:**
- `user_id` (String) → Unique identifier  
- `name` (String) → User’s name  
- `age` (Integer) → User’s age  
- `favorite_genres` (List) → Genres the user likes the most  
- `preferred_duration` (Integer) → Average preferred duration in minutes  

### **Movie (Movie)**
Represents a movie in the system.

**Properties:**
- `movie_id` (String) → Unique identifier  
- `title` (String) → Movie title  
- `genre` (List) → List of genres  
- `duration` (Integer) → Duration in minutes  
- `release_date` (Date) → Release date  
- `average_rating` (Float) → Average rating received  

### **Series (Series)**
Represents a TV series in the system.

**Properties:**
- `series_id` (String) → Unique identifier  
- `title` (String) → Series title  
- `genre` (List) → List of genres  
- `total_episodes` (Integer) → Total number of episodes  
- `release_date` (Date) → Release date  
- `average_rating` (Float) → Average rating received  

### **Rating (Rating)**
Stores the rating that a user gives to a movie or series.

**Properties:**
- `rating_id` (String) → Unique identifier  
- `user_id` (String) → ID of the user who provided the rating  
- `content_id` (String) → ID of the rated movie or series  
- `score` (Integer) → Rating score from 1 to 5  
- `comment` (String) → Optional user comment  

### **Genre (Genre)**
Represents a genre of movies/series.

**Properties:**
- `genre_id` (String) → Unique identifier  
- `name` (String) → Name of the genre (e.g., Action, Drama, Comedy)  
- `avg` (Float) → How common the genre is  
- `description` (String) → Brief description of the genre  
- `popular` (Boolean) → Indicates whether the genre is considered popular (if more than 50 movies/series belong to this genre, it is marked as popular)  

---

## Defined Relationships

The system defines **ten types of relationships** between nodes:

### **User Preferences**
- `(:User)-[:LIKES]->(:Genre)`
  - `preference_level` (Integer) → Value from 1 to 5 indicating how much the user likes the genre  
  - `date_added` (Date) → Date when the user marked this genre as a favorite  

- `(:User)-[:DISLIKES]->(:Genre)`
  - `dislike_level` (Integer) → Value from 1 to 5 indicating how much the user dislikes the genre  
  - `date_added` (Date) → Date when the user marked this genre as disliked  

### **User Ratings**
- `(:User)-[:RATED]->(:Rating)`
  - `rating_date` (Date) → Date when the rating was given  
  - `comment` (String) → Optional comment provided by the user with the rating  

- `(:Rating)-[:BELONGS_TO]->(:Movie)`
  - `relevance` (Float) → Indicates how relevant this rating is compared to other ratings for the same movie  

- `(:Rating)-[:BELONGS_TO]->(:Series)`
  - `relevance` (Float) → Indicates how relevant this rating is compared to other ratings for the same series  

### **User Watch History**
- `(:User)-[:WATCHED]->(:Movie)`
  - `watched_date` (Date) → Date when the user watched the movie  

- `(:User)-[:WATCHED]->(:Series)`
  - `watched_date` (Date) → Date when the user watched the series  
  - `episodes_watched` (Integer) → Number of episodes watched  

### **Genre Associations**
- `(:Movie)-[:HAS_GENRE]->(:Genre)`
  - `weight` (Float) → Indicates how important this genre is in the movie (value between 0 and 1)  

- `(:Series)-[:HAS_GENRE]->(:Genre)`
  - `weight` (Float) → Indicates how important this genre is in the series (value between 0 and 1)  

### **User Similarity**
- `(:User)-[:SIMILAR_TO]->(:User)`
  - `score` (Float) → Similarity score between users based on their preferences and ratings  
  - `calculation_date` (Date) → Date when the similarity was calculated  

---