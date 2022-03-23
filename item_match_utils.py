import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
import re
from fuzzywuzzy import process


def clean_str(text):
    text = str(text)
    text = text.lower()
    text = text.strip()
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    text = re.sub(r'\(|\)|\:', " ", text)
    text = re.sub(','        , " ", text)
    text = re.sub(r'\s+'     , " ", text)
    text = text.strip()
    return text

def get_regex_match(x, targets):
    x = clean_str(x)
    
    ls = []
    for s in targets:
        try:
            regroup = re.search(f'{s}', x)
            if len(regroup.group(0)) > 0 :
                ls.append(s_)
                ls.append(regroup.group(0))
        except:
            None
    
    if len(ls)>0:
        return '; '.join(ls)
    else:
        return 'No Match Found'
    
    
def get_fuzz_match(x, targets):
    x = clean_str(x)
    
    out = process.extract(x, targets)
    k_ls = []
    v_ls = []
    if len(out)>0:
        for k,v in out:
            k_ls.append(k)
            v_ls.append(v)

        df_match = pd.DataFrame({'target':k_ls, 'ratio':v_ls})
        df_match = df_match[df_match['ratio'] > 50]
        
        
        
        if len(df_match) > 0:
            df_match = df_match.sort_values('ratio', ascending=False).reset_index(drop=True)
            return df_match.iloc[0]['target']
        else:
            return 'No Match Found'
    else:
        return 'No Match Found'

def convert_df(df):
    return df.to_csv(index=False)