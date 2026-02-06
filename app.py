from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# 🔑 TMDB API KEY (already inserted)
API_KEY = "e4ec32dd6d3b6978d1a2605826a39f88"

# Load trained data
movies = pickle.load(open("movies_data.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# 🔹 SAFE TMDB API CALL (with error handling)
def get_movie_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("results") and data["results"][0].get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["results"][0]["poster_path"]

    except requests.exceptions.RequestException as e:
        print("TMDB API Error:", e)

    return None


@app.route('/')
def home():
    return render_template("index.html", movies=movies['title'].tolist())


@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie = request.form['movie']

    index = movies[movies['title'] == selected_movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []

    for i in distances:
        title = movies.iloc[i[0]].title
        poster = get_movie_poster(title)

        # 🔹 fallback image if API fails
        if poster is None:
            poster = "https://via.placeholder.com/300x450?text=No+Poster"

        recommendations.append({
            "title": title,
            "poster": poster
        })

    return render_template(
        "index.html",
        movies=movies['title'].tolist(),
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)
