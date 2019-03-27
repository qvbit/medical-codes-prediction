import pandas as pd
import numpy as np

import re


def reformat(code, is_diag):
    """
        Put a period in the right place because the MIMIC-3 data files exclude them.
        Generally, procedure codes have dots after the first two digits, 
        while diagnosis codes have dots after the first three digits.
    """
    code = ''.join(code.split('.'))
    if is_diag:
        if code.startswith('E'):
            if len(code) > 4:
                code = code[:4] + '.' + code[4:]
        else:
            if len(code) > 3:
                code = code[:3] + '.' + code[3:]
    else:
        code = code[:2] + '.' + code[2:]
    return code

def preproc(df):
    """
    Remove '\n' and all text within brackets (and also brackets themselves)
    """
    
    df['TEXT'] = df['TEXT'].apply(lambda x: x.replace('\n', ' '))
    df['TEXT'] = df['TEXT'].apply(lambda x: re.sub("[\[].*?[\]]", "", x))
    
    return df
                              