
import pickle
import streamlit as st
import requests
import time
from datetime import datetime
import random

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def recommend(movie):
   
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def recFromRated(movie,diction):
    if len(st.session_state.Rated_Dict) != 0:
        index = movies[movies['title'] == movie].index[0]
        keylist =list(diction.keys())
        value = list(diction.values())

        cos = []
        cosValues = dict()
    

        for i in keylist:
            cos.append( movies[movies['title'] == i].index[0])

        
        for i in cos:
            # cosValues = sorted(list(enumerate(similarity[index][i])),reverse=True, key=lambda x: x[1])
            cosValues[i] = similarity[index][i]
            
        highestcos = max(cosValues, key=lambda k: cosValues[k])

        distances = sorted(list(enumerate(similarity[highestcos])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters






st.markdown("<h1 style='text-align: center;'>MovieManiax</h1>", unsafe_allow_html=True)
st.write("<hr>", unsafe_allow_html=True)

movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

if 'submit_count' not in st.session_state:
    st.session_state.submit_count = 0

if 'Rated_Dict' not in st.session_state:
    st.session_state.Rated_Dict = {}

if "History" not in st.session_state:
     st.session_state.History = {}



page = st.sidebar.radio("Select a page", ["Home","Rate", "History"])

if page == "Rate":
    st.header("Rate Your Favourite Movies")
   
    with st.form(key="rating_form"):
            
            moviess = st.selectbox("Type or select a movie from the dropdown", movies['title'].values) 
            rating = st.selectbox("Rate from 1 to 5", [1, 2, 3, 4, 5])
            submitted = st.form_submit_button("Submit Rating")

            if submitted:
                st.session_state.Rated_Dict[moviess] = rating

     




   

elif page == "Home":
    st.header("Search For Worlds Latest movies")

    with st.form(key="creating_form"):
        selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)
        bigsubmitted = st.form_submit_button("Recommendation")

    if bigsubmitted:
       
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        columnz = st.columns(len(recommended_movie_names))
        
        click_time = time.time()

        st.session_state.History[selected_movie] = datetime.fromtimestamp(click_time).strftime('%Y-%m-%d %H:%M:%S')

        for i in range(len(recommended_movie_names)):
            with columnz[i]:
                st.text(recommended_movie_names[i])
               
                st.image(recommended_movie_posters[i], use_column_width=True,caption=recommended_movie_names[i])

        
        

        

        if len(st.session_state.Rated_Dict) != 0:
            st.header("Suggest from earlier ratings")
            columny =  st.columns(len(recommended_movie_names))

            rec_rated_movie_names, rec_rated_movie_posters = recFromRated(selected_movie,st.session_state.Rated_Dict)


            
            
            
            for i in range(len(rec_rated_movie_names)):
                with columny[i]:
                    st.text(rec_rated_movie_names[i])
                
                    st.image(rec_rated_movie_posters[i], use_column_width=True,caption=rec_rated_movie_names[i])




elif page == "History":
 st.header("Search History")
 if len(st.session_state.History) != 0:
    # st.write(st.session_state.History)

    for key, value in st.session_state.History.items():
        st.write(f"{key} - {value}")

    
    randmovie = random.choice(list(st.session_state.History.keys()))

    rand_movie_names, rand_movie_posters = recommend(randmovie)
    columnhis = st.columns(len(rand_movie_names))
     
    for i in range(len(rand_movie_names)):
            with columnhis[i]:
                st.text(rand_movie_names[i])
                
                st.image(rand_movie_posters[i], use_column_width=True,caption=rand_movie_names[i])










    


 
 