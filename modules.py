import spacy
import urllib.request
import streamlit as st

def check_space(ing:str):
  r'''
  arg : str of ingredinets
  return : list of ingredients seperator by comma
  '''
  ing =  ing.replace(', ,',',').replace(',  ,',',').replace(' ,',',').replace(', ',',')
  if ing[-1] == ' ':ing = ing[:-1]
  if ing[-1] == ',':ing = ing[:-1]
  return ing.split(',')
  
def lemmatize(ins:str):
  r'''
  arg : str type sentences 
  return : lemmatized str type sentences
  '''
  nlp = spacy.load('en_core_web_sm')
  doc = nlp(ins)

  return ' '.join([token.lemma_ for token in doc])

def multi_token(ing:list):
  r'''
  arg : list of Ingredinets
  return : combined double word Ingredient into single word in list form 
  '''
  for i in range(len(ing)):
    if ' ' in ing[i]: ing[i] = ing[i].replace(' ','_')
  return ing

def regex(dic:dict):
  r'''
  arg : dictionary of ingredient and its alternative
  return : dictionary of ingredient where dic.value have been changed based on the given condition
  '''  
  l = ['_syrup' ,'_extract' ,'_essence' ,'_paste' ,'_juice','_puree' ]
  for key in dic.keys():
    for i in l: 
      if i in key: 
        if dic[key][0] != key.replace(i,''):
          dic[key][1] = dic[key][0]
          dic[key][0] = key.replace(i,'')
  return dic

def check(inp_ing_str ,file_name):
    with open(file_name ,'r') as file:
        if file.read() == inp_ing_str:
            return 0
        if file.read() != inp_ing_str:
            with open(file_name ,'w') as file:
                file.write(inp_ing_str)
                return 1

def detail_rec(recommend ,i):
    urllib.request.urlretrieve(recommend.iloc[i]['Image'],"img.png")

    #st.markdown(f"<h1 style='text-align: Center; color:  LightSlateGray;font-size: 40px;'> {recommend.iloc[i]['Title']} </h1>", unsafe_allow_html=True) # Title
    st.subheader(recommend.iloc[i]['Title'])
    col1, col2 = st.columns([2,3])

    cuisine =recommend.iloc[i]['Cuisine']
    cat = recommend.iloc[i]['Category']
    link = recommend.iloc[i]['Link']

    col2.markdown(f'**🍴 {cuisine} cuisine**')
    col2.markdown(f'**🍴 {cat}**')

    col1.image('img.png',width =350 ,channels = 'BGR',caption = 'Dish Image')
    col2.markdown(recommend.iloc[i]['Ingridients'].replace("'" ,'').replace('[','').replace(']',''))
    col1.markdown(f"check out this [link]({link}) for more details 📃")