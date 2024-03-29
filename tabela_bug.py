# %% [markdown]
# ### First Follow

# %%
import os
import pandas as pd
import numpy as np

# %% [markdown]
# ## Funções Auxiliares

# %%
def checar_dictionario(key, dict):
    check = key in dict
    if check:
        if len(dict[key])>0:
            return True
    return False

def print_dict(dictionary):
    for key, value in dictionary.items():
        print(key + " : " + listToString(value))

def merge_lists(elem1, elem2):
    if type(elem1 != list):
        elem1 = list(elem1)
    if type(elem2 != list):
        elem2 = list(elem2)
    return list(set(elem1 + elem2))

def listToString(list):
    str = '{'
    for elem in list:
        str = str + elem + ','

    str = str[:-1] + '}'
    return str

def juntar_lista(lista):
    saida = ''
    for elem in lista:
        saida = saida + elem
    return saida


# %%
file_path = "lib/input/productions/"

try:
    file_name = file_name_externo
except:
    file_name = "exemplo3.txt"
try:
    codigo_entrada = open(file_path + file_name, "r", encoding="utf8").read()
except:
    codigo_entrada = """S -> aSbc | D
D -> dD | d"""

# %%
simbolo_inicial = codigo_entrada[0]

# %%
codigo_entrada = codigo_entrada.replace('id','i')
codigo_entrada = codigo_entrada.replace('num','n')
codigo_entrada = codigo_entrada.replace(':=','=')

# %%
import re

# %%
qtd_linhas = codigo_entrada.count("\n") + 1
qtd_linhas

# %%
### Encontrar
regex_terminais = r"[\[\]\(\)a-z+:=*-/;]"
matches = re.finditer(regex_terminais, codigo_entrada.replace("->"," "), re.MULTILINE)
variaveis_terminais = []
for match in matches:
    variaveis_terminais.append(match.group())

variaveis_terminais = list(dict.fromkeys(variaveis_terminais))


# %%
### Adicionar num
cond_num_1 = 'n' in variaveis_terminais
cond_num_2 = 'u' in variaveis_terminais
cond_num_3 = 'm' in variaveis_terminais

if (cond_num_1 and cond_num_2 and cond_num_3):
    variaveis_terminais.remove('n')
    variaveis_terminais.remove('u')
    variaveis_terminais.remove('m')
    variaveis_terminais.append('n')

### Adicionar id
cond_id_1 = 'i' in variaveis_terminais
cond_id_2 = 'd' in variaveis_terminais

if (cond_id_1 and cond_id_2):
    variaveis_terminais.remove('i')
    variaveis_terminais.remove('d')
    variaveis_terminais.append('i')

### Adicionar :=
cond_ponto_1 = ':' in variaveis_terminais
cond_ponto_2 = '=' in variaveis_terminais

if (cond_ponto_1 and cond_ponto_2):
    variaveis_terminais.remove(':')
    variaveis_terminais.remove('=')
    variaveis_terminais.append('=')

# %%
variaveis_terminais

# %%
variaveis_terminais

# %%
# regex_nao_terminais = r"[A-Z]"
regex_nao_terminais = r".+?(?=->)"
matches = re.finditer(regex_nao_terminais, codigo_entrada, re.MULTILINE)
variaveis_nao_terminais = []
for match in matches:
    variaveis_nao_terminais.append(match.group().strip())

variaveis_nao_terminais
# variaveis_nao_terminais = list(dict.fromkeys(variaveis_nao_terminais))

# %%
variaveis_nao_terminais

# %%
variaveis_nao_terminais

# %%
production = dict()

# %%

for line in codigo_entrada.splitlines():
    left = line.split('->')[0].strip() 
    right = line.split('->')[1].strip()
    production[left] = []

    for idx, right_part  in enumerate(right.split("|")):  
        production[left].append(right_part.strip())

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
lista_first_por_elem = []

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
        saida = []
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
        lista_first_por_elem.append([key,elem,saida])
      
    first_dict[key] = resultado
    return resultado


# %%
for variavel in production:
    variavel_da_vez = variavel
    try:
        first_set(variavel)
    except Exception as e:
        print("Erro First: ", e)
        print("Variável: ", variavel_da_vez)


