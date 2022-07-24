# Revised Recs Grpah

import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
from modules import lemmatize ,check_space

def recipe():
  df = pd.read_csv('data/recs_dataset.csv')# calling cleaned dataset 
  
  ing = df.graph_ingredient
  ti = df.Filtered_title
  
  B = nx.Graph()
  # Add nodes| with the node attribute "bipartite"
  top_nodes = pd.read_excel('data/ingredient_node.xlsx' ,engine='openpyxl').ingredient_node # Call the ingredients.xlsx and load all ingredients 
  bottom_nodes = ti
  B.add_nodes_from(top_nodes, bipartite=0)
  B.add_nodes_from(bottom_nodes, bipartite=1)
  # Add edges with weights

  [ [ B.add_edge(ti[count] ,j)  for j in check_space(ing[count]) if j != ' 'and j != '  'and j != '' ] for count in range(len(ti)) ] # Add edges with weights

  return dict([(n, nbrdict) for n, nbrdict in B.adjacency()]) ,df


def sorting(cuisine ,category,recs_df):

    length =len(category)
    if len(cuisine)>len(category):length = len(cuisine)

    cui = recs_df['Cuisine'] == cuisine[0]
    typ = recs_df['Category'] == category[0]
    for i in range(length):
        try:cui+=recs_df['Cuisine'] == cuisine[i]
        except:IndexError
        try:typ += recs_df['Category'] == category[i]
        except:IndexError
    return recs_df[cui*typ]