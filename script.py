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
production

# %%
produz_vazio = []

for line in codigo_entrada.splitlines():
    left = line.split('->')[0].strip() 
    right = line.split('->')[1].strip()

    print(f"FIRST({left}) = ", end="")
    right
    production[left] = right

    for idx, right_part  in enumerate(right.split("|")): 

        if(right_part.strip() == "λ"): ## Guardar quando o elemento produz vazio
            produz_vazio.append(left) 

        if idx > 0:
            print(f" + FIRST({right_part.strip()})", end="")
        else:
            print(f"FIRST({right_part.strip()})", end="")        

    print("")

produz_vazio = list(set(produz_vazio))

# %%
def first_set(value):        
    print(f"FIRST({value})")
    if value == prod:
        return ""
    if value == "λ":
        return "λ"
    if value in variaveis_nao_terminais:
        first_set(production[value])
    elif value[0] in variaveis_terminais:
        return value[0]
    elif value[0] in variaveis_nao_terminais:        
        if "λ" not in first_set(value[0]):
            return first_set(value[0])
        else:
            return first_set(value[0]).replace("λ","") + first_set(value[1:])
        
    return 1

# %%
dict_first = dict()
for prod in production:
    print(f"FIRST({prod}) = ", end="")
    right_list = production[prod].split("|")
    right_list = [elem.strip() for elem in right_list]

    dict_first[prod] = []

    for value in right_list:    
        dict_first[prod].append(first_set(value))
    
