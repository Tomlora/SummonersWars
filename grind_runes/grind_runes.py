#!/usr/bin/env python
# coding: utf-8
# convertit avec jupyter nbconvert mynotebook.ipynb --to python

# In[112]:


import pandas as pd
import numpy as np
import json
import plotly.express as px
import ast
import requests

# fix plotly express et Visual Studio Code
import plotly.io as pio
pio.renderers.default = "notebook_connected"




# In[113]:


def extraire_variables_imbriquees(df, colonne):
    df[colonne] = [ast.literal_eval(str(item)) for index, item in df[colonne].iteritems()]

    df = pd.concat([df.drop([colonne], axis=1), df[colonne].apply(pd.Series)], axis=1)
    return df

def export_excel(data, data_short, data_property, data_count):
        writer = pd.ExcelWriter("resultat/fichier.xlsx")
        data.to_excel(writer, startrow=0, sheet_name='Data_complete', index=True)
        data_short.to_excel(writer, startrow=0, sheet_name='Par rune et monstre', index=True)
        data_property.to_excel(writer, startrow=0, sheet_name='Par set', index=True)
        data_count.to_excel(writer, startrow=0, sheet_name='Par set et propriété', index=False)
        
        workbook = writer.book
        worksheet1 = writer.sheets['Data_complete']
        worksheet2 = writer.sheets['Par rune et monstre']
        worksheet3 = writer.sheets['Par set']
        worksheet4 = writer.sheets['Par set et propriété']

        # Gestion de la taille des colonnes

        cell_format = workbook.add_format({'valign':'vcenter', 'align': 'center'})
        cell_format.set_text_wrap()
        for i, col in enumerate(data.columns):
                worksheet1.set_column(i, i+1, 20, cell_format) # colonne, colonne, len_colonne, format colonne
        for i, col in enumerate(data_short.columns):
                worksheet2.set_column(i, i+1, 20, cell_format) # colonne, colonne, len_colonne, format colonne
        for i, col in enumerate(data_property.columns):
                worksheet3.set_column(i, i+1, 20, cell_format) # colonne, colonne, len_colonne, format colonne
        for i, col in enumerate(data_count.columns):
                worksheet4.set_column(i, i+1, 20, cell_format) # colonne, colonne, len_colonne, format colonne

        writer.save()
        



def swarfarm_monstres():
        # database swarfarm
    url = "https://swarfarm.com/api/v2/monsters/?page=1"
    r = requests.get(url=url)
    data = r.json()
    df = pd.DataFrame(data)


    for i in range(2,21):
        url = f"https://swarfarm.com/api/v2/monsters/?page={i}"
        r = requests.get(url=url)
        data = r.json()
        df2 = pd.DataFrame(data)
        df = pd.concat([df, df2])
        
        
    # on extrait les variables du dict dans la colonne ['results'] et on supprime ce qui m'intéresse pas
    df = extraire_variables_imbriquees(df, 'results')
    df.drop(['next', 'previous'], axis=1, inplace=True)
    # On garde ce qui nous intéresse
    df_mobs_swarfarm = df[['id', 'url', 'com2us_id', 'family_id', 'name']]

    df_mobs_swarfarm.to_excel('swarfarm.xlsx', index=False)


# # Import data

# In[114]:

url_json = input('Lien du json ?')
f = open(url_json, encoding="utf8")


# In[115]:


# On charge le json
data_json = json.load(f)


# In[116]:


data_json['runes'][0]


# In[117]:


player_runes = {}

