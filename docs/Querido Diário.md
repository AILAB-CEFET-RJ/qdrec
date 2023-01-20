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

- clean_and_insert

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

- pipeline_multiprocess

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
