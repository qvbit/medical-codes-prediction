import pandas as pd
import numpy as np
import re

from preproc_functions import *
from constants import *


if __name__ == '__main__':
    
    df_proc = pd.read_csv('%s/PROCEDURES_ICD.csv' % MIMIC_3_DIR)
    df_diag = pd.read_csv('%s/DIAGNOSES_ICD.csv' % MIMIC_3_DIR)

    df_diag['ABS_CODE'] = df_diag.apply(lambda row: str(reformat(str(row[4]), True)), axis=1)
    df_proc['ABS_CODE'] = df_proc.apply(lambda row: str(reformat(str(row[4]), False)), axis=1)

    df_codes = pd.concat([df_diag, df_proc])

    df_notes = pd.read_csv('%s/NOTEEVENTS.csv' % MIMIC_3_DIR)
    
    # Only consider discharge summaries:
    df_notes = df_notes[df_notes['CATEGORY'] == 'Discharge summary']
    
    # Drop rows with null HADM_IDs
    df_notes = df_notes.dropna(subset=['HADM_ID'])
    
    # Convert all IDs to int
    df_notes['SUBJECT_ID'] = df_notes['SUBJECT_ID'].apply(lambda x: int(x))
    df_notes['HADM_ID'] = df_notes['HADM_ID'].apply(lambda x: int(x))

    df_codes['SUBJECT_ID'] = df_codes['SUBJECT_ID'].apply(lambda x: int(x))
    df_codes['HADM_ID'] = df_codes['HADM_ID'].apply(lambda x: int(x))
    
    # Some non-aggressive preprocessing. More preprocessing will be done by model tokenizer.
    df_notes = preproc(df_notes)
    
    # Append all notes and addenda
    df_notes_grouped = df_notes.groupby(by=['HADM_ID','SUBJECT_ID'], as_index=False).agg({'TEXT': lambda x: ' '.join(x)})
    
    # Left join the two dataframes such that we discard any HADM_IDs not appearing in df_notes
    merged = pd.merge(df_notes_grouped, df_codes, on='HADM_ID', how='left')
    
    # Group by HADM_ID and SUBJECT_ID, aggregating on the ICD9_codes and appending them to a list.
    grouped = merged.groupby(by=['HADM_ID', 'SUBJECT_ID_x'], as_index=False).agg({'ABS_CODE': lambda x: list(x),
                                                                              'TEXT': 'first'})
    
    # Just some cosmetic stuff
    grouped = grouped.sort_values(['SUBJECT_ID_x', 'HADM_ID'])
    grouped = grouped.rename(columns={'ABS_CODE': 'LABELS', 'SUBJECT_ID_x': 'SUBJECT_ID'})
    grouped = grouped[['SUBJECT_ID', 'HADM_ID', 'TEXT', 'LABELS']]
    grouped = grouped.reset_index(drop=True)
    
    # Convert labels to a semi-colon seperated string.
    grouped['LABELS'] = grouped['LABELS'].apply(lambda x: ';'.join(x))

    remove = ['admission date:', 'discharge date:', 'date of birth:', 'service:', 'chief complaint:', 'HISTORY OF PRESENT ILLNESS:',
          'PAST MEDICAL HISTORY:', 'admission diagnosis:', 'history of the present illness:', 'attending:', 'cc:']

    remove = [r.lower() for r in remove]

    #remove words in 'remove' as these dont add anything informative. 
    grouped['TEXT'] = grouped['TEXT'].apply(lambda x: re.sub(r'|'.join(map(re.escape, remove)), '', x.lower()))
    grouped['TEXT'] = grouped['TEXT'].apply(lambda x: x.lstrip())
    
    # Save dataframe
    grouped.to_pickle('dataframes/df_data.pkl')
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
