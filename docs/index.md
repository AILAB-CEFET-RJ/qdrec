# Documentação das funções e processos utilizados no decorrer do desenvolvimento

## Funções

As funções se encontram dentro da pasta `scripts` e são divididas em 3 arquivos:

- `google_scrapper.py`: contém funções que são utilizadas para fazer o scrapping da correção de texto sugerida pelo Google.
- `preprocess_qd.py`: contém funções que são utilizadas para fazer a limpeza nos trechos que e o pipeline de pré-processamento dos trechos do QD.
- `multiprocess_request.py`: contém funções que são utilizadas para fazer o scrapping de forma paralela.

### Funções de pré-processamento (limpeza)

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
  Esta função é utilizada ainda durante o período de pré-processamento após a correção da frase via google_scraper.

  Ela é feita como um processo de tratamento para os casos que o Google "não conseguiu corrigir". A função faz isso selecionando a palavra com hífen, removendo o hífen e verificando se essa nova palavra gerada existe na língua portuguesa. Para essa verificação é utilizado um arquivo que possui as palavras da língua portuguesa.

```python
def find_dashes_and_replace_words(text:str,
                                  df_ptbr:pd.DataFrame) -> str:
    dashes_indexes = find_occurrences(text, "-")
    spaces_indexes = find_occurrences(text, " ")

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
  Esta função é utilizada no momento de pré-processamento após a correção via google_scrapper.

  Sucintamente, o objetivo desta função é:

  - 1. identificar a ocorrência de "-" (hífens) no texto, que é onde o nosso problema a ser solucionado ocorre;
  - 2. dar um contexto à nossa palavra problemática, selecionando n caracteres anteriores e n caracteres posteriores;
  - 3. enviar essa frase de contexto para o google como pesquisa;
  - 4. retornar a frase corrigida baseada na sugestão do google.

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
  Esta etapa consiste em orquestrar todas as funções de pré-processamento e de forma paralelizada.

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

#### Funções de scraping google

- clean_text
  Esta função se baseia em receber como parâmetro uma frase (preferivelmente que possua erro ortográfico), efetuar uma pesquisa no google por meio de request e retornar a sugestão de correção do erro ortográfico.

````python
def send_query(query):
    while True:
        url = "https://www.google.com.br/search?q={}".format(query)

        headers = {'User-agent': 'your bot 0.1',
                   'proxy': get_any_proxy()}

        html = requests.get(url, headers=headers)
        html = requests.get(url)

        if html.status_code == 200:  # Everything is OK
            soup = BeautifulSoup(html.text, 'lxml')

            a = soup.find("a", {"id": "scl"})

            if a == None:
                break

            query = a.text

        elif html.status_code == 429:  # Too many requests
            break
        else:
            break

    return query, html.status_code
    
````

### Funções de orquestração

- multiprocess_request
    Essa função consiste em:
        - Receber via linha de comando o nome de um arquivo csv;
        - fazer sua leitura;
        - dividir o processamento para os N núcleos;
        - efetuar o pré-processamento em paralelo;
        - salvar o arquivo.
```python
def multiprocess_request(df:pd.DataFrame(), func, n_jobs:int=cpu_count()) -> pd.DataFrame():
    """
    Multiprocess a function that takes a DataFrame as input
    :param df: DataFrame
    :param func: function
    :param n_jobs: number of processes
    :return: DataFrame
    """
    #func -> pipeline
    df_split = np.array_split(df, n_jobs-1)
    pool = Pool(n_jobs)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


if __name__ == '__main__':
    print("Starting...")
    print("Reading dataset...")
    filepath = sys.argv[1]
    print(f"Filepath: {filepath}")
    df = pd.read_csv(f"{filepath}")
    print("Multiprocessing...")
    print(f"CPU COUNT -> {cpu_count()}")
    df = multiprocess_request(df, pipeline_multiprocess)
    df.to_csv(f"{filepath}-cleaned.csv",
              index=False)
```

## API (em desenvolvimento)

A API criada para o projeto é uma API REST que recebe um texto e retorna o texto corrigido. A API foi criada utilizando o framework Flask e está disponível no seguinte repositório:

- read_excerpts
  Esta é a função principal dentro da API. O objetivo é retornar os ids de K trechos recomendados mais próximo de um determinado termo de pesquisa.
  Para fazer isso deve ser enviado um json via post que contenha necessariamente um termo de pesquisa, e, opcionalmente, cidade, estado, data de início e data de fim.

```python
def read_excerpts(data: ExcerptReadData):
    session = DBSession()

    excerpts = session.query(DBExcerpts.excerpt_id, DBExcerpts.excerpt_vector)# DBExcerpts.excerpt_id, DBExcerpts.excerpt_vector

    if data.city:
        excerpts = excerpts.filter(DBExcerpts.city == data.city)

    if data.state:
        excerpts = excerpts.filter(DBExcerpts.state == data.state)

    if data.start_date:
        try:
            excerpts = excerpts.filter(DBExcerpts.source_date >= data.start_date)
        except InvalidDateError:
            return "Invalid date format. Please use YYYY-MM-DD"

    if data.end_date:
        try:
            excerpts = excerpts.filter(DBExcerpts.source_date <= data.end_date)
        except InvalidDateError:
            return "Invalid date format. Please use YYYY-MM-DD"


    # recommendations

    return excerpts.all()
```
