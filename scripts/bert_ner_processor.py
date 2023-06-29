from io import StringIO
from fastapi import Depends
import pandas as pd

from api.crud.crud import create_excerpt_metadata, create_named_entity
from api.model.schemas import ExcerptMetadataCreate, NamedEntityCreate

from database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
                    'end_offset': 0,
                    'entity_type': 'PERSON'
                })
                lastIndex = len(names) - 1
    
    #if names != []:
        #print(names)
    return names

### FOR TESTS PURPOSE ONLY ###

def execute_csv(file):
    
    contents = file.file.read()
    s = str(contents,'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)
    count_excerpt = 0
    count_named_entities = 0
    for index, row in df.iterrows():
        names = find_people(row['excerpt_id'], row['excerpt'])
        excerpt_metadata = ExcerptMetadataCreate(excerpt_id=row['excerpt_id'], uf=row['source_state_code'], cidade=row['source_territory_name'], tema=row['excerpt_subthemes'], data=row['source_created_at'])
        db_gen = get_db()
        db = next(db_gen)
        count_excerpt+=1 if (create_excerpt_metadata(db, excerpt_metadata)) else False
        if len(names) > 0:
            for name in names:
                item = NamedEntityCreate(excerpt_id=name['excerpt_id'], content=name['content'], start_offset=name['start_offset'], end_offset=name['end_offset'], entity_type=name['entity_type'])

                count_named_entities+=1 if (create_named_entity(db, item)) else False

    return "Saved " + str(count_excerpt) + " excerpt ids and " + str(count_named_entities) + " named entitites"