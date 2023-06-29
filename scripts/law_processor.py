import re
from io import StringIO
from fastapi import Depends
import pandas as pd

import requests
from bs4 import BeautifulSoup
import json
import time

from api.crud.crud import create_excerpt_metadata, create_named_entity
from api.model.schemas import ExcerptMetadataCreate, NamedEntityCreate

from database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_law_info(law_number: str) -> dict:

    cookies = {
        'f5_cspm': '1234',
        'TS00000000076': '086567d05fab2800558c1f86c1d1ee549702eead90d33434ae66c56a4244860651de79ea141290d3213acb2b52197fa408058548cf09d00008dbebd2947a373f45131a7027ef3c9cf8b4e5401e62ee8fa922bbb5cce88e51750f1e51a65e9f20275bf21be810a873ec2d369169cfe46b3bab77d95a07771b2d99100c21a92db8b06db5d93d3624c2bf288c499a9e05332933f493cd8c976f1be7ca21d5b25d13157cd98df28a50caa3ac8c65604c58a5f65c46b582046ddabb95eb0539a30a84c93ba47aeca350c6e4aa12bca2ce69d32b103b8eca5c56dff37f048ab4c5500863d874ab11af5dfeca91fc8c5ce2aaa74aeaf051aaa70296daa6b6c4b8642e6a57c0628185dd111f',
        'TSPD_101_DID': '086567d05fab2800558c1f86c1d1ee549702eead90d33434ae66c56a4244860651de79ea141290d3213acb2b52197fa408058548cf063800b491cd897376f485c0be259785df303997b1c270a8c7f8a3c85c1e4b2916617a5bb80b339dce8c90ba2186efbe9e5e9dfa3524f201ce3e70',
        'TS01acd2cb': '0150f80db1851f386586dcd76eb04f13bc5d758f2099cfdb2d4ab54c751cd0fc6f09989f768c5453ec0cf92e04ab7797742fc34056f0f2aa09b4d36a7b521537bc83070626a2e8375ff6107965fdf21a0acb9c7d19',
        'TSPD_101': '086567d05fab2800168607c0335cc8ae4456329a64b7f9290a701ee14cd8a4abe6f7e631970f1d29c90046e36ef565250814c89176051800a4af617ffde9f551304602e69b56a39104eeedb0a518443c',
        'TS99db2205077': '086567d05fab2800dfa72b04fa4c5998522c0f49e497af8e979d937ed22a94c0cc9e3bad3afbeccffbddd0d5b5ac75f008a6d67891172000615e3921599c453890a79e4c9868afe10a86264d52e8d74f8c6d04ae8093fd62',
        'TS6b6d31b1027': '086567d05fab200047ad112575b7841617cc9fd19c030f95e7791e268e08e75512364f81d3b69e05081a4f2ea71130009ae6ad9a491b68822ae7261b9368fbba56469db493510333a0287ebaca9892d02e5b6840cc07d9bc1c4670e5d0fbebf5',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'f5_cspm=1234; TS00000000076=086567d05fab2800088fb59476ad4bfb13e3d23dd4c1e5fc8db0fbc40c4a3e00b342c4f9c1e6e8933888a773e74e344c08b6baffa109d00050bf073f0c543ae6cc5e0f0a3e72b5b76edab836b0db73e664551a53198b3b4cf6e2bc422608ee7175dd5387493eaaddcd23134e4f0e0fa2ef754c5379b7076dfd34a3be6707cfd4bd7d2b97b82e5938070ef261b528c4abab389b15b864d4fbfd74f46a82910dc008d33242b74534051c874193a5dcde2846c767e2dad3360502afaf91462c7166769c2f1f58e61e3cc4d5885602bd9cd9a1993e681951ca1ad76e556d9811becca1be03351debca6fa60500492fa47be5951964515316c1f79d4fc43dfd5f469715c6af3212d8d5b0; TSPD_101_DID=086567d05fab2800088fb59476ad4bfb13e3d23dd4c1e5fc8db0fbc40c4a3e00b342c4f9c1e6e8933888a773e74e344c08b6baffa106380029093da7ff315f0341545f72b078e4514fc4c3110a5f8465e49aaf0efa7df7fb0ed2821294498e0299247c3e190849d7bd0f24810093d4e3; TS01acd2cb=0150f80db1389bb9f487ed0e879a4068b846c401981a55a03fde4e61114f258e46ed1ccfd01297063c84833d920d77e6d2abf8e9dfd9e06501cf1ec9becc081d8500575a5b5245476b07454db0bae952c433ef044a; TSPD_101=086567d05fab2800aabf33d5701b5cdf40ca7f16036e893ddd1c3ec9a98cd44e366f459841dc1d60a50a49e9265dbcd708ba4e3099051800d3a65cbd3e71ac1a304602e69b56a39104eeedb0a518443c; TS99db2205077=086567d05fab2800c08aabbc77fa2afda2b4ab21be22c7719feedd93937cf8dfbe04c1de2ed02e757709cf3545f4914a086c68300917200012c1c0d9523533471900adfaeec9ae435ea67b198b200266ba54704df6147303; TS6b6d31b1027=086567d05fab2000f06cf2d518f77c509e492f8d4f021521e14b2688ce14146ddf2a3315b2a2433b0883e2162111300024b13cf213b7219e81e1b45f88ec3eb4ec20a4601515b2e1ba2c21f38c93147f88b75ccab7d7f89d21ecd034f61899a0',
        'Origin': 'https://legislacao.presidencia.gov.br',
        'Referer': 'https://legislacao.presidencia.gov.br/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    data = {
        'pagina': '0',
        'posicao': '0',
        'termo': '',
        'num_ato': law_number,
        'ano_ato': '',
        'dat_inicio': '',
        'dat_termino': '',
        'tipo_macro_ato': '',
        'tipo_ato': '',
        'situacao_ato': '',
        'presidente_exercicio': '',
        'chefe_governo': '',
        'dsc_referenda_ministerial': '',
        'referenda_ministerial': '',
        'origem': '',
        'diario_extra': '',
        'data_resenha': '',
        'num_mes_resenha': '',
        'num_ano_resenha': '',
        'ordenacao': 'maior_data',
        'conteudo_tipo_macro_ato': '',
        'conteudo_tipo_ato': '',
        'conteudo_situacao_ato': '',
        'conteudo_presidente_exercicio': '',
        'conteudo_chefe_governo': '',
        'conteudo_referenda_ministerial': '',
        'conteudo_origem': '',
        'conteudo_diario_extra': '',
    }

    response = requests.post(
        'https://legislacao.presidencia.gov.br/pesquisa/ajax/resultado_pesquisa_legislacao.php',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    dict_response =  {}
    
    time.sleep(2)

    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find_all('h4', class_='card-title')
    link = content[0].a.get('href')
    

    lei_data = content[0].text.strip().replace('de', '-', 1)

    lei, data = lei_data.split('-')

    dict_response['link'] = link.strip()
    dict_response['lei'] = lei.strip()
    dict_response['data'] = data.strip()

    response_2 = requests.get(dict_response['link'], headers=headers, verify=False)

    soup = BeautifulSoup(response_2.content, 'html.parser')

    content = soup.find_all('p')

    doc = ""

    for text in content:
        doc+=(text.text)

    dict_response['doc_lei'] = doc

    response_json_str = json.dumps(dict_response)

    return response_json_str



def find_law(id:str, text:str) -> list:
    laws=[]
    cnt=0
    law_regex = "(?i)(Lei|Decreto)\s*(?:[Ff]ederal|[Mm]unicipal)?\s*(?:n?[oº]?°?\s*)?(\d{1,6})[./](\d{1,4})(/(\d{2,4}))?"

    num_regex = "^\d{2}\.\d{3}$"
    
    for law in re.finditer(law_regex, str(text)):
        cnt+=1

        content = law.group()

        pattern = r"\b\d{1,2}\.\d{3}\b"

        num_law = re.findall(pattern, content)

        if len(num_law) == 0:
            continue
        
        content_dict = get_law_info(num_law)
        
        laws.append({
                'excerpt_id': id,
                'content': content_dict,
                'start_offset': law.start(),
                'end_offset': law.start() + len(law.group()),
                'entity_type': 'LAW'
                })
    return laws


def execute_csv_law(file):
    
    contents = file.file.read()
    s = str(contents,'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)
    count_excerpt = 0
    count_named_entities = 0

    for index, row in df.iterrows():
        names = find_law(row['excerpt_id'], row['excerpt'])
        excerpt_metadata = ExcerptMetadataCreate(excerpt_id=row['excerpt_id'], uf=row['source_state_code'], cidade=row['source_territory_name'], tema=row['excerpt_subthemes'], data=row['source_created_at'])
        db_gen = get_db()
        db = next(db_gen)
        count_excerpt+=1 if (create_excerpt_metadata(db, excerpt_metadata)) else False
        if len(names) > 0:
            for name in names:
                item = NamedEntityCreate(excerpt_id=name['excerpt_id'], content=name['content'], start_offset=name['start_offset'], end_offset=name['end_offset'], entity_type=name['entity_type'])

                count_named_entities+=1 if (create_named_entity(db, item)) else False

    return "Saved " + str(count_excerpt) + " excerpt ids and " + str(count_named_entities) + " named entitites"
