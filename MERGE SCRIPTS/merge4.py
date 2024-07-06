import os
import zipfile
import pandas as pd

# file paths
metadata_folder = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\METADATA'
output_folder_path = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\METADATA\\temp_extracted\\'
final_output_file = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\QuestromSA_final.csv'
sentiment_data = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\WB_VIS.csv'

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# define the name of the csv file to be merged
metadata_file = 'citation.csv'

# Function to extract specific file from zip
def extract_specific_file(zip_path, output_path, file_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith(file_name):
                zip_ref.extract(file, output_path)

# Initialize DataFrame to None
merged_metadata = pd.DataFrame()

# Extract the specific CSV file from each zipped folder and read into DataFrame
zip_files = [f for f in os.listdir(metadata_folder) if f.endswith('.zip')]

for idx, zip_filename in enumerate(zip_files):
    zip_file_path = os.path.join(metadata_folder, zip_filename)
    extract_specific_file(zip_file_path, output_folder_path, metadata_file)

    # Read the extracted CSV file into DataFrame
    for root, dirs, files in os.walk(output_folder_path):
        for file in files:
            if file == metadata_file:
                temp_df = pd.read_csv(os.path.join(root, file))
                if merged_metadata.empty:
                    merged_metadata = temp_df
                else:
                    merged_metadata = pd.concat([merged_metadata, temp_df], ignore_index=True)

    # Remove extracted files
    for file in files:
        os.remove(os.path.join(root, file))

    # Provide progress feedback
    print(f"Processed {idx + 1}/{len(zip_files)}: {zip_filename}")

# rename ID column
merged_metadata.rename(columns={'GOID': 'ID'}, inplace = True)

# full outer join with the sentiment data
merged_SAdata = pd.read_csv(sentiment_data)
merged_metadata = merged_metadata[merged_metadata['ID'].isin(merged_SAdata['ID'])]
final = pd.merge(merged_metadata, merged_SAdata, on = 'ID', how = 'outer')

# drop columns from the final merged DataFrame
columns_to_drop = ['ID', 'Title_y', 'Publication', 'Date_y']  
final.drop(columns = columns_to_drop, inplace=True)

# save file
final.to_csv(final_output_file, index=False)
