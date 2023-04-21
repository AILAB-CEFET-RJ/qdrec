import pandas as pd

'''
Citação de projeto utilizado: https://github.com/neuralmind-ai/portuguese-bert
@InProceedings{souza2020bertimbau,
    author="Souza, F{\'a}bio and Nogueira, Rodrigo and Lotufo, Roberto",
    editor="Cerri, Ricardo and Prati, Ronaldo C.",
    title="BERTimbau: Pretrained BERT Models for Brazilian Portuguese",
    booktitle="Intelligent Systems",
    year="2020",
    publisher="Springer International Publishing",
    address="Cham",
    pages="403--417",
    isbn="978-3-030-61377-8"
}
'''

from transformers import BertForTokenClassification, DistilBertTokenizerFast, pipeline
model = BertForTokenClassification.from_pretrained('pierreguillou/ner-bert-large-cased-pt-lenerbr')
tokenizer = DistilBertTokenizerFast.from_pretrained('pierreguillou/bert-large-cased-pt-lenerbr'
                                                    , model_max_length=512
                                                    , do_lower_case=False
                                                    )
nlp = pipeline('ner', model=model, tokenizer=tokenizer, grouped_entities=True)

def find_people(id:str, text:str) -> list:

    result = nlp(str(text).replace('- ', ''))
    names = []
    lastIndex = 0

    for item in result:
        if item['entity_group'] == "PESSOA":
            if "#" in item['word'] and names != []:
                name = names[lastIndex]['content']
                name += item['word']
                names[lastIndex]['content'] = name.replace("#", '')
                names[lastIndex]['end_offset'] = item['end']
            else:
                names.append({
                    'excerpt_id': id,
                    'content': item['word'],
                    'start_offset': item['start'],
                    'end_offset': '',
                    'entity_type': 'PERSON'
                })
                lastIndex = len(names) - 1
    
    if names != []:
        print(names)
        return names
    

### FOR TESTS PURPOSE ONLY ###
df = pd.read_csv('../dataset-ambiental.csv')
i = 0
for index, row in df.iterrows():
    if i == 100:
        break
    find_people(row['excerpt_id'], row['excerpt'])
    i += 1