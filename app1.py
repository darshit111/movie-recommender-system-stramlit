import streamlit as st
import pickle
import pandas as pd
import requests
import io
import gdown

# Load movie dictionary
movies_dict = pickle.load(open('movie_dictionary.pkl', 'rb'))
movie_s = pd.DataFrame(movies_dict)

# Load similarity.pkl from Google Drive using gdown
@st.cache_resource
def load_similarity():
    file_id = "1uLIXz0aE-uFJAT_RngngIVlcVuzxiA-3"  # ✅ your correct file ID
    url = f"https://drive.google.com/uc?id={file_id}"

    try:
        output = 'similarity.pkl'
        gdown.download(url, output, quiet=False)
        with open(output, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading pickle file: {e}")
        return None

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1c0f2de87af947d3ca22514029f87b7&language=en-US'
        )
        data = response.json()
        return 'https://image.tmdb.org/t/p/w500' + data['poster_path']
    except:
        return "https://via.placeholder.com/200x300?text=No+Image"

# Recommend movies
def recommend(movie_title, similarity):
    if movie_title not in movie_s['title'].values:
        st.error(f"Movie '{movie_title}' not found.")
        return [], []

    movie_index = movie_s[movie_s['title'] == movie_title].index[0]

    if movie_index >= len(similarity):
        st.error("Invalid index found in similarity matrix.")
        return [], []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movie_s.iloc[i[0]].movie_id
        recommended_movies.append(movie_s.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# UI Starts Here
st.title('🎬 Movie Recommender System by Darshit Rudani')

similarity = load_similarity()

if similarity is not None:
    selected_movie_name = st.selectbox(
        '🎥 Choose a movie to get recommendations:',
        movie_s['title'].values
    )

    if st.button('🔍 Recommend'):
        names, posters = recommend(selected_movie_name, similarity)

        if names and posters:
            col1, col2, col3, col4, col5 = st.columns(5)
            cols = [col1, col2, col3, col4, col5]

            for i in range(5):
                with cols[i]:
                    st.text(names[i])
                    st.image(posters[i])
else:
    st.warning("⏳ Loading similarity matrix. Please wait or refresh...")
