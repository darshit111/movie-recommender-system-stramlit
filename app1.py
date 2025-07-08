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
    movie_index = movie_s[movie_s['title'] == movies].index[0]
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
movies_dict = pickle.load(open('moive_dictionary.pkl', 'rb'))
movie_s = pd.DataFrame(movies_dict)

st.title('🎬 Movie Recommender System by Darshit Rudani')

# File uploader for large model file
uploaded_file = st.file_uploader("📂 Upload 'similarity.pkl' file to continue", type="pkl")

if uploaded_file is not None:
    similarity = pickle.load(uploaded_file)

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
