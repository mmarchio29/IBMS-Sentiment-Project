import os
import zipfile
import pandas as pd

# file paths
visdata = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\new_VDATA\\'
output_folder_path = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\new_VDATA\\temp_extracted\\'
merged_output_file = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\idk.csv'

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# two CSV files to be merged
file1_name = 'documentmetadata.csv'
file2_name = 'emotion_docs.csv'
shared_column = 'ID'

# extract specific files from zip
def extract_specific_files(zip_path, output_path, file_names):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if any(file.endswith(name) for name in file_names):
                zip_ref.extract(file, output_path)

# process CSV files in a folder
def process_csv_files_in_folder(folder_path, keyword):
    global df1, df2
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == file1_name:
                temp_df1 = pd.read_csv(os.path.join(root, file))
                temp_df1['Keyword'] = keyword 
                if df1 is None:
                    df1 = temp_df1
                else:
                    df1 = pd.concat([df1, temp_df1], ignore_index=True)
            elif file == file2_name:
                temp_df2 = pd.read_csv(os.path.join(root, file))
                if df2 is None:
                    df2 = temp_df2
                else:
                    df2 = pd.concat([df2, temp_df2], ignore_index=True)

# initialize DataFrames
df1 = None
df2 = None

# process both zip files and regular folders
items = os.listdir(visdata)

for idx, item in enumerate(items):
    item_path = os.path.join(visdata, item)
    
    # if item is a zip file
    if item.endswith('.zip'):
        extract_specific_files(item_path, output_folder_path, [file1_name, file2_name])
        keyword = os.path.splitext(item)[0].split('-')[0]
        process_csv_files_in_folder(output_folder_path, keyword)

        # clean up extracted files
        for file in os.listdir(output_folder_path):
            os.remove(os.path.join(output_folder_path, file))
        
    # if item is a regular folder
    elif os.path.isdir(item_path):
        keyword = os.path.basename(item_path).split('-')[0]
        process_csv_files_in_folder(item_path, keyword)
    
    # progress
    print(f"Processed {idx + 1}/{len(items)}: {item}")

# save merged file
if df1 is not None and df2 is not None:
    merged_df = pd.merge(df1, df2, on=shared_column)
    merged_df.drop_duplicates(subset=['ID', 'Keyword'], keep='first', inplace=True)
    
    merged_df.to_csv(merged_output_file, index=False)
    print(f"Merged CSV file saved to {merged_output_file}")
else:
    print("One or both of the specified files were not found.")