# Rune pas équipé
for rune in data_json['runes']:
    first_sub = 0
    first_sub_value = 0
    first_sub_grinded_value = 0
    second_sub = 0
    second_sub_value = 0
    second_sub_grinded_value = 0
    third_sub = 0
    third_sub_value = 0
    third_sub_grinded_value = 0
    fourth_sub = 0
    fourth_sub_value = 0
    fourth_sub_grinded_value = 0

    rune_id = rune['rune_id']
    rune_set = rune['set_id']
    rune_slot = rune['slot_no']
    rune_equiped = rune['occupied_id']
    stars = rune['class']
    level = rune['upgrade_curr']
    efficiency = 0
    max_efficiency = 0
    max_efficiency_reachable = 0
    gain = 0
    main_type = rune['pri_eff'][0]
    main_value = rune['pri_eff'][1]
    innate_type = rune['prefix_eff'][0]
    innate_value = rune['prefix_eff'][1]

    if level > 2:
        first_sub = rune['sec_eff'][0][0]
        first_sub_value = rune['sec_eff'][0][1]
        first_gemme_bool = rune['sec_eff'][0][2]
        first_sub_grinded_value = rune['sec_eff'][0][3]
    if level > 5:
        second_sub = rune['sec_eff'][1][0]
        second_sub_value = rune['sec_eff'][1][1]
        second_gemme_bool = rune['sec_eff'][1][2]
        second_sub_grinded_value = rune['sec_eff'][1][3]
    if level > 8:
        third_sub = rune['sec_eff'][2][0]
        third_sub_value = rune['sec_eff'][2][1]
        third_gemme_bool = rune['sec_eff'][2][2]
        third_sub_grinded_value = rune['sec_eff'][2][3]
    if level > 11:
        fourth_sub = rune['sec_eff'][3][0]
        fourth_sub_value = rune['sec_eff'][3][1]
        fourth_gemme_bool = rune['sec_eff'][3][2]
        fourth_sub_grinded_value = rune['sec_eff'][3][3]
    player_runes[rune_id] =  [rune_set, rune_slot, rune_equiped, stars, level, efficiency, max_efficiency,
                              max_efficiency_reachable, gain, main_type, main_value, innate_type, innate_value,
                              first_sub, first_sub_value, first_gemme_bool,  first_sub_grinded_value, second_sub, second_sub_value, second_gemme_bool,
                              second_sub_grinded_value, third_sub, third_sub_value, third_gemme_bool, third_sub_grinded_value, fourth_sub,
                              fourth_sub_value, fourth_gemme_bool, fourth_sub_grinded_value]

# Rune équipée
for unit in data_json['unit_list']:
    for stat in unit:
        if stat == "runes":
            for rune in unit[stat]:
                first_sub = 0
                first_sub_value = 0
                first_sub_grinded_value = 0
                second_sub = 0
                second_sub_value = 0
                second_sub_grinded_value = 0
                third_sub = 0
                third_sub_value = 0
                third_sub_grinded_value = 0
                fourth_sub = 0
                fourth_sub_value = 0
                fourth_sub_grinded_value = 0

                rune_id = rune['rune_id']
                rune_set = rune['set_id']
                rune_slot = rune['slot_no']
                rune_equiped = rune['occupied_id']
                stars = rune['class']
                level = rune['upgrade_curr']
                efficiency = 0
                max_efficiency = 0
                max_efficiency_reachable = 0
                gain = 0
                main_type = rune['pri_eff'][0]
                main_value = rune['pri_eff'][1]
                innate_type = rune['prefix_eff'][0]
                innate_value = rune['prefix_eff'][1]
                # rank = rune['extra']
                if level > 2:
                    first_sub = rune['sec_eff'][0][0]
                    first_sub_value = rune['sec_eff'][0][1]
                    first_gemme_bool = rune['sec_eff'][0][2]
                    first_sub_grinded_value = rune['sec_eff'][0][3]
                if level > 5:
                    second_sub = rune['sec_eff'][1][0]
                    second_sub_value = rune['sec_eff'][1][1]
                    second_gemme_bool = rune['sec_eff'][1][2]
                    second_sub_grinded_value = rune['sec_eff'][1][3]
                if level > 8:
                    third_sub = rune['sec_eff'][2][0]
                    third_sub_value = rune['sec_eff'][2][1]
                    third_gemme_bool = rune['sec_eff'][2][2]
                    third_sub_grinded_value = rune['sec_eff'][2][3]
                if level > 11:
                    fourth_sub = rune['sec_eff'][3][0]
                    fourth_sub_value = rune['sec_eff'][3][1]
                    fourth_gemme_bool = rune['sec_eff'][3][2]
                    fourth_sub_grinded_value = rune['sec_eff'][3][3]
                player_runes[rune_id] =  [rune_set, rune_slot, rune_equiped, stars, level, efficiency, max_efficiency,
                              max_efficiency_reachable, gain, main_type, main_value, innate_type, innate_value,
                              first_sub, first_sub_value, first_gemme_bool, first_sub_grinded_value, second_sub, second_sub_value, second_gemme_bool,
                              second_sub_grinded_value, third_sub, third_sub_value, third_gemme_bool, third_sub_grinded_value, fourth_sub,
                              fourth_sub_value, fourth_gemme_bool, fourth_sub_grinded_value]


