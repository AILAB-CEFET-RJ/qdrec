import pandas as pd
import re

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

    if docs != []:
      print(docs)
      return docs


df = pd.read_csv('./dataset-ambiental.csv')
i = 0
for index, row in df.iterrows():
    if i == 100:
        break    
    
    result = str(row['excerpt']).replace('- ', '')
    #print(result)
    
    find_regex(row['excerpt_id'], result)
    i += 1
