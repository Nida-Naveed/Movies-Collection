# 🎬 Movie Collection App (Flask)

A Flask web application that allows users to manage a personal movie collection.  
Users can add, edit, delete, and rate movies while fetching data from an external movie API.

---

## 🌐 Live Demo

👉 https://movies-collection-a1oc.onrender.com/

---

## 🚀 Features

- ➕ Add movies using external movie search (TMDB API)
- ✏️ Edit movie ratings and reviews
- ❌ Delete movies from collection
- 📊 Rank movies based on ratings
- 🎬 Fetch movie details from TMDB API
- 🗄 Persistent storage using SQLite database
- 🎨 Responsive UI using Bootstrap 5

---

## 🧰 Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Bootstrap5
- WTForms
- SQLite
- TMDB API
- HTML / Jinja Templates

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Movie-Collection.git
cd Movie-Collection
```

---

### 2. Create virtual environment (optional)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the app locally

```bash
python main.py
```

Then open:

```
http://127.0.0.1:5000
```

---

## 🔑 API Used

This project uses **The Movie Database (TMDB) API**.

- Search Movies:
```
https://api.themoviedb.org/3/search/movie
```

- Movie Details:
```
https://api.themoviedb.org/3/movie/{movie_id}
```

---

## 🧠 Key Functionalities

### ➕ Add Movie
Search movies from TMDB and add them to your collection.

### ✏️ Edit Movie
Update rating and review of a movie.

### ❌ Delete Movie
Remove a movie from the database.

---

## 🗄 Database Model

```
Movie:
- id
- title
- year
- description
- rating
- ranking
- review
- img_url
```

---

## 🌐 Deployment

Deployed using:

Render → https://render.com/

---


