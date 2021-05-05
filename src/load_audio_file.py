import requests
import os
from zipfile import ZipFile


def load_file(url='http://www.archive.org/download/alices_adventures/alices_adventures_64kb_mp3.zip'):
    print('requesting data')
    file_name = os.path.join('data', url.split('/')[-1])
    print(os.getcwd())
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    r = requests.get(url, allow_redirects=True, stream=True)
    print('Response code: ', r.status_code)
    print('Writing File to: ', file_name)
    with open(file_name, 'wb') as file:
        file.write(r.content)


def unzip_file(path="data"):
    list_of_audiobooks = os.listdir(path)
    print(list_of_audiobooks)
    print('Books are: ', list_of_audiobooks)
    for book in list_of_audiobooks:
        print(book)
        if 'mp3' in book:
            file_name = os.path.join(path, book)
            # opening the zip file in READ mode 
            folder_name = os.path.join(path, book.split('.')[0])
            print('Folder names is: ', folder_name)
            print('File opening...', file_name)
            with ZipFile(file_name, 'r') as zipfile:
                # extracting all the files 
                print('Extracting all the files now...')
                zipfile.extractall(path=folder_name)
                print('Done!')
            os.remove(file_name)


if __name__ == "__main__":
    load_file()
