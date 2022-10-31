#preprocessing.py
import pandas as pd
import re
from unidecode import unidecode
import logging
import datetime
from copy import deepcopy
from google_scrapper import fix_spelling_in_answer

def remove_dash_n(text):
    return text.replace('/n', ' ')

def remove_spaces(text):
    return re.sub(r"\s+", " ", text).strip()

def remove_lots_of_points(text):
    return re.sub('\.{2,}', ' ', text)

def remove_bad_chars(text):
    return re.sub('[˜˚˝˙ˆˇ˚˘˘Œ˛œ_%ﬁﬂ‡š<>›„’]', ' ', text)

def spaced_letters(text):
    text = text.replace('A P O S E N T A R', ' aposentar ')
    return text

def join_words(text):
    # Há muitas palavras assim: "res - ponsável"
    # Vou ter algum problema juntando coisa que não devia
    # Espero que nesses casos o tokenizer resolva
    return re.sub(' - ?', '', text)

def separate_words(text):
    # Há muitas palavras assim: "FerrazPresidente" "FerrazAPresidente"
    # Vou supor que sempre que houver uma letra minúscula seguida de maiúscula é para separar
    text = re.sub('(?<=[a-záàâãéêíóôõú])(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚ])', ' ', text)
    text = re.sub('(?<=[ÓA-ZÁÀÂÃÉÊÍÓÔÕÚ])(?=[ÓA-ZÁÀÂÃÉÊÍÓÔÕÚ][a-záàâãéêíóôõú])', ' ', text)
    return text

