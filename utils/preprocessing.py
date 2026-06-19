import pandas as pd

def preprocess_data(df):

    fitur = [
        'duration',
        'src_bytes',
        'dst_bytes',
        'src_ip_bytes',
        'dst_ip_bytes'
    ]

    return df[fitur]