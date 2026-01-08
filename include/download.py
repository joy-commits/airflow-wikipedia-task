# Import dependencies
import os
import requests

from dotenv import load_dotenv
load_dotenv()

RAW_PATH = os.getenv('RAW_PATH')
WIKIPEDIA_URL = os.getenv('WIKIPEDIA_URL')

# Function to download gzip file
def download_file(**kwargs):
    """
    Download the gzip file from 
    Wikipedia and save it locally.
    """

    # Create directory if it doesn't exist
    os.makedirs(RAW_PATH, exist_ok=True)

    gz_filename = os.path.basename(WIKIPEDIA_URL)
    gz_path = os.path.join(RAW_PATH, gz_filename)

    response = requests.get(WIKIPEDIA_URL)
    response.raise_for_status()

    with open(gz_path, 'wb') as f:
        f.write(response.content)
    
    # Store the path for the next task
    kwargs['ti'].xcom_push(key='gz_path', value=gz_path)
    #kwargs['ti'].xcom_push(key='gz_filename', value=gz_filename)

    print(f"Downloaded and pushed: {gz_path}")