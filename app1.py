import requests
import io

# Load similarity.pkl from Google Drive
@st.cache_resource
def load_similarity():
    file_id = "1uLIXz0aE-uFJAT_RngngIVlcVuzxiA-3"
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    return pickle.load(io.BytesIO(response.content))



import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1c0f2de87af947d3ca22514029f87b7&language=en-US'
    )
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


def recommend(movies, similarity):
    # Debug: check if the selected movie exists
    st.write(f"Selected movie: {movies}")

    if movies not in movie_s['title'].values:
        st.error(f"Movie '{movies}' not found in dataset.")
        return [], []

    movie_index = movie_s[movie_s['title'] == movies].index[0]

    if movie_index >= len(similarity):
        st.error(f"Invalid movie index: {movie_index}")
        return [], []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movie_s.iloc[i[0]].movie_id
        recommended_movies.append(movie_s.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load movie dictionary
movies_dict = pickle.load(open('movie_dictionary.pkl', 'rb'))
movie_s = pd.DataFrame(movies_dict)

st.title('🎬 Movie Recommender System by Darshit Rudani')

# File uploader for large model file
similarity = load_similarity()

    selected_movie_name = st.selectbox(
        '🎥 Choose a movie to get recommendations:',
        movie_s['title'].values
    )

    if st.button('🔍 Recommend'):
        names, posters = recommend(selected_movie_name, similarity)

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
else:
    st.warning("⚠ Please upload the 'similarity.pkl' file to use the recommendation system.")
