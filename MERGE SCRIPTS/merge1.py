import pandas as pd
import os

def merge_csv_files(wbdata, output_file_path):

    dataframes = []
    for filename in os.listdir(wbdata):
        if filename.endswith(".csv") and filename != os.path.basename(output_file_path):
            file_path = os.path.join(wbdata, filename)
            df = pd.read_csv(file_path)
            dataframes.append(df)

            # add keyword column
            keyword = filename.split("WB")[0]
            df['Keyword'] = keyword

    merged_data = pd.concat(dataframes, ignore_index=True)
    merged_data.to_csv(output_file_path, index=False)

# save file
wbdata = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\WDATA\\'
output_file_path = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\WDATA\\mergedWB.csv'
merge_csv_files(wbdata, output_file_path)

output_file_path