def dots_that_mess_segmentation(text):
    text = re.sub('sec\.', 'Sec ', text, flags=re.IGNORECASE)
    text = re.sub('av\.', 'Avenida ', text, flags=re.IGNORECASE)
    text = re.sub('min\.', 'Ministro ', text, flags=re.IGNORECASE)
    text = re.sub('exmo\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('sr\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('dr\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('sra\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('proc\.', ' processo ', text, flags=re.IGNORECASE)
    text = re.sub('reg\.', ' registro ', text, flags=re.IGNORECASE)
    text = re.sub('func\.', ' funcionário ', text, flags=re.IGNORECASE)
    text = re.sub('art\.', ' artigo ', text, flags=re.IGNORECASE)
    text = re.sub('inc\.', ' inciso ', text, flags=re.IGNORECASE)
    text = re.sub('(?<=[ \.][A-Z])\.', ' ', text)
    text = re.sub('(?<=comp)\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('(?<=insc)\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('p[áa]g[\. ]', ' página ', text, flags=re.IGNORECASE) #Pág. N 5
    text = re.sub('\. *(n|n[uú]mero)[ \.°º]+', ' número ', text, flags=re.IGNORECASE) #. N°
    
    return text

def preprocess(text):
    text = remove_special_characters(text)
    text = remove_dash_n(text)
    text = remove_lots_of_points(text)
    text = remove_bad_chars(text)
    text = spaced_letters(text)
    text = dots_that_mess_segmentation(text)
    text = remove_spaces(text)
    text = join_words(text)
    text = separate_words(text)
    text = remove_page_breaker(text)
    text = remove_special_characters(text)
    
    return text


def replaces(text):
    #tokenizador separa essas palavras em 3 tokens
    text = re.sub('teresina', 'cidade', text) 
    text = re.sub('piauí', 'estado', text)
    text = re.sub('c/c', 'concomitante', text)
    return text

#my functions
def remove_special_characters(text:str):
    text = text.replace("<__", "").replace("__>", "")
    text = text.replace("- -", "-")
    text = text.replace(" - ", "-")
    text = text.replace("  ", " ")
    text = text.replace("- ", "-")
    text = text.replace(" -", "-")
    
    return text

def remove_page_breaker(text:str) -> str:
    return text.replace("\n", " ").strip()

def find_occurrences(text:str, 
                     character:str) -> list:
    return [i for i, letter in enumerate(text) if letter == character]

def get_whole_words(subtext:str) -> str:
    spaces_indexes = find_occurrences(subtext, " ")
    first_pos=spaces_indexes[0]
    last_pos=spaces_indexes[-1]
    
    #pega entre o primeiro e o ultimo espaço
    #para não pegar palavras pela metade
    return (subtext[first_pos:
                    last_pos],
            first_pos,
            last_pos)

def contains_number(word):
    return bool(re.search(r'\d', word))

def find_dashes_and_replace_words(text:str,
                                  df_ptbr:pd.DataFrame) -> str:
    dashes_indexes = find_occurrences(text, "-")
    spaces_indexes = find_occurrences(text, " ")
#    words = df_ptbr['Word'].map(lambda w: unidecode(w.lower())).unique()#unidecode
    words = df_ptbr['Word'].map(lambda w: w.lower()).unique()#unidecode

    for dash in dashes_indexes:
        try:
            space_before=max([elem for elem in spaces_indexes if elem < dash])
        except:
            space_before=0
        
        try:
            space_after= min([elem for elem in spaces_indexes if elem > dash])
        except:
            space_after=len(text)

        new_word=text[space_before:space_after]
        new_word=new_word.replace('-', '')

        new_word_cleaned = (new_word.
                                    lower().
                                    strip().
                                    replace('.', '').
                                    replace(',', '').
                                    replace(':', '').
                                    replace(';', '').
                                    replace(')', '').
                                    replace('(', '').
                                    replace('[', '').
                                    replace(']', ''))
        if not(contains_number(word=new_word)):        
            if new_word_cleaned in words:
                text = ''.join([text[:space_before], 
                                new_word,
                                text[space_after:]])

    return text





def clean_text(text:str,
               window_size:int=50,
               time_between_queries:int=3) -> str:
    inicio = datetime.datetime.now()#.strftime("%Y%m%d%H:%M:%S")
    logging.info(f"TEXTO INICIAL {inicio.strftime('%Y%m%d%H:%M:%S')} -> {text}")
    dash_indexes = find_occurrences(text, "-")
    if dash_indexes:
        final_text=''
        dash_indexes_size = len(dash_indexes)
        for i in range(0, dash_indexes_size):

            start_dash_position = dash_indexes[i]-window_size
            end_dash_position = dash_indexes[i]+window_size

            if start_dash_position < 0:
                start_dash_position=0 #pegar inicio do texto caso o intervalo de contexto esteja antes da posição 0

            if i==0:
                last_position=0
                start_dash_position=0
            else:
                last_position=dash_indexes[i]
                if start_dash_position < (dash_indexes[i-1]+window_size):
                    start_dash_position= last_space_position#dash_indexes[i-1]+window_size

            subtext = text[start_dash_position:
                           end_dash_position]

            subtext, first_space_position, last_space_position = get_whole_words(subtext=subtext)

            first_space_position+=start_dash_position#(last_position)
            last_space_position+=start_dash_position#last_position

            subtext = fix_spelling_in_answer(subtext)[0] #aqui entra a validação no google

            first_fragment = text[start_dash_position:
                                  first_space_position]

            if i==(dash_indexes_size-1):
                last_fragment = text[last_space_position:]
            else:
                next_dash_position = dash_indexes[i+1]-window_size

                last_fragment = text[last_space_position:
                                     next_dash_position]

            final_text += " ".join([first_fragment,
                                    subtext,
                                    last_fragment])
            final_text = final_text.replace("  ", " ")
    else:
        final_text=text
        
    final = datetime.datetime.now()
    logging.info(f"TEXTO FINAL {final.strftime('%Y%m%d%H:%M:%S')} -> {final_text}")
    logging.info(f"TEMPO DE PROCESSAMENTO -> {(final-inicio).total_seconds()}")
    
    return final_text

def read_dicionario_br() -> pd.DataFrame:
    #obtendo palavras do portugues brasileiro
    url = 'https://drive.google.com/file/d/1tUDeEyH6vonx-ctxeGVWG6gh4knP1Igi/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    header_list = ['Word']
    df_ptbr = pd.read_csv(path, 
                        skiprows=0,
                        names=header_list,
                        header=None,
                        sep=',')
    
    #Pendente: localizar a função que implementei tratando o "- " e validando no 'ptbr'.
    return df_ptbr

def clean_and_save(text_list:list) -> None:
    with open("de-para.csv", "w",encoding = 'utf-8') as f:
        for text in text_list:
            new_text = clean_text(text)
            f.write(f'{text}\t{new_text}\n')
    print("DONE!")    

def pipeline(df_path:str='dataset-tecnologias-educacao.csv') -> None:
    date = datetime.datetime.now().strftime("%d%m%Y%H:%M")

    logging.basicConfig(filename=f'QD-scrap_google-{date}.log',
                        level=logging.INFO)
    df = pd.read_csv(df_path)

    df['cleaned_text'] = df['excerpt'].map(preprocess)
    df['cleaned_text'] = df['cleaned_text'].apply(lambda txt:
                                         find_dashes_and_replace_words(txt, 
                                                                       df_ptbr)
                                             )
    df_ptbr = read_dicionario_br()

    unique_text_list = df['cleaned_text'].unique()

    clean_and_save(unique_text_list)