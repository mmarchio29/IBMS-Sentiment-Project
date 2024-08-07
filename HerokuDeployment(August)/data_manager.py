import pandas as pd

def load_data():
    # Data
    file_path = r'assets/data/QuestromSA_final.csv'
    df = pd.read_csv(file_path)

    # Convert the date column to datetime format with mixed formats
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year

    # Define positive and negative sentiments
    positive_sentiments = ['Happiness', 'Love', 'Surprise']
    negative_sentiments = ['Anger', 'Disgust', 'Fear', 'Sadness']

    # Positive/Negative scores
    df['Positive'] = df[positive_sentiments].sum(axis=1)
    df['Negative'] = df[negative_sentiments].sum(axis=1)

    # Clean up whitespace and handle missing values
    df['Source Type'] = df['Source Type'].str.strip().fillna('')
    df['Publication Title'] = df['Publication Title'].str.strip().fillna('')
    df['Keyword'] = df['Keyword'].str.strip().fillna('')

    # Ensure numeric columns are indeed numeric
    numeric_columns = positive_sentiments + negative_sentiments + ['Positive', 'Negative']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df