from io import StringIO
from fastapi import Depends
import pandas as pd
import re

from api.crud.crud import create_excerpt_metadata, create_named_entity
from api.model.schemas import ExcerptMetadataCreate, NamedEntityCreate

from database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def find_regex(id:str, text:str) -> list:
    docs=[]
    cnt=0

    url_extract_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    mail_extract_pattern = "([a-z0-9_.-]+@[a-z0-9_.-]+)"
    cpf_extract_pattern = "\d{3}\.?\d{3}\.?\d{3}\-?\d{2}"
    cnpj_extract_pattern = "\d{2}\.?\d{3}\.?\d{3}\/\d{4}-\d{2}"

    for url in re.finditer(url_extract_pattern, str(text)):
      cnt+=1

      docs.append({'excerpt_id': id,
                   'content': url.group(),
                   'start_offset': url.start(),
                   'end_offset': url.start() + len(url.group()),
                   'entity_type':"URL"})

    for email in re.finditer(mail_extract_pattern, str(text)):
      cnt+=1

      docs.append({'excerpt_id': id,
                   'content': email.group(),
                   'start_offset': email.start(),
                   'end_offset': email.start() + len(email.group()),
                   'entity_type':"E-mail"})

    for cpf in re.finditer(cpf_extract_pattern, str(text)):
      cnt+=1

      docs.append({'excerpt_id': id,
                   'content': cpf.group(),
                   'start_offset': cpf.start(),
                   'end_offset': cpf.start() + len(cpf.group()),
                   'entity_type':"CPF"})

    for cnpj in re.finditer(cnpj_extract_pattern, str(text)):
      cnt+=1

      docs.append({'excerpt_id': id,
                   'content': cnpj.group(),
                   'start_offset': cnpj.start(),
                   'end_offset': cnpj.start() + len(cnpj.group()),
                   'entity_type':"CNPJ"})

    #if docs != []:
     # print(docs)
      #return docs

    return docs if docs else []

def execute_csv_regex(file):

    contents = file.file.read()
    s = str(contents,'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)

    count_excerpt = 0
    count_named_entities = 0
    for index, row in df.iterrows():

        result = str(row['excerpt']).replace('- ', '')
        docs = find_regex(row['excerpt_id'], result)
        excerpt_metadata = ExcerptMetadataCreate(excerpt_id=row['excerpt_id'], uf=row['source_state_code'], cidade=row['source_territory_name'], tema=row['excerpt_subthemes'], data=row['source_created_at'])
        db_gen = get_db()
        db = next(db_gen)
        count_excerpt+=1 if (create_excerpt_metadata(db, excerpt_metadata)) else False
        if len(docs) > 0:
            for name in docs:
                item = NamedEntityCreate(excerpt_id=name['excerpt_id'], content=name['content'], start_offset=name['start_offset'], end_offset=name['end_offset'], entity_type=name['entity_type'])

                count_named_entities+=1 if (create_named_entity(db, item)) else False

    return "Saved " + str(count_excerpt) + " excerpt ids and " + str(count_named_entities) + " named entitites"