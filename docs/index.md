# Documentação das funções e processos utilizados no decorrer do desenvolvimento

## Funções

As funções se encontram dentro da pasta `scripts` e são divididas em 3 arquivos:

- `google_scrapper.py`: contém funções que são utilizadas para fazer o scrapping da correção de texto sugerida pelo Google.
- `preprocess_qd.py`: contém funções que são utilizadas para fazer a limpeza nos trechos que e o pipeline de pré-processamento dos trechos do QD.
- `multiprocess_request.py`: contém funções que são utilizadas para fazer o scrapping de forma paralela.

### Funções de limpeza

As funções de limpeza são utilizadas para fazer a limpeza dos trechos que serão utilizados para o modelo.

#### cleaning_text

Principais funções:

- preprocess
  - esta função recebe o parâmetro text, que deve ser um trecho e faz o uso de uma série de outras funções para deixar o texto mais bem formatado corrigindo possíveis erros.

```python

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
```

- find_dashes_and_replace_words

```python
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
```

- clean_text

```python
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
```

- pipeline_multiprocess

```python

def pipeline_multiprocess(df:pd.DataFrame) -> None:
    date = datetime.datetime.now().strftime("%d%m%Y%H:%M")

    df_unique_texts = deepcopy(df.drop_duplicates(subset=['excerpt']))

    logging.basicConfig(filename=f'QD-scrap_google-{date}.log',
                        level=logging.INFO)

    df_ptbr = read_dicionario_br()

    df_unique_texts['cleaned_text'] = df_unique_texts['excerpt'].map(preprocess)
    df_unique_texts['cleaned_text'] = df_unique_texts['cleaned_text'].apply(lambda txt:
                                         find_dashes_and_replace_words(txt,
                                                                       df_ptbr)
                                             )


    unique_text_list = df_unique_texts['cleaned_text'].unique()

    clean_and_save(unique_text_list)

    return df_unique_texts
```
