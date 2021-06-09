from pymongo import MongoClient
import json
from urllib.parse import quote_plus
from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# retrieve credentials from file
with open('credentials.json') as f:
    credentials = json.load(f)

uri = f"mongodb://{quote_plus(credentials['username'])}\
:{quote_plus(credentials['password'])}\
@{credentials['host']}\
:27017\
/rhobs"

# connect to database
client = MongoClient(uri)

db = client[credentials['db']]
collection = db['test']

## 0. The number of listeners by music. 
def dico_nb_listener() :
    res = {}
    cursor = collection.find({})
    for doc in cursor :
        keys = [key for key in doc.keys() if key != '_id']
        assert len(keys) == 1
        doc_infos = doc[keys[0]]
        for genre in doc_infos['music'] :
            if genre in res :
                res[genre] += 1
            else :
                res[genre] = 1
    return res

# final_dic_nb_listeners = dico_nb_listener()

def nb_listener(genre, final_dic) :
    if genre in final_dic :
        return final_dic[genre]
    else :
        return "Pas de nombre moyen d'auditeurs car ce genre n'est pas connu"

# Résultat : 
# final_dic_nb_listeners =
# {'country': 18971,
#  'blues': 20817,
#  'hiphop': 28043,
#  'metal': 27774,
#  'rock': 34472,
#  'disco': 34297,
#  'pop': 32249,
#  'reggae': 19127,
#  'jazz': 24304,
#  'gabber': 18525,
#  'trance': 18173,
#  'eurodance': 23487,
#  'classical': 21306}
# 
# Soit 321545 genre-auditeurs pour 82816
# donc 321545/82816 ~= 3.9 genres écoutés par personne en moyenne

## 1. The average age by music. 
def dico_average_age() :
    """
    This is what res should look like
    res = {
        'country' : {
            'nb_days'  : 95000,
            'nb_people': 15 
        },
        'pop' : {
            'nb_days'  : 155000,
            'nb_people': 20 
        },
        ...
    }
    """
    res = {}
    cursor = collection.find({})
    present_day = datetime.now()

    for doc in cursor :
        keys = [key for key in doc.keys() if key != '_id']
        assert len(keys) == 1
        doc_infos = doc[keys[0]]

        for genre in doc_infos['music'] :
            birthdate = datetime.strptime(doc_infos['birthdate'], '%Y-%m-%d')
            exact_age = present_day - birthdate
            if genre in res :
                res[genre]['nb_days']   += exact_age
                res[genre]['nb_people'] += 1
            else :
                res[genre] = {
                    'nb_days'  : exact_age,
                    'nb_people': 1
                }
    return res

def convert_dico(dico) :
    def normalize(dic) :
        average_in_days = (dic['nb_days'].days/dic['nb_people'])
        average_age = int(average_in_days/365)
        return average_age

    new_dic = {genre:normalize(dic) for genre, dic in dico.items()}
    return new_dic

# final_dic_average_ages = convert_dico(dico_average_age())

def average_age(genre, final_dic) :
    if genre in final_dic :
        return final_dic[genre]
    else :
        return "Pas d'âge moyen car ce genre n'est pas connu"

# Résultat :
#
# final_dic_average_ages
# {'country': 42,
#  'blues': 50,
#  'hiphop': 39,
#  'metal': 38,
#  'rock': 43,
#  'disco': 43,
#  'pop': 41,
#  'reggae': 39,
#  'jazz': 47,
#  'gabber': 38,
#  'trance': 40,
#  'eurodance': 39,
#  'classical': 47}


## 2. The population pyramid

def dataframe_pyramid(city) :
    cursor = collection.find({})
    present_day = datetime.now()
    df = pd.DataFrame(columns=['Population'])

    for doc in cursor :
        keys = [key for key in doc.keys() if key != '_id']
        assert len(keys) == 1
        doc_infos = doc[keys[0]]

        if doc_infos['city'] == city :
            birthdate = datetime.strptime(doc_infos['birthdate'], '%Y-%m-%d')
            exact_age = present_day - birthdate
            age_in_years = int(exact_age.days/365)
            if age_in_years in df.index :
                df.loc[age_in_years,'Population'] += 1
            else :
                df.loc[age_in_years,'Population'] = 1
    
    age_min = min(df.index)
    for x in range(age_min) :
        df.loc[x,'Population'] = 0
    return df

def plot_pyramid(city, slice) :
    data = dataframe_pyramid(city)

    _, ax = plt.subplots(figsize=(8,8))
    
    data = data.groupby(by=lambda x : f"{slice*(x//slice)}-{slice*(x//slice+1)-1}")['Population'].sum()
    data.sort_index(inplace= True, key= np.vectorize(lambda x : int(x[:x.index('-')])))

    ax.barh(data.index, data.values)
    titre = f"Pyramide des âges de la ville de {city} pour un pas de {slice} année" + "s"*(slice>1)
    ax.set_title(titre)
    ax.set_ylabel("Ages")
    ax.set_xlabel("Habitants")

    plt.savefig(f'{city} - {slice} ans.png')

plot_pyramid('Blin',3)
plot_pyramid('Foucher',10)
plot_pyramid('Saint Thibaut',5)
plot_pyramid('Sainte Corinne',7)