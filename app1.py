import streamlit as st
import pickle
import pandas as pd
import requests
import io
import gdown

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Loading spinner for startup
with st.spinner('Loading application...'):
    # Load movie dictionary from Google Drive
    @st.cache_resource
    def load_movie_data():
        file_id = "<1kPBJDR_tJbqIBcKmoHpWC329h1yp6b3z>"
        url = f"https://drive.google.com/uc?id={file_id}"
        output = 'movie_dictionary.pkl'
        gdown.download(url, output, quiet=False)
        with open(output, 'rb') as f:
            return pd.DataFrame(pickle.load(f))

    # Load similarity.pkl from Google Drive
    @st.cache_resource
    def load_similarity():
        file_id = "1uLIXz0aE-uFJAT_RngngIVlcVuzxiA-3"
        url = f"https://drive.google.com/uc?id={file_id}"
        output = 'similarity.pkl'
        gdown.download(url, output, quiet=False)
        with open(output, 'rb') as f:
            return pickle.load(f)

    movie_s = load_movie_data()
    similarity = load_similarity()

# --- Authentication (basic demo only) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("🔐 Login to Continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username == "admin" and password == "admin":  # Demo only
                st.success("✅ Logged in successfully!")
                st.session_state.logged_in = True
            else:
                st.error("❌ Invalid credentials")
    st.stop()

# --- Main UI ---
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System by Darshit Rudani</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    '🎥 Choose a movie to get recommendations:',
    movie_s['title'].values
)

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c1c0f2de87af947d3ca22514029f87b7&language=en-US'
        )
        data = response.json()
        return 'https://image.tmdb.org/t/p/w500' + data['poster_path']
    except:
        return "https://via.placeholder.com/200x300?text=No+Image"

def recommend(movie_title):
    if movie_title not in movie_s['title'].values:
        st.error(f"Movie '{movie_title}' not found.")
        return [], []

    movie_index = movie_s[movie_s['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movie_s.iloc[i[0]].movie_id
        recommended_movies.append(movie_s.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

if st.button('🔍 Recommend'):
    names, posters = recommend(selected_movie_name)
    if names:
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])
