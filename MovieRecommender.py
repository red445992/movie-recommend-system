import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie posters
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4ad460ddd1e37663f2ee603d909e2607")
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Load pre-trained data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit title
st.title("🎬 Movie Recommendation System")

# Movie selection dropdown
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values,
    index=0,  # Pre-select the first movie for better UX
    placeholder="Search for a movie...",
)

# Recommendation button
if st.button("Get Recommendations"):
    names, posters = recommend(selected_movie_name)
    
    # Display recommendations as cards
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.header(name)  # Movie title
            st.image(poster, width=150, use_container_width=True) # Poster
            
