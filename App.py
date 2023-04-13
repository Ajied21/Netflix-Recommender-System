"""
    ajied
"""

import streamlit as st
from PIL import Image
import json
from Recommended import recommend
from bs4 import BeautifulSoup
import requests,io
import PIL.Image
from urllib.request import urlopen

with open('movie_data.json', 'r+', encoding='utf-8') as f:
    movie_data = json.load(f)
with open('movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)

with open('tv_data.json', 'r+', encoding='utf-8') as f:
    tv_data = json.load(f)
with open('tv_titles.json', 'r+', encoding='utf-8') as f:
    tv_titles = json.load(f)

def all_poster_fetcher(net_link):
    ## Display Movie Poster
    url_data = requests.get(net_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    dp = s_data.find("meta", property="og:image")
    all_poster_link = dp['content']
    u = urlopen(all_poster_link)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    image = image.resize((300, 300), )
    st.image(image, use_column_width=False)

    if all_poster_link == None:
        print("Movie is not available or is no longer showing")

def get_movie_info(net_link):
    url_data = requests.get(net_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    content = s_data.find("meta", property="og:description")
    movie_descr = content['content']
    movie_descr = str(movie_descr).split('.')
    movie_director = movie_descr[0]
    movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()

    if movie_descr == None:
        print("Movie is not available or is no longer showing")

    return movie_director,movie_cast

def get_tv_info(imdb_link):
    url_data = requests.get(imdb_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    content = s_data.find("meta", property="og:description")
    tv_descr = content['content']
    tv_descr = str(tv_descr).split('.')
    tv_director = tv_descr[0]
    tv_cast = str(tv_descr[1]).replace('With', 'Cast: ').strip()

    if tv_descr == None:
        print("TV-Show is not available or is no longer showing")

    return tv_director,tv_cast

def Movie_Recommender(test_point, n):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = recommend(movie_data, target, test_point, n=n)
    # Run the algorithm
    model.fit()
    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2],movie_data[i][-1]])
    print(table)
    return table

def TV_Recommender(test_point, n):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = recommend(tv_data, target, test_point, n=n)
    # Run the algorithm
    model.fit()
    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([tv_titles[i][0], tv_titles[i][2],tv_data[i][-1]])
    print(table)
    return table

st.set_page_config(
   page_title="Movie & TV-Show Netflix Recommender System",
)

def run():

    img1 = Image.open('Net.png')

    img1 = img1.resize((750,350),)

    st.image(img1,use_column_width=False)

    st.markdown("<h1 style='text-align: center; color: grey;'>Welcome to My Project</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: White;'>🎬 Movie & Tv_Show Netflix Recommender System 🎬</h3>", unsafe_allow_html=True)

    
    #genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History',
    #          'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']
    
    movies = [title[0] for title in movie_titles]
    tv = [title[0] for title in tv_titles]
    category = ['--Select--', 'Movie based', 'TV-Show based']
    cat_op = st.selectbox('Select Recommendation Type', category)


    if cat_op == category[0]:
        st.warning('Please select Recommendation Type')

    elif cat_op == category[1]:
        select_movie = st.selectbox('Select movie: (Recommendation will be based on this selection)', ['--Select--'] + movies)
        dec = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        
        if dec == 'No':

            if select_movie == '--Select--':
                st.warning('Please select Movie!!')

            else: 
                if st.button('Show Recommendation'):
                    no_of_reco = st.slider('Number of movies you want Recommended:', min_value=1, max_value=10, step=1)
                    genres = movie_data[movies.index(select_movie)]
                    test_points = genres
                    table = Movie_Recommender(test_points, no_of_reco+1)
                    table.pop(0)
                    c = 0
                    st.success('Some of the movies from our Recommendation, have a look below')

                    for movie, link, ratings in table:
                        c+=1
                        director,cast = get_movie_info(link)
                        st.markdown(f"({c})[ {movie}]({link})")
                        st.markdown(director)
                        st.markdown(cast)
        else:

            if select_movie == '--Select--':
                st.warning('Please select Movie!!')

            else:
                if st.button('Show Recommendation'):
                    no_of_reco = st.slider('Number of movies you want Recommended:', min_value=1, max_value=10, step=1)
                    genres = movie_data[movies.index(select_movie)]
                    test_points = genres
                    table = Movie_Recommender(test_points, no_of_reco+1)
                    table.pop(0)
                    c = 0
                    st.success('Some of the movies from our Recommendation, have a look below')

                    for movie, link, ratings in table:
                        c += 1
                        st.markdown(f"({c})[ {movie}]({link})")
                        all_poster_fetcher(link)
                        director,cast = get_movie_info(link)
                        st.markdown(director)
                        st.markdown(cast)

    elif cat_op == category[2]:
        select_TV = st.selectbox('Select TV-Show: (Recommendation will be based on this selection)', ['--Select--'] + tv)
        dec = st.radio("Want to Fetch Tv-Show Poster?", ('Yes', 'No'))
        
        if dec == 'No':

            if select_TV == '--Select--':
                st.warning('Please select Tv_Show!!')

            else:
                if st.button('Show Recommendation'):
                    no_of_reco = st.slider('Number of TV-Show you want Recommended:', min_value=1, max_value=10, step=1)
                    genres = tv_data[tv.index(select_TV)]
                    test_points = genres
                    table = TV_Recommender(test_points, no_of_reco+1)
                    table.pop(0)
                    c = 0
                    st.success('Some of the Tv-Show from our Recommendation, have a look below')

                    for tv, link, ratings in table:
                        c+=1
                        director,cast = get_tv_info(link)
                        st.markdown(f"({c})[ {tv}]({link})")
                        st.markdown(director)
                        st.markdown(cast)
        else:

            if select_TV == '--Select--':
                st.warning('Please select Tv-Show!!')

            else:
                if st.button('Show Recommendation'):
                    no_of_reco = st.slider('Number of Tv-Show you want Recommended:', min_value=1, max_value=10, step=1)
                    genres = tv_data[tv.index(select_TV)]
                    test_points = genres
                    table = TV_Recommender(test_points, no_of_reco+1)
                    table.pop(0)
                    c = 0
                    st.success('Some of the Tv-Show from our Recommendation, have a look below')

                    for tv, link, ratings in table:
                        c += 1
                        st.markdown(f"({c})[ {tv}]({link})")
                        all_poster_fetcher(link)
                        director,cast = get_tv_info(link)
                        st.markdown(director)
                        st.markdown(cast)

run()

hide_menu_style = """
       <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

footer="""
    <style>
    a:link , a:visited{
    color: white;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: white;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    font-weight: bold;
    position: fixed;
    height: 50px;
    width: 50px;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: maroon;
    color: white;
    text-align: center;
    }
    </style>
    <div class="footer">
    <p class="center">Developed with by : <a href="https://www.linkedin.com/in/dhoifullahluthmajied/" target="_blank">Dhoifullah Luth Majied</a><br />
         Copyright &copy; 2023</p>
    </div>
    """

st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown(footer,unsafe_allow_html=True)
