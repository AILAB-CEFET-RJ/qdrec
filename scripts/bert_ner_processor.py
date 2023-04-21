import pandas as pd

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
        print(item)
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
        return names
    
'''
### FOR TESTS PURPOSE ONLY ###
df = pd.read_csv('../dataset-ambiental.csv')
i = 0
for index, row in df.iterrows():
    if i == 100:
        break
    print(find_people(row['excerpt_id'], row['excerpt']))
    i += 1
'''