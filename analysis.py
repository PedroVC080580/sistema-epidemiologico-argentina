import pandas as pd

# Cargar datos
def load_data():
    data = pd.read_csv('data/pathogen_data.csv')
    return data

# Total de casos
def total_cases(data):
    return data['Cases'].sum()

# Casos por patógeno
def cases_by_pathogen(data):
    return data.groupby('Pathogen')['Cases'].sum()

# Detectar brotes
def detect_outbreaks(data):
    outbreaks = data[data['Cases'] > 50]
    return outbreaks