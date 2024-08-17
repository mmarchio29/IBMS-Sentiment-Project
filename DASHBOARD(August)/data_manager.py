import pandas as pd
from functools import lru_cache

def load_data():
    # Data
    file_path = r'assets/data/QuestromSA_final.csv'
    df = pd.read_csv(file_path)
    df = df.drop_duplicates()

    # Convert the date column to datetime format with the specific format 'YYYYMMDD'
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')
    df['Year'] = df['Date'].dt.year

    # Filter data to include only records from 1900 to 2024
    df = df[(df['Year'] >= 1900) & (df['Year'] <= 2024)]

    # Define positive and negative sentiments
    positive_sentiments = ['Happiness', 'Love', 'Surprise']
    negative_sentiments = ['Anger', 'Disgust', 'Fear', 'Sadness']

    # Positive/Negative scores
    df['Positive'] = df[positive_sentiments].sum(axis=1)
    df['Negative'] = df[negative_sentiments].sum(axis=1)

    # Clean up whitespace and handle missing values
    df['Title'] = df['Title'].str.strip().fillna('')
    df['Publication'] = df['Publication'].str.strip().fillna('')
    df['Keyword'] = df['Keyword'].str.strip().fillna('')

    # Ensure numeric columns are indeed numeric
    numeric_columns = positive_sentiments + negative_sentiments + ['Positive', 'Negative']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def load_extra(data_name):
    file_path = f'assets/data/{data_name}.csv'
    df = pd.read_csv(file_path)
    return df

@lru_cache(maxsize=1)
def get_data():
    return load_data()

@lru_cache(maxsize=1)
def get_market():
    df = load_extra('djia')
    df['DATE'] = pd.to_datetime(df['date'])
    df['Year'] = df['DATE'].dt.year
    df['Year'] = df['Year'].astype(int)
    df = df.groupby(['Year'])['nominal'].mean().reset_index()
    df['nominal'] = pd.to_numeric(df['nominal'], errors='coerce')
    df['nominal'] = df['nominal'].astype(float).round(2)
    return df

@lru_cache(maxsize=1)
def get_consumer():
    df = load_extra('consumer')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Year'] = df['Year'].astype(int)
    df['UMCSENT'] = pd.to_numeric(df['UMCSENT'], errors='coerce')
    df = df.dropna(subset=['UMCSENT'])
    df['UMCSENT'] = df['UMCSENT'].astype(float).round(2)
    return df

@lru_cache(maxsize=1)
def get_inflation():
    df = load_extra('inflation')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Year'] = df['Year'].astype(int)
    df['Percent'] = pd.to_numeric(df['FPCPITOTLZGUSA'], errors='coerce')
    df['Percent'] = df['Percent'].astype(float).round(2)
    df = df.drop(columns=['DATE', 'FPCPITOTLZGUSA'])
    return df

@lru_cache(maxsize=1)
def get_unemployment():
    df = load_extra('unemployment')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Year'] = df['Year'].astype(int)
    df['Percent'] = pd.to_numeric(df['UNRATE'], errors='coerce')
    df['Percent'] = df['Percent'].astype(float).round(2)
    df = df.drop(columns=['DATE', 'UNRATE'])
    df = df.dropna()
    return df

@lru_cache(maxsize=1)
def get_wage():
    df = load_extra('wage')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Year'] = df['DATE'].dt.year
    df['Year'] = df['Year'].astype(int)
    df['Dollars'] = pd.to_numeric(df['LES1252881600Q'], errors='coerce')
    df['Dollars'] = df['Dollars'].astype(float).round(2)
    df = df.drop(columns=['DATE', 'LES1252881600Q'])
    df = df.dropna()
    return df