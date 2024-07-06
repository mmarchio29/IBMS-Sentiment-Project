import pandas as pd

# file paths
file1_path = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\WDATA\\mergedWB.csv'
file2_path = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\VDATA\\mergedVIS.csv'

# read into df
wb = pd.read_csv(file1_path)
vis = pd.read_csv(file2_path)

# rename columns in the workbench dataset to match the visualization dataset
wb.rename(columns={'GOID': 'ID', 'anger': 'Anger', 'disgust': 'Disgust', 'fear': 'Fear', 'happiness': 'Happiness', 
                      'love': 'Love', 'neutral': 'Neutral', 'other': 'Other', 'sadness': 'Sadness', 
                      'surprise': 'Surprise'}, inplace=True)

# identify common columns and additional columns
common_columns = ['Date', 'ID', 'Keyword', 'Anger', 'Disgust', 'Fear', 'Happiness', 'Love', 'Neutral', 'Other', 'Sadness', 'Surprise']
additional_columns = ['Title', 'Publication']

# add additional columns to data1 with NaN values
for col in additional_columns:
    wb[col] = pd.NA

# merge
columns_to_merge = common_columns + additional_columns
merged_data = pd.concat([wb[columns_to_merge], vis[columns_to_merge]], ignore_index=True)

# save file
output_file_path  = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\WB_VIS.csv'
merged_data.to_csv(output_file_path, index=False)

output_file_path
