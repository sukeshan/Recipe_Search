import streamlit as st
import cv2
import pandas as pd
from recs import recipe ,sorting 
from modules import lemmatize ,check_space ,check ,detail_rec
from alternative import alter
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

st.set_page_config(
    page_title=" гëɕട",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Title

st.markdown("<h1 style='text-align: center; color: Grey;font-size: 60px;'> Recipe Search</h1>", unsafe_allow_html=True)

search_help = set(pd.read_excel('data/ingredient_node.xlsx').ingredient_node)

# Input
inp_ing = st.multiselect( '' ,search_help)
col1, col2= st.columns([4, 5])


# Sidebar

st.sidebar.subheader('Prefer your cuisine ')
cuisine = st.sidebar.multiselect('',['Continental' ,'North Indian' ,'American' ,'South India' ,'Mexican' ,'Thai'])

st.sidebar.subheader('Prefer your Food Type ')
category = st.sidebar.multiselect('',['desserts' ,'dinner' ,'snacks' ,'appetizers' ,'breakfast' ,'lunch'])


# Filter

col2.button('Search a Recipe 🍽️')


# Pantry
st.sidebar.subheader('Pantry')
pantry = st.sidebar.multiselect('' ,search_help , key = "<uniquevalueofsomesort>")

inp_ing+=pantry

# Ingredient alternative

st.sidebar.subheader('Ingredient Alternative')
ingredient_alt = st.sidebar.text_input('')
if len(ingredient_alt) >=1 : st.sidebar.subheader(alter(ingredient_alt) + ' are sharing same characterstics')

if len(cuisine) ==0: cuisine = ['Continental' ,'North Indian' ,'American' ,'South India' ,'Mexican' ,'Thai']
if len(category) ==0 :category = ['desserts' ,'dinner' ,'snacks' ,'appetizers' ,'breakfast' ,'lunch']


#Graph Sorting-------------------------------------------------------------------------------------------------------------------------------------------------------------
if check(str(inp_ing + cuisine +category+pantry) ,'data/check_ing.txt') ==1 :
    adj,df = recipe()
    un_listed_words = []
    lis =[]
    for recp in inp_ing:
        
        try:lis+=list(adj[lemmatize(recp.lower())])
        except KeyError:un_listed_words.append(lemmatize(recp))
            
    lis_set = list(set(lis))

    recs = [(lis.count(recipe) + len(inp_ing) / len(adj[recipe].keys()) ,recipe ) for recipe in lis_set if lis.count(recipe) >= len(inp_ing)-3 and len(inp_ing)/len(adj[recipe].keys()) >=.4 ]
    recs.sort(reverse = True)
    len_recs = len(recs)
    # Sort
    

    #DataFrame----------------------------
    recs_df = pd.DataFrame(columns=['Title', 'Cuisine', 'Category', 'Ingridients', 'Instructions', 'Image',
        'Link', 'Ratings', 'Filtered_ingridient', 'Filtered_title',
        'Filtered_cuisine'] )


    for i in range(len(recs)):recs_df = recs_df.append(df[(df.Filtered_title == recs[i][1]) ]) #& (df.Cuisine == 'Thai') & (df.Category == category[0])

    recs_df.drop(columns=['Filtered_ingridient' ,'Filtered_title' ,'Filtered_cuisine'] ,inplace = True)
    recommend = sorting(cuisine ,category ,recs_df)
    #recommend.drop_duplicates('Title' ,inplace = True)
    recommend.to_csv('data/recommend.csv' , index = False)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

rec = pd.read_csv('data/recommend.csv')

sort = st.slider('Sorting ', 0, len(rec), 10)
st.write( f'Recommending  {sort}  recipes' )

for i in range(sort):
   if len(rec) >=1: detail_rec(rec,i)
   if len(rec) ==0 : detail_rec(pd.read_csv('data/recs_cleaned_dataset.csv' )[:15],i)



