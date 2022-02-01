import requests
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

output_path = './pytorch/data/github/'
files = {'1FYfNZKNUXaYTKuOhwY3POhnUGpnQuZOe': 'use.name.h5', 
         '1yQwqzx7hW7qMGnRDOolI_vYZDNN0_SoA': 'use.tokens.h5',
         '11Iia3ZyNuD-TYeymo8I3hU1YTNweY9_i': 'use.apiseq.h5'
}
if __name__ == "__main__":
    for key in files.keys(): 
        file_id = key
        destination = os.path.join(output_path, files[key])
        download_file_from_google_drive(file_id, destination)