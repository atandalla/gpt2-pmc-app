from flask_restful import Resource, abort, request
import requests
import json
import urllib
import nltk
nltk.download('stopwords') 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np
import transformers 
import time
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import pipeline
from urllib.parse import unquote

#########################################FUNCIONES############################################

##Normalizacion
def normalizacion(doc):
    doc = re.sub('[^A-Za-z0-9]+', ' ', doc)
    doc = doc.lower()
    doc_tokens = doc.split()  # Tokenización
    list_stopwords = stopwords.words('english') #Eliminacion de stopwords
    for word in doc_tokens:
        if word in list_stopwords:
            doc_tokens.remove(word)
    stemmer = PorterStemmer()  #Proceso de Stemming
    doc_tokens1 = [stemmer.stem(word) for word in doc_tokens]
    doc = doc_tokens1
    return doc

def similitudJaccard(d1,d2):
    simi_jaccard=(len(d1.intersection(d2))) / len(d1.union(d2))
    return simi_jaccard
####################################################################################
class IndexDocs(Resource):
    def get(self, getquery):
        query=[unquote(getquery)]
        URL = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+getquery+'&resultType=core&cursorMark=*&pageSize=100&format=json' #configuramos la url
        data = requests.get(URL)
        json_post = data.json()
        title=[feature["title"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        keyword=[" ".join(feature["keywordList"]["keyword"]) for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        authors=[feature["authorString"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        abstract=[feature["abstractText"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        id_pub=[feature["id"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        pubyear=[feature["pubYear"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        doi=[feature["doi"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        url=[feature["fullTextUrlList"]["fullTextUrl"][0]["url"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        ##Inicializacion data
        data_abstract=[]
        data_title=[]
        data_keyword=[]
        data_abstract=data_abstract+query+abstract
        data_title=data_title+query+title
        data_keyword=data_keyword+query+keyword

        ##########################################NORMALIZACION##############################################
        data_normalizados_abstract=[" ".join(normalizacion(data_abstract[i])) for i in range(len(data_abstract))]
        data_normalizados_title = [normalizacion(data_title[i]) for i in range(len(data_abstract))]
        data_normalizados_keyword = [normalizacion(data_keyword[i]) for i in range(len(data_abstract))]
        #########################################SIMILITUD COSENO############################################
        tfidf = TfidfVectorizer().fit_transform(data_normalizados_abstract)
        #Similitud coseno
        simi_coseno_abstract=cosine_similarity(tfidf[0:1], tfidf).flatten()
        ########################################SIMILITUD JACCARD############################################
        simi_jaccard_title=[similitudJaccard(set(data_normalizados_title[0]),set(data_normalizados_title[i])) for i in range(len(data_abstract))]
        simi_jaccard_keyword=[similitudJaccard(set(data_normalizados_keyword[0]),set(data_normalizados_keyword[i])) for i in range(len(data_abstract))]

        similitud_final= (np.array(simi_jaccard_title)*0.10)+ (np.array(simi_jaccard_keyword)*0.20)+(np.array(simi_coseno_abstract)*0.70)
        salida_ordena= np.argsort(-1*similitud_final)

        resultados=[{ "id": id_pub[salida_ordena[i]-1],"doi": doi[salida_ordena[i]-1],"title": title[salida_ordena[i]-1], "author":authors[salida_ordena[i]-1],"pubyear": pubyear[salida_ordena[i]-1],"url": url[salida_ordena[i]-1], "keyword":keyword[salida_ordena[i]-1], "abstract":abstract[salida_ordena[i]-1]} for i in range(1,len(salida_ordena))]

        return resultados, 200

####################################################################################
class ResultSimi(Resource):
    def get(self, getquery1):
        query=[unquote(getquery1)]
        URL = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+getquery1+'&resultType=core&cursorMark=*&pageSize=600&format=json' #configuramos la url
        data = requests.get(URL)
        json_post = data.json()
        title=[feature["title"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        keyword=[" ".join(feature["keywordList"]["keyword"]) for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        authors=[feature["authorString"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        abstract=[feature["abstractText"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        id_pub=[feature["id"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        pubyear=[feature["pubYear"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        doi=[feature["doi"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        url=[feature["fullTextUrlList"]["fullTextUrl"][0]["url"] for feature in json_post["resultList"]["result"] if "keywordList" in feature and "abstractText" in feature and "authorString" in feature and "title" in feature and "pubYear" in feature and "doi" in feature and "id" in feature and "fullTextUrlList" in feature]
        ##Inicializacion data
        data_abstract=[]
        data_title=[]
        data_keyword=[]
        data_abstract=data_abstract+query+abstract
        data_title=data_title+query+title
        data_keyword=data_keyword+query+keyword
        ##########################################NORMALIZACION##############################################
        data_normalizados_abstract=[" ".join(normalizacion(data_abstract[i])) for i in range(len(data_abstract))]
        data_normalizados_title = [normalizacion(data_title[i]) for i in range(len(data_abstract))]
        data_normalizados_keyword = [normalizacion(data_keyword[i]) for i in range(len(data_abstract))]
        #########################################SIMILITUD COSENO############################################
        tfidf = TfidfVectorizer().fit_transform(data_normalizados_abstract)
        #Similitud coseno
        simi_coseno_abstract=cosine_similarity(tfidf[0:1], tfidf).flatten()
        ########################################SIMILITUD JACCARD############################################
        simi_jaccard_title=[similitudJaccard(set(data_normalizados_title[0]),set(data_normalizados_title[i])) for i in range(len(data_abstract))]
        simi_jaccard_keyword=[similitudJaccard(set(data_normalizados_keyword[0]),set(data_normalizados_keyword[i])) for i in range(len(data_abstract))]

        similitud_final= (np.array(simi_jaccard_title)*0.10)+ (np.array(simi_jaccard_keyword)*0.20)+(np.array(simi_coseno_abstract)*0.70)
        salida_ordena= np.argsort(-1*similitud_final)

        resultados=[{ "id": id_pub[salida_ordena[i]-1],"doi": doi[salida_ordena[i]-1],"title": title[salida_ordena[i]-1], "author":authors[salida_ordena[i]-1],"pubyear": pubyear[salida_ordena[i]-1],"url": url[salida_ordena[i]-1], "keyword":keyword[salida_ordena[i]-1], "abstract":abstract[salida_ordena[i]-1]} for i in range(2,5)]

        return resultados, 200

####################################################################################
class GPT2(Resource):
    
    def get(self, getquery2,abstract1):

        start_time = time.time()
        title=unquote(getquery2)
        abstract_original=unquote(abstract1)
        palabras_original=len(abstract_original.split())
        num_palabras=palabras_original

        long_palabras_aumentada = palabras_original + (palabras_original*0.48) 

        with open("../gpt2-europe-v3/config.json", "r") as jsonfile:
            data = json.load(jsonfile) # Reading the file
            print("Read successful")
            jsonfile.close()

        data['task_specific_params']['text-generation']['max_length'] = int(long_palabras_aumentada)

        print("Date updated")
        with open("../gpt2-europe-v3/config.json", "w") as jsonfile:
            myJSON = json.dump(data, jsonfile) # Writing to the file
            print("Write successful")
            jsonfile.close()  
        
        resumen = pipeline('text-generation',model='../gpt2-europe-v3', tokenizer='gpt2')
        text=resumen(title)
        abstract_gpt2=text[0]['generated_text']
        abstract_gpt2 = abstract_gpt2.replace(title+" ", '')
        abstract_gpt2 = abstract_gpt2.capitalize()
        abstract_final_gpt2 = ''
        abstract_final_gpt2_extra = ''

        i=0
        pos_final_abstract = abstract_gpt2.rfind(".")

        for i in range(0,pos_final_abstract+1):
            abstract_final_gpt2 = abstract_final_gpt2 + abstract_gpt2[i]

        data_abstract=[]
        data_abstract.append(abstract_original)
        data_abstract.append(abstract_final_gpt2)
        palabras_gpt2=len(abstract_final_gpt2.split())
        #similitud coseno
        data_normalizados_abstract=[" ".join(normalizacion(data_abstract[i])) for i in range(len(data_abstract))]
        #similitud jaccard
        data_normalizados_abstract2=[normalizacion(data_abstract[i]) for i in range(len(data_abstract))]

        #Similitud coseno
        tfidf = TfidfVectorizer().fit_transform(data_normalizados_abstract)
        simi_coseno_abstract=cosine_similarity(tfidf[0:1], tfidf).flatten()
        #Similitud jaccard
        simi_jaccard_abstract=similitudJaccard(set(data_normalizados_abstract2[0]),set(data_normalizados_abstract2[1]))

        print("---Tiempo de Procesamiento:  %s seconds ---" % (time.time() - start_time))
        timegpt2=time.time() - start_time
        result={'new_abstract': abstract_final_gpt2,'num_words_original': palabras_original,'num_words_gpt2': palabras_gpt2,'simi_coseno': simi_coseno_abstract[1],'simi_jaccard': simi_jaccard_abstract, 'timeGPT2': timegpt2}
        
        return result,200