# In[118]:


data = pd.DataFrame.from_dict(player_runes, orient="index", columns=['rune_set', 'rune_slot', 'rune_equiped', 'stars', 'level', 'efficiency', 'max_efficiency', 'max_efficiency_reachable', 'gain', 'main_type', 'main_value', 'innate_type',
                                                                     'innate_value','first_sub', 'first_sub_value', 'first_gemme_bool', 'first_sub_grinded_value', 'second_sub', 'second_sub_value', 'second_gemme_bool',
                              'second_sub_grinded_value', 'third_sub', 'third_sub_value', 'third_gemme_bool', 'third_sub_grinded_value', 'fourth_sub',
                              'fourth_sub_value', 'fourth_gemme_bool', 'fourth_sub_grinded_value'])
data


# # On supprime toute rune inférieure au level 11 ou 5 etoiles

# In[119]:


data = data[data['level'] > 11]
data = data[data['stars'] > 5]


# # Map des sets

# In[120]:


set = {1:"Energy", 2:"Guard", 3:"Swift", 4:"Blade", 5:"Rage", 6:"Focus", 7:"Endure", 8:"Fatal", 10:"Despair", 11:"Vampire", 13:"Violent",
        14:"Nemesis", 15:"Will", 16:"Shield", 17:"Revenge", 18:"Destroy", 19:"Fight", 20:"Determination", 21:"Enhance", 22:"Accuracy", 23:"Tolerance", 99:"Immemorial"}

data['rune_set'] = data['rune_set'].map(set)
data


# # Efficiency

# In[121]:


sub = {1: (375 * 5) * 2, # PV flat
       2: 8 * 5,  # PV%
       3: (20 * 5) * 2, #ATQ FLAT 
       4: 8 * 5, #ATQ%
       5:( 20 * 5) * 1, #DEF FLAT 
       6: 8 * 5,  # DEF %
       8: 6 * 5, # SPD
       9: 6 * 5, # CRIT
       10: 7 * 5, # DCC
       11: 8 * 5, # RES
       12: 8 * 5} # ACC

# Value max :
data['first_sub_value_max'] = data['first_sub'].map(sub)
data['second_sub_value_max'] = data['second_sub'].map(sub)
data['third_sub_value_max'] = data['third_sub'].map(sub)
data['fourth_sub_value_max'] = data['fourth_sub'].map(sub)
data['innate_value_max'] = data['innate_type'].replace(sub)


# Value stats de base + meule

data['first_sub_value_total'] = (data['first_sub_value'] + data['first_sub_grinded_value'])
data['second_sub_value_total'] = (data['second_sub_value'] + data['second_sub_grinded_value'])
data['third_sub_value_total'] = (data['third_sub_value'] + data['third_sub_grinded_value'])
data['fourth_sub_value_total'] = (data['fourth_sub_value'] + data['fourth_sub_grinded_value'])

