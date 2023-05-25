import string
from querido_diario.db.engine import DBSession
from querido_diario.db.models import DBExcerpts
import difflib

from typing import Optional

from pydantic import BaseModel

from datetime import date

class InvalidDateError(Exception):
    "Invalid date format. Please use YYYY-MM-DD"

#class Excerpt(BaseModel):
#    excerpt_id: str
#    excerpt_processed: str
#    source_territory_name: str
#    source_state_code: str
#    excerpt_vector: str#BLOB
#    source_date: datetime.date

class ExcerptReadData(BaseModel):
    # Required data
    term: str #search term

    # Optional data
    city: Optional[str]
    state: Optional[str]
    start_date: Optional[date] #published since
    end_date: Optional[date] #published until
    

def read_all_excerpts():
    """Read all excerpts from the database."""
    session = DBSession()
    excerpts = session.query(DBExcerpts).all()
    return excerpts

def read_excerpt(excerpt_id: str):
    session = DBSession()
    excerpts = session.query(DBExcerpts).get(excerpt_id)#.filter(DBExcerptss.text_id == text_id).first()
    return excerpts


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


def get_recommended_excerpts(data: ExcerptReadData):
    # get excerpts
    excerpts = read_excerpts(data)
    term = embed(data.term)
    # get vector
    # get recommendations
    # return recommendations
    pass

def get_entity(data: string, entity_type: string):
    # get all entities
    # test simulating return from db
    entities = [{'excerpt_id': '123',
                    'content': 'JAIME CRUZ',
                    'start_offset': 0,
                    'end_offset': 9,
                    'entity_type': 'PERSON'},
                {'excerpt_id': '234',
                    'content': 'JAIME CRUZ',
                    'start_offset': 1,
                    'end_offset': 10,
                    'entity_type': 'PERSON'}]
    
    for entity in entities:
        closest_match = difflib.get_close_matches(data, [entity['content']])
        substring = data in entity['content']
        if (closest_match or substring) and entity['entity_type'] == entity_type:
            print('For entry string:', data, 'closest entity found:', closest_match) if closest_match else True
            print('start:', entity['start_offset'], 'end:', entity['end_offset'])

get_entity('CRUZ', 'PERSON')