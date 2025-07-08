import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c1c0f2de87af947d3ca22514029f87b7&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


def recommend(movies):
    movie_index = movie_s[movie_s['title'] == movies].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posterts = []

    for i in movie_list:

        movie_id = movie_s.iloc[i[0]].movie_id
        recommended_movies.append(movie_s.iloc[i[0]].title)
                    #fetch posters from API
        recommended_movies_posterts.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posterts

movies_dict = pickle.load(open('moive_dictionary.pkl', 'rb'))
movie_s = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System by Darshit Rudani')

selected_movie_name = st.selectbox(
'How would you like to be contacted?',
movie_s['title'].values)


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.text(names[0])
    st.image(posters[0])

with col2:
    st.text(names[1])
    st.image(posters[1])

with col3:
    st.text(names[2])
    st.image(posters[2])

with col4:
    st.text(names[3])
    st.image(posters[3])

with col5:
    st.text(names[4])
    st.image(posters[4])