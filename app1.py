import streamlit as st
import pickle
import pandas as pd
import requests
import gdown

# ✅ Download similarity.pkl from Google Drive
file_id_sim = "1uLIXz0aE-uFJAT_RngngIVlcVuzxiA-3"
url_sim = f"https://drive.google.com/uc?id={file_id_sim}"
output_sim = "similarity.pkl"
gdown.download(url_sim, output_sim, quiet=False)

# ✅ Load manually uploaded movie_dictionary.pkl (you upload this in Streamlit Cloud manually)
movies_dict = pickle.load(open('movie_dictionary.pkl', 'rb'))
movie_s = pd.DataFrame(movies_dict)

# ✅ Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ✅ Function to fetch movie posters
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1c0f2de87af947d3ca22514029f87b7&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# ✅ Recommender logic
def recommend(movie):
    movie_index = movie_s[movie_s['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movie_s.iloc[i[0]].movie_id
        recommended_movies.append(movie_s.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ✅ Streamlit UI
st.title("🎬 Movie Recommender System by Darshit Rudani")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movie_s['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
