import requests

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