# %%
production

# %%
follow_dict

# %%
lista_follow_por_elem = []

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
                if key == simbolo_inicial:
                    saida = '$'
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
           

  follow_dict[key] = resultado
  lista_follow_por_elem.append([key,elem,saida])
  
  return resultado

# %%
for variavel in production:
    variavel_da_vez = variavel
    try:
        follow_set(variavel)
    except Exception as e:
        print("Erro Follow: ", e)
        print("Variável: ", variavel_da_vez)

# %%
### Remover chaves de tamanho maior que um

lista_chaves_desnecessarias = [key for key in first_dict if len(key) > 1 or key in variaveis_terminais]
[first_dict.pop(key) for key in lista_chaves_desnecessarias]


# %%
df = pd.DataFrame(columns=['Variavel', 'Producao', 'First', 'Follow'])

# %%
df["Variavel"] = variaveis_nao_terminais

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
nome_arquivo_saida = f'lib/output/first_follow/{file_name[:-3]}csv'
try:
    df.to_csv(nome_arquivo_saida, index = False)
except:
    print("Não pode salvar aquivo de saída")

# %%
df

# %% [markdown]
# #### Primeira Tabela Resultante

# %%
colunas = variaveis_terminais.copy()
colunas.insert(0,'M(V,T)')

# %%
df_1 = pd.DataFrame(columns=colunas)
df_1['M(V,T)'] = variaveis_nao_terminais
df_1.index = df_1['M(V,T)']

# %%
print('Produção:')
print_dict(production)

# %%
### Todos as produções vão para seu FIRST
### As Vazio vão para o follow

# %%
### Tratar casos onde a produção é vazia -> Usar elementos do follow
lista_ajustes = []

for row in lista_first_por_elem:
    if 'λ' in row[1]:
        lista_follow = follow_set(row[0])
        lista_follow = [elem for elem in lista_follow if elem not in first_dict[row[0]]]
        lista = merge_lists(row[2],lista_follow)        
        row[2] = [elem for elem in lista if elem != 'λ']
    else:
        if 'λ' in row[2]:
            lista_follow = follow_set(row[0])
            lista_follow = [elem for elem in lista_follow if elem not in first_dict[row[0]]]
            lista = merge_lists(row[2],lista_follow)        
            row[2] = [elem for elem in lista if elem != 'λ']
            lista_ajustes.append([row[0],row[2]])
        

### Eliminar Variaves Não Terminais Erradas

lista_table = [elem for elem in lista_first_por_elem if elem[0] in variaveis_nao_terminais]
lista_ajustes = [elem for elem in lista_ajustes if elem[0] in variaveis_nao_terminais]

# %%
### Tentando deixar como prioridade os elementos que geram vazio

dicionario_ajustes = dict(lista_ajustes)

for elem in lista_table:
    for coluna in elem[2]:
        if elem[0] in dicionario_ajustes.keys():
            if elem[2] != dicionario_ajustes[elem[0]]:
                [elem[2].remove(remov) for remov in elem[2] if remov in dicionario_ajustes[elem[0]]] 

# %%
## Adicionando elementos na tabela

for elem in lista_table:
    for coluna in elem[2]:
        df_1.loc[elem[0], coluna] = elem[0] + "->" + elem[1]
    

# %%
### Formatar

df_1 = df_1.fillna('-')
df_1

# %%
nome_arquivo_saida = f'lib/output/predictive_table/{file_name[:-3]}csv'
try:
    df_1.to_csv(nome_arquivo_saida, index = False)
    print('Tabela Preditiva Gerada')
except:
    print("Não pode salvar aquivo de saída")

# %%
alfabeto = merge_lists(df_1.index,df_1.columns)
alfabeto = merge_lists(alfabeto,'$') 

# %%
#### Tabela de Verificação
palavra = 'x + x * x'
palavra = palavra.replace(" ","")

file_path_test = "lib/input/test_words/"

try:
    palavra = open(file_path_test + file_name, "r", encoding="utf8").read()
    palavra = palavra.replace(" ","")
except:
    palavra = """aab"""


# %%
mensagem = ''
palavra = 'a'
# %%

