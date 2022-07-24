import spacy

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
