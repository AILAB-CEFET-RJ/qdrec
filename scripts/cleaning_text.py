

import logging
import datetime
from copy import deepcopy
import json

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