df_2 = pd.DataFrame(columns=['Pilha','Entrada','Producao'])

lista_pilha= ['$']
lista_entrada = ['$']

df_2.loc[0] = [juntar_lista(lista_pilha),juntar_lista(lista_entrada),simbolo_inicial]


### Colocar Produção da linha passada na pilha
producao = simbolo_inicial
eliminado = lista_pilha[-1]

nova_entrada = palavra
[lista_entrada.insert(len(lista_entrada) - 1, elem) for elem in nova_entrada]


for i in range(1,50):

    nova_pilha = producao.split('->')[-1].replace(" ","") 

    if nova_pilha == 'λ':
        nova_pilha = ''

    [lista_pilha.insert(len(lista_pilha), elem) for elem in nova_pilha[::-1]]    

    if len(lista_pilha) == 0:
        break

    elemento_analisado = lista_pilha[-1]
    elemento_entrada = lista_entrada[0]

    if elemento_entrada not in alfabeto:
        mensagem = 'Elemento não corresponde ao Alfabeto'
        print(mensagem)
        break

    pop_entrada = False
    if (elemento_analisado == elemento_entrada): 
        pop_entrada = True    
        elemento_entrada = lista_entrada[0]
        if elemento_analisado in variaveis_nao_terminais:        
            producao = df_1.loc[elemento_analisado][elemento_entrada]
        else:
            producao = ''    
    else:
        if (elemento_analisado in variaveis_nao_terminais):
           producao = df_1.loc[elemento_analisado][elemento_entrada]
        else:
            df_2.loc[i] = [juntar_lista(lista_pilha),juntar_lista(lista_entrada),producao]
            mensagem = "Não foi possível realizar a palavra, pilha não possui não-terminais"
            print(mensagem)
            break
        if (len(producao) == 1):
            df_2.loc[i] = [juntar_lista(lista_pilha),juntar_lista(lista_entrada),producao]
            mensagem = "Não foi possível realizar a palavra, não há producão que gere entrada"
            print(mensagem)
            break

    df_2.loc[i] = [juntar_lista(lista_pilha),juntar_lista(lista_entrada),producao]

    if pop_entrada: lista_entrada.pop(0)
    eliminado = lista_pilha.pop()

df_2

# %%
nome_arquivo_saida = f'lib/output/test_table/{file_name[:-3]}csv'
try:
    df_2.to_csv(nome_arquivo_saida, index = False)
    print('Tabela de Testes Gerada')
except:
    print("Não pode salvar aquivo de saída")

# %%
### Gerar documento de saida (Apenas para a versão total)

# %%
if file_name == 'input_c.txt':

    codigo_entrada = codigo_entrada.replace('i','id')
    codigo_entrada = codigo_entrada.replace('n','num')
    codigo_entrada = codigo_entrada.replace('=',':=')

    df = df.applymap(lambda x: x.replace('i','id'))
    df = df.applymap(lambda x: x.replace('n','num'))
    df = df.applymap(lambda x: x.replace('=',':='))

    df_1 = df_1.applymap(lambda x: x.replace('i','id'))
    df_1 = df_1.applymap(lambda x: x.replace('n','num'))
    df_1 = df_1.applymap(lambda x: x.replace('=',':='))

    df_2 = df_2.applymap(lambda x: x.replace('i','id'))
    df_2 = df_2.applymap(lambda x: x.replace('n','num'))
    df_2 = df_2.applymap(lambda x: x.replace('=',':='))

# %%
try:
    doc.add_heading(f'Arquivo: {file_name}', 1)
    doc.add_heading(f'Entrada de Dados', 3)
    doc.add_paragraph(f'Codigo do arquivo:')

    doc.add_paragraph(f'{codigo_entrada}')

    doc.add_heading('Tabela First - Follow', 3)
    criar_tabela(df)

    doc.add_heading('Tabela Preditiva', 3)
    criar_tabela(df_1)

    doc.add_heading('Tabela Teste', 3)
    doc.add_paragraph(f'Palavra de teste: {palavra}')
    criar_tabela(df_2)
    doc.add_paragraph(f'{mensagem}')
except:
    pass



# %%


# %%