data['efficiency'] = np.where(data['innate_type'] != 0, round(((1+data['innate_value'] / data['innate_value_max'] + data['first_sub_value_total'] / data['first_sub_value_max'] + data['second_sub_value_total'] / data['second_sub_value_max'] + data['third_sub_value_total'] / data['third_sub_value_max'] + data['fourth_sub_value_total'] / data['fourth_sub_value_max']) / 2.8)*100,2),
                              round(((1 + data['first_sub_value_total'] / data['first_sub_value_max'] + data['second_sub_value_total'] / data['second_sub_value_max'] + data['third_sub_value_total'] / data['third_sub_value_max'] + data['fourth_sub_value_total'] / data['fourth_sub_value_max']) / 2.8)*100,2))



# In[122]:


sub_max_lgd = {1:550, 2:10, 3:30, 4:10, 5:30, 6:10, 8:5}
sub_max_heroique = {1:450, 2:7, 3:22, 4:7, 5:22, 6:7, 8:4}


# Certaines stats ne sont pas meulables. On remplace donc le potentiel de meule par 0

dict = {'first_grind_value_max' : 'first_sub', 'second_grind_value_max' : 'second_sub', 'third_grind_value_max' : 'third_sub', 'fourth_grind_value_max' : 'fourth_sub'}

for key, value in dict.items():
       data[key + '_lgd'] = data[value].replace(sub_max_lgd)
       data[key + '_hero'] = data[value].replace(sub_max_heroique)
       
       # Certaines stats ne sont pas meulables. On remplace donc le potentiel de meule par 0
       
       data[key + "_lgd"] = np.where(data[value] > 8, 0,  data[key + "_lgd"])
       data[key + "_hero"] = np.where(data[value] > 8, 0, data[key + "_hero"]) 


# Value stats de base + meule (max)

data['first_sub_value_total_max_lgd'] = (data['first_sub_value'] + data['first_grind_value_max_lgd'])
data['second_sub_value_total_max_lgd'] = (data['second_sub_value'] + data['second_grind_value_max_lgd'])
data['third_sub_value_total_max_lgd'] = (data['third_sub_value'] + data['third_grind_value_max_lgd'])
data['fourth_sub_value_total_max_lgd'] = (data['fourth_sub_value'] + data['fourth_grind_value_max_lgd'])

data['first_sub_value_total_max_hero'] = (data['first_sub_value'] + data['first_grind_value_max_hero'])
data['second_sub_value_total_max_hero'] = (data['second_sub_value'] + data['second_grind_value_max_hero'])
data['third_sub_value_total_max_hero'] = (data['third_sub_value'] + data['third_grind_value_max_hero'])
data['fourth_sub_value_total_max_hero'] = (data['fourth_sub_value'] + data['fourth_grind_value_max_hero'])


# In[123]:


data['efficiency_max_lgd'] = np.where(data['innate_type'] != 0, round(((1+data['innate_value'] / data['innate_value_max'] + data['first_sub_value_total_max_lgd'] / data['first_sub_value_max'] + data['second_sub_value_total_max_lgd'] / data['second_sub_value_max'] + data['third_sub_value_total_max_lgd'] / data['third_sub_value_max'] + data['fourth_sub_value_total_max_lgd'] / data['fourth_sub_value_max']) / 2.8)*100,2),
                              round(((1 + data['first_sub_value_total_max_lgd'] / data['first_sub_value_max'] + data['second_sub_value_total_max_lgd'] / data['second_sub_value_max'] + data['third_sub_value_total_max_lgd'] / data['third_sub_value_max'] + data['fourth_sub_value_total_max_lgd'] / data['fourth_sub_value_max']) / 2.8)*100,2))

