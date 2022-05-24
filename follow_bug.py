# %% [markdown]
# ### First Follow

# %%
import os
import pandas as pd
import numpy as np

# %%
def checar_dictionario(key, dict):
    check = key in dict
    if check:
        if len(dict[key])>0:
            return True
    return False

# %%


# %%
file_path = "lib/input/"

try:
    file_name = file_name_externo
except:
    file_name = "input_b.txt"
# file_name = "example_1.txt"
try:
    codigo_entrada = open(file_path + file_name, "r", encoding="utf8").read()
except:
    codigo_entrada = """S -> aSbc | D
D -> dD | d"""

# %%
simbolo_inicial = codigo_entrada[0]

# %%
import re

# %%
qtd_linhas = codigo_entrada.count("\n") + 1
qtd_linhas

# %%
### Encontrar
regex_terminais = r"[a-z+:=*-/]"
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
follow_dict = production.copy()
follow_position = production.copy()
for elem in first_dict:
    first_dict[elem] = []
    follow_dict[elem] = []
    follow_position[elem] = []

# %%
production

# %%
first_dict

# %%
follow_dict

# %%
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

    if len(key) == 1 and key in variaveis_nao_terminais:
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


# %%
for variavel in production:
    variavel_da_vez = variavel
    first_set(variavel)

# %%
production

# %%
follow_dict

# %%
def follow_set(key):
  resultado = []
  ### Achar elemento que contem key
  for chave, valor in production.items():
    for elem in valor:
      saida = []
      if key == simbolo_inicial:
          saida = "$"
      if key in elem:
        ### Achou elemento que possui a key     
        ### Se elemento estiver na posição final    
        indice = elem.index(key)

        palavra_restante = elem[indice + 1:]

        if palavra_restante == '':
            
          if checar_dictionario(chave,follow_dict):
                saida = follow_dict[chave]
          else:
            if key == chave:
                saida = [] 
            else:
                saida = follow_set(chave)
        else:
            if checar_dictionario(palavra_restante,first_dict):
                saida = first_dict[palavra_restante]
            else:
                saida = first_set(palavra_restante)


      resultado = merge_lists(resultado,saida)     
      if 'λ' in resultado: 
          resultado.remove('λ')
          resultado = merge_lists(resultado,follow_set(chave))
           

  follow_dict[key] = resultado
  
  return resultado
  
print("Inicio do Follow")
variavel_da_vez = 'S'
follow_set(variavel_da_vez)

variavel_da_vez = 'A'
follow_set(variavel_da_vez)




# %%
### Remover chaves de tamanho maior que um

lista_chaves_desnecessarias = [key for key in first_dict if len(key) > 1 or key in variaveis_terminais]
[first_dict.pop(key) for key in lista_chaves_desnecessarias]


# %%
df = pd.DataFrame(columns=['Variavel', 'Producao', 'First', 'Follow'])

# %%
df["Variavel"] = variaveis_nao_terminais

# %%
def listToString(list):
    str = '{'
    for elem in list:
        str = str + elem + ','

    str = str[:-1] + '}'
    return str


# %%
for key, value in production.items():
    df.loc[df['Variavel'] == key, 'Producao'] = listToString(value)

# %%
for key, value in first_dict.items():
    df.loc[df['Variavel'] == key, 'First'] = listToString(value)

# %%
for key, value in follow_dict.items():
    df.loc[df['Variavel'] == key, 'Follow'] = listToString(value)

# %%
df

# %%
nome_arquivo_saida = f'lib/output/{file_name[:-3]}csv'
try:
    df.to_csv(nome_arquivo_saida, index = False)
except:
    print("Não pode salvar aquivo de saída")

# %%



