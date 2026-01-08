# Import dependencies
import gzip
import os

from dotenv import load_dotenv
load_dotenv()

PROCESSED_PATH = os.getenv('PROCESSED_PATH')

# Function to extract gzip file
def extract_file(**kwargs):
    """
    Extract the gzip file into a txt file.
    """
    # Retrieve the gz_path from previous task using XCom.
    gz_path = kwargs['ti'].xcom_pull(key='gz_path', task_ids='download')

    txt_filename = gz_path.replace('.gz', '')  # Remove .gz extension.
    txt_path = os.path.join(PROCESSED_PATH, os.path.basename(txt_filename))
    
    with gzip.open(gz_path, 'rb') as f_in:
        with open(txt_path, 'wb') as f_out:
            f_out.write(f_in.read())
    
    # Store the extracted path for the next task.
    kwargs['ti'].xcom_push(key='txt_path', value=txt_path)
    kwargs['ti'].xcom_push(key='txt_filename', value=txt_filename)