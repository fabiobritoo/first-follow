# %% [markdown]
# ### First Follow

# %%
import os
import pandas as pd
import numpy as np

# %%
file_path = "lib/input/"
file_name = "input_4.txt"
try:
    codigo_entrada = open(file_path + file_name, "r", encoding="utf8").read()
except:
    codigo_entrada = """S -> aSbc | D
D -> dD | d"""

# %%
print(codigo_entrada)

# %%
import re

# %%
qtd_linhas = codigo_entrada.count("\n") + 1
qtd_linhas

# %%
### Encontrar
regex_terminais = r"[a-z+:=*-]"
matches = re.finditer(regex_terminais, codigo_entrada.replace("->"," "), re.MULTILINE)
variaveis = []
for match in matches:
    variaveis.append(match.group())

variaveis_terminais = list(set(variaveis))

variaveis_terminais

# %%
regex_nao_terminais = r"[A-Z]"
matches = re.finditer(regex_nao_terminais, codigo_entrada.replace("->"," "), re.MULTILINE)
variaveis = []
for match in matches:
    variaveis.append(match.group())

variaveis_nao_terminais = list(set(variaveis))
variaveis_nao_terminais

# %%
print(codigo_entrada)

# %%
production = dict()

# %%

for line in codigo_entrada.splitlines():
    left = line.split('->')[0].strip() 
    right = line.split('->')[1].strip()

    print(f"FIRST({left}) = ", end="")
    right
    production[left] = []

    for idx, right_part  in enumerate(right.split("|")): 
 
        production[left].append(right_part.strip())
        if idx > 0:
            print(f" + FIRST({right_part.strip()})", end="")
        else:
            print(f"FIRST({right_part.strip()})", end="")        

    print("")



# %%
production

# %%
## Criar dicionário de first
first_dict = production.copy()
for elem in first_dict:
    first_dict[elem] = []

# %%
production

# %%
first_dict

def merge_lists(elem1, elem2):
    if type(elem1 != list):
        elem1 = list(elem1)
    if type(elem2 != list):
        elem2 = list(elem2)
    return list(set(elem1 + elem2))

# %%
def first_set(key):
    ### Checar se já existe no dicionário 

    resultado = []

    if len(key) == 1:
        if (len(first_dict[key]) != 0):
            return first_dict[key]
            
        value = production[key]
    else:
        value = [key]  

    for elem in value:

        if (len(elem) == 1 and elem == key):
            saida = []
        if elem == 'λ':
            saida = 'λ'
        if elem[0] in variaveis_terminais:
            saida = elem[0]
        if elem[0] in variaveis_nao_terminais:
            if (len(first_dict[elem[0]]) != 0 ):
                check = first_dict[elem[0]]
            else:
                check = first_set(elem[0])
            ### CHecar se o first já foi calculado FIRST T
            if 'λ' not in check:
                saida = first_dict[elem[0]]
            else:       
                if(len(elem) > 1):
                    lista_sem_vazio =  [value for value in first_dict[elem[0]] if value != 'λ']
                    
                    if (elem[1:] == variavel_da_vez):
                        saida = lista_sem_vazio
                    else:
                        # saida = lista_sem_vazio.append(first_set(elem[1:]))
                        saida = merge_lists(lista_sem_vazio, first_set(elem[1:]))
                else:
                    saida = first_dict[elem[0]]
        
        # resultado.append(saida)
        resultado = merge_lists(resultado,saida)
    first_dict[key] = resultado
    return resultado

print("INICIO")
variavel_da_vez = 'Z'
first_set('Z')
variavel_da_vez = 'Y'
first_set('Y')
variavel_da_vez = 'T'
first_set('T')
variavel_da_vez = 'X'
first_set('X')
# %%