data['efficiency_max_hero'] = np.where(data['innate_type'] != 0, round(((1+data['innate_value'] / data['innate_value_max'] + data['first_sub_value_total_max_hero'] / data['first_sub_value_max'] + data['second_sub_value_total_max_hero'] / data['second_sub_value_max'] + data['third_sub_value_total_max_hero'] / data['third_sub_value_max'] + data['fourth_sub_value_total_max_hero'] / data['fourth_sub_value_max']) / 2.8)*100,2),
                              round(((1 + data['first_sub_value_total_max_hero'] / data['first_sub_value_max'] + data['second_sub_value_total_max_hero'] / data['second_sub_value_max'] + data['third_sub_value_total_max_hero'] / data['third_sub_value_max'] + data['fourth_sub_value_total_max_hero'] / data['fourth_sub_value_max']) / 2.8)*100,2))


# In[124]:


data['potentiel_max'] = data['efficiency_max_lgd'] - data['efficiency']


# Exemple d'une rune

# In[125]:


data.loc[22149241043]


# # On supprime les variables inutiles

# In[126]:


data.drop(['max_efficiency', 'max_efficiency_reachable', 'gain'], axis=1, inplace=True)


# # Map 
# ## Propriété
# Plus simple ici qu'avant

# In[127]:


property = {0:'Aucun', 
            1:'HP', 
            2:'HP%', 
            3:'ATQ', 
            4:'ATQ%', 
            5:'DEF', 
            6:'DEF%', 
            8:"SPD", 
            9:'CRIT', 
            10:'DCC', 
            11:'RES', 
            12:'ACC'}

for c in ['innate_type', 'first_sub', 'second_sub', 'third_sub', 'fourth_sub', 'main_type']:
    data[c] = data[c].map(property)
    
    


# ## Monstres

# In[128]:


data_mobs = pd.DataFrame.from_dict(data_json, orient="index").transpose()


# In[129]:


data_mobs = data_mobs['unit_list']


# In[130]:


# On va boucler et retenir ce qui nous intéresse..
list_mobs = []
data_mobs[0]
for monstre in data_mobs[0]:
    unit = monstre['unit_id']
    master_id = monstre['unit_master_id']
    list_mobs.append([unit, master_id])
    
# On met ça en dataframe    
df_mobs = pd.DataFrame(list_mobs, columns=['id_unit', 'id_monstre'])


# In[131]:


df_mobs


# Maintenant, on a besoin d'identifier les id.
# Pour cela, on va utiliser l'api de swarfarm

# In[ ]:





# In[132]:


# swarfarm_monstres() # à activer/désactiver pour maj 
swarfarm = pd.read_excel('swarfarm.xlsx')
swarfarm


# In[133]:


swarfarm = swarfarm[['com2us_id', 'name']].set_index('com2us_id')
df_mobs['name_monstre'] = df_mobs['id_monstre'].map(swarfarm.to_dict(orient="dict")['name'])


# In[134]:


df_mobs


# On peut faire le mapping...

# In[135]:


df_mobs = df_mobs[['id_unit', 'name_monstre']].set_index('id_unit')


# In[136]:


data['rune_equiped'] = data['rune_equiped'].replace(df_mobs.to_dict(orient="dict")['name_monstre'])


# # Indicateurs
# ## Runes +15

# In[137]:


data['indicateurs_level'] = (data['level'] == 15).astype('int') # Si 15 -> 1. Sinon 0


# # Amélioration des Grind

# In[138]:


dict = {'amelioration_first_grind' : ['first_sub_grinded_value', 'first_grind_value'],
        'amelioration_second_grind' : ['second_sub_grinded_value', 'second_grind_value'],
        'amelioration_third_grind' : ['third_sub_grinded_value', 'third_grind_value'],
        'amelioration_fourth_grind' : ['fourth_sub_grinded_value', 'fourth_grind_value']}

for key, value in dict.items():
    # Améliorable ? (valeur)
    data[key + '_lgd_value'] = data[value[1] + '_max_lgd'] - data[value[0]]
    data[key + '_hero_value'] = data[value[1] + '_max_hero'] - data[value[0]]
    # Améliorable ? (bool)
    data[key + '_lgd_ameliorable?'] = (data[key + '_lgd_value'] > 0).astype('int')
    data[key + '_hero_ameliorable?'] = (data[key + '_hero_value'] > 0).astype('int')


