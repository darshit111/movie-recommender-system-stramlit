import streamlit as st
import pickle
import pandas as pd
import requests

# 🔄 Download helper from Google Drive
def download_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# ✅ Load movie dictionary
@st.cache_resource
def load_movie_data():
    file_id = "1kPBJDR_tJbqIBcKmoHpWC329h1yp6b3z"  # movie_dictionary.pkl
    download_from_google_drive(file_id, "movie_dictionary.pkl")
    with open("movie_dictionary.pkl", "rb") as f:
        return pd.DataFrame(pickle.load(f))

# ✅ Load similarity matrix
@st.cache_resource
def load_similarity():
    file_id = "1uLIXz0aE-uFJAT_RngngIVlcVuzxiA-3"  # similarity.pkl
    download_from_google_drive(file_id, "similarity.pkl")
    with open("similarity.pkl", "rb") as f:
        return pickle.load(f)

# ✅ Fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1c0f2de87af947d3ca22514029f87b7&language=en-US"
    )
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

# ✅ Recommendation logic
def recommend(movie, similarity):
    movie_index = movie_s[movie_s['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movie_s.iloc[i[0]].movie_id
        recommended_movies.append(movie_s.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# 🎬 UI
st.title("🎬 Movie Recommender System by Darshit Rudani")

with st.spinner('🔁 Please wait while the data loads...'):
    movie_s = load_movie_data()
    similarity = load_similarity()

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movie_s['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, similarity)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
