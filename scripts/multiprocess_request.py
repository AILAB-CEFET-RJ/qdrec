from multiprocessing import cpu_count, Pool
import numpy as np
import pandas as pd
from google_scrapper import fix_spelling_in_answer
from preprocess_qd import pipeline_multiprocess

import sys



def multiprocess_request(df:pd.DataFrame(), func, n_jobs:int=cpu_count()) -> pd.DataFrame():
    """
    Multiprocess a function that takes a DataFrame as input
    :param df: DataFrame
    :param func: function
    :param n_jobs: number of processes
    :return: DataFrame
    """
    #func -> pipeline
    df_split = np.array_split(df, n_jobs-1)
    pool = Pool(n_jobs)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


if __name__ == '__main__':
    print("Starting...")
    print("Reading dataset...")
    filepath = sys.argv[1]
    print(f"Filepath: {filepath}")
    df = pd.read_csv(f"{filepath}")
    print("Multiprocessing...")
    print(f"CPU COUNT -> {cpu_count()}")
    df = multiprocess_request(df, pipeline_multiprocess)
    df.to_csv(f"{filepath}-cleaned.csv",
              index=False)