# # Commentaires

# In[139]:


# Level
data['Commentaires'] = np.where(data['level'] != 15, "A monter +15 \n", "")
data['Grind_lgd'] = ""
data['Grind_hero'] = ""


dict = {'amelioration_first_grind' : 'first_sub',
        'amelioration_second_grind' : 'second_sub',
        'amelioration_third_grind' : 'third_sub',
        'amelioration_fourth_grind' : 'fourth_sub'}

for key, value in dict.items():
    nom = key + "_lgd_value"
    data['Grind_lgd'] = np.where(data[key + '_lgd_ameliorable?'] == 1, data['Grind_lgd'] +  data[value] + "(" + data[nom].astype('str') + ") \n", data['Grind_lgd'])
    
    nom = key + "_hero_value"
    data['Grind_hero'] = np.where(data[key + '_hero_ameliorable?'] == 1, data['Grind_hero'] +  data[value] + "(" + data[nom].astype('str') + ") \n", data['Grind_hero'])


# # Clean du xl

# In[140]:


data.drop(['stars', 'level'], axis=1, inplace=True)

data_short = data[['rune_set', 'rune_slot', 'rune_equiped', 'efficiency', 'efficiency_max_hero', 'efficiency_max_lgd', 'potentiel_max', 'Grind_lgd', 'Grind_hero']]


# # Pour le fun
# ## Meules manquantes par stat

# In[141]:


property = {1:'HP', 
            2:'HP%', 
            3:'ATQ', 
            4:'ATQ%', 
            5:'DEF', 
            6:'DEF%', 
            8:"SPD"}

list_property_type = []
list_property_count = []


for propriete in property.values():
    count = data['Grind_hero'].str.count(propriete).sum()
    
    list_property_type.append(propriete)
    list_property_count.append(count)
    
    df_property = pd.DataFrame([list_property_type, list_property_count]).transpose()
    df_property = df_property.rename(columns={0:'Propriété', 1:'Meules manquantes pour atteindre la stat max'})
    


# In[142]:


# Graphique

fig = px.histogram(df_property, x='Propriété', y='Meules manquantes pour atteindre la stat max', color='Propriété', title="Meules manquantes pour atteindre la stat max", text_auto=True)
fig.write_image('resultaT/Meules_manquantes_par_stat.png')


# ## Meules manquantes par set

# In[143]:


pd.options.display.max_rows = 200  # retour à 5 pour éviter de surcharger la suite
dict_rune = {}
list_type = []
list_count = []
list_propriete = []

for type_rune in set.values():
    for propriete in property.values():
        data_type_rune = data[data['rune_set'] == type_rune]
        nb_rune = data[data['rune_set'] == type_rune].count().max()
        count = data_type_rune['Grind_hero'].str.count(propriete).sum()
        
        dict_rune[type_rune] = nb_rune
        
        list_type.append(type_rune)
        list_count.append(count)
        list_propriete.append(propriete)
        
        
        # if propriete == "HP":
        #     print(f'Tu as {nb_rune} runes du set {type_rune}')
        # print(f'{type_rune} : Il manque {count} heroique pour totalement grind au max la stat {propriete}')
        
        df_rune = pd.DataFrame.from_dict(dict_rune, orient='index', columns=['Nombre de runes'])


# In[144]:


df_count = pd.DataFrame([list_type, list_propriete, list_count]).transpose()
df_count = df_count.rename(columns={0:'Set', 1:'Propriété', 2:'Meules manquantes pour la stat max'})


# In[145]:


df_count


# In[146]:


# Graphique
fig = px.histogram(df_count, x='Set', y='Meules manquantes pour la stat max', color='Propriété', title="Meules manquantes pour la stat max", text_auto=True)
fig.write_image('resultat/Meules_manquantes par rune et propriété.png')


# # Export

# In[147]:


export_excel(data, data_short, df_rune, df_count)

