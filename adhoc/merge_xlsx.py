import pandas as pd
import glob
import os

all_data_frames = []

for f in glob.glob(r"C:\Work\jenny\*"):
    file_extension = os.path.splitext(f)[1].lower()
    df = None

    # Process based on file extension
    if file_extension == '.xlsx':
        df = pd.read_excel(f, skiprows=1)
    elif file_extension == '.xls':
        try:
            df_list = pd.read_html(f)
            if df_list:
                df = df_list[0]
        except ValueError as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"Unsupported file format: {f}")

    if df is not None:
        df['Source File'] = os.path.basename(f)
        all_data_frames.append(df)

all_data = pd.concat(all_data_frames, ignore_index=True)
all_data.to_csv(r"C:\Work\jenny\output.csv", index=False)