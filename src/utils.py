import requests
from datetime import datetime
import pandas as pd

def parse_custom_date(date_float):
    try:
        date_str = str(int(date_float))
        # Assuming date_str is in the format "YYYYMM"
        year = int(date_str[:4])
        month = int(date_str[4:])
        return datetime(year, month, 1)  # Set day to 1 since the day is not provided in the float format
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None

def parse_excel_file(file_paths):
    if not isinstance(file_paths, list):
        file_paths = list(file_paths)

    df_return = pd.DataFrame()

    for file_path in file_paths:
        df = pd.read_excel(file_path)

        if len(df.columns) > 9:
            df = df.iloc[:,1:].reset_index(drop=True)
        column_names = df.iloc[2].values

        df = df.iloc[4:]
        df.columns = column_names


        column_names[0] = "year"
        column_names[1] = "year_month"
        column_names[2] = "month"

        df.columns = df.columns.str.lower()
        df.year = df.year.ffill()
        df.dropna(inplace=True)
        df["date_time"] = df.year_month.apply(parse_custom_date)

        df_return = pd.concat([df_return, df]).reset_index(drop=True)

        df_return['total'] = df_return['total'].astype(float)

    return df_return


def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there's an error in the response
        with open(save_path, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")

def format_sepe_file(file_path):
    pass