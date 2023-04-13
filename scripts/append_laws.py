
import re
import pandas as pd


def find_laws(text:str) -> list:
    docs=[]
    cnt=0
    law_regex = "(?i)(Lei|Decreto)\s*(?:[Ff]ederal|[Mm]unicipal)?\s*(?:n?[oº]?°?\s*)?(\d{1,6})[./](\d{1,4})(/(\d{2,4}))?"
    
    for law in re.finditer(law_regex, str(text)):
        cnt+=1
        docs.append({'doc':law.group(), 
                     'start_doc': law.start(),
                     'end_doc': law.start() + len(law.group()),
                     'doc_type':"LAW"})
    return docs




def append_laws(df:pd.DataFrame) -> pd.DataFrame:
    
    df["laws"] = df["excerpt"].apply(find_laws)
    
    return df
