import pandas as pd
import numpy as np
import re
import string
import collections
import time
from pytrie import StringTrie as Trie
from flask import Flask, Response
from flask_restful import Resource, Api
import distance

app = Flask(__name__)
api = Api(app)

train  = pd.read_csv("train.csv",header=None)
    



def preprocessing(pre_string):
    #Function replaces special characters with spaces
    
    for ch in ["'s"]:
        if ch in pre_string:
            pre_string = pre_string.replace(ch,"s ")
    
    pre_string = pre_string.replace("dhosa"," dosa ")
            
    pre_string = pre_string.translate ({ord(c): " " for c in "'1234567890!@#$%^*()[]{};:,./<>?\|`~-=_+"})
    
    for ch in ['&',' n ',"n\'"," N ","-N-"]:
        if ch in pre_string:
            pre_string = pre_string.replace(ch," and ")
    
    return pre_string.lower()

inverted_index = dict()

t0 = time.time() #Start time
for index, row in train.iterrows():
    #Normalise the names of dishes.
    
    with_sc = row[1]
    
    processed_string = preprocessing(with_sc)
    
    for token in processed_string.split():
        #Create Inverted Index
        if inverted_index.get(token)==None:
            inverted_index.update({token:set()})
        inverted_index[token].add(row[0])
        
prefix_tree = Trie(**inverted_index)

t1 = time.time() - t0 #Time required for index construction

print("Time taken for Trie generation: {} ".format(t1))
    

def search_results(query):
    #Return primary keys for query matching strings
    
    t0 = time.time() #Start time
    
    found = False
    
    processed_query = preprocessing(query) #Apply same pre-processing as before
    
    list_of_indices = []
    
    for token in processed_query.split():
        #generate suggestions for each word in the trie for query as prefix
        suggestions = prefix_tree.values(prefix=token)
        if suggestions!=[] :
            found = True
            list_of_indices.append(set.union(*suggestions))
        else:
            for term in list(inverted_index.keys()):
                if distance.levenshtein(token, term)<=2:
                    found = True
                    list_of_indices.append(inverted_index[term])
                    break
                    

    if found and len(list_of_indices)==1:
        intersection_list = list_of_indices[0]
    elif found and len(list_of_indices)>1:
        intersection_list = set.intersection(*list_of_indices) #Intersection of postings
        
        joint_result = prefix_tree.values(prefix=("".join(processed_query.split())))
        
        if joint_result!=[]:
            #check if combining two words also a word in voacabulary
            for posting in joint_result:
                for item in posting:
                    intersection_list.add(item)
    else:
        intersection_list = []
        
    t1 = time.time() - t0 #Time required for results
    print("Time taken for fetching results : {} ".format(t1))
    
    return intersection_list

class search_json(Resource):
    def get(self, query):
        results = train.loc[train[0].isin(search_results(query))].reset_index().drop('index',axis=1)
        resp = Response(response=results.to_json(orient='records'),
        status=200,
        mimetype="application/json")
        return(resp)

api.add_resource(search_json, '/bunny/<query>') # Route_3


@app.route('/')
def index():
    return 'OK'

if __name__ == "__main__":
    app.run()
