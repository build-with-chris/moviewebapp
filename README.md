# 🎬 MoviewebApp

Welcome to **MoviewebApp** – a user-friendly web application for managing your favorite movies, powered by Flask and SQLite.  
Each user has their own little movie universe: add, update, or remove movies with just a few clicks – and it even connects to the OMDb API to fetch movie details for you. ✨

---

## 🚀 Features

- 🔐 **User selection** – Choose your user from a list (no login needed)
- 🎞️ **Add movies** – Enter a movie title and let the app do the rest via OMDb API
- 📝 **Update movies** – Change title, director, rating, or year
- ❌ **Delete movies** – Clean out your watchlist
- 👥 **Create or remove users** – Manage who’s watching what
- 🧠 **IMDb integration** – Auto-fetch movie info with a single input
- 💾 **SQLite database** – Fast, lightweight, and integrated into the app

---

## 🛠️ Tech Stack

- **Flask** – Python micro web framework
- **SQLAlchemy** – ORM for managing database models
- **SQLite** – Simple file-based database
- **HTML/CSS** – Frontend templates and styling
- **Jinja2** – Dynamic template rendering
- **OMDb API** – For real movie data

---

## 💡 What makes the database special?

- ✅ **User-friendly structure**: Each movie is linked to a specific user via `user_id`, making the logic simple and intuitive.
- ✅ **Clean separation**: The database is managed through a `DataManager` class that abstracts all operations – no raw SQL needed.
- ✅ **Scalable logic**: The app uses an interface-based approach, meaning you could easily swap SQLite for another backend like PostgreSQL later on.

---

## 🧠 What I learned so far

- How to set up and structure a **Flask app** from scratch
- Creating and linking models with **SQLAlchemy**
- Using **OMDb API** to fetch and handle external data
- Rendering dynamic content with **Jinja2**
- Implementing **RESTful routes** and handling edge cases
- Writing clean, reusable logic using **abstract base classes**
- Using **pytest** and `client` fixtures for automated testing
- Styling and structuring templates for a better user experience

---

## 🧪 How to run locally

1. Clone this repo  
   `git clone https://github.com/build-with-chris/moviewebapp.git`

2. Install dependencies  
   `pip install -r requirements.txt`

3. Add your OMDb API key to a `.env` file:  

4. Run the app  
`flask run`

5. Visit [http://localhost:5000](http://localhost:5000) in your browser 🎉

---

## 🧭 Next steps (for future development)

- Add user login/authentication
- Tag movies with genres or custom labels
- Switch to PostgreSQL for production
- Add search or filter options for large movie lists

---

_Thanks for reading – and happy movie tracking! 🍿_