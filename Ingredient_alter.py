from modules import lemmatize  ,multi_token ,regex
from gensim.models import Word2Vec

def check_space(ing:str):
  r'''
  arg : str of ingredinets
  return : list of ingredients seperator by comma
  '''
  ing =  ing.split(',')
  for i in range(len(ing)):
    if ing[i][0] ==' ':ing[i] = ing[i][1:]
    if ing[i][-1]==' ':ing[i] = ing[i][:-1]
  return ing

def alter(ingredient_alt):
    model = Word2Vec.load('model_weight/ingredient_alt.model') 
    df_ing = pd.read_excel('data/ingredient.xlsx')
    ings = multi_token(check_space(lemmatize(ingredient_alt)))
    result = {item : [j[0] for j in model.wv.similar_by_word(item)[:2]]  for item in ing}
    return regex(result)