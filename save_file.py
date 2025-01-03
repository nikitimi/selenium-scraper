from pathlib import Path

def save_as_text_file(urls:list):
    file_path = Path('urls.txt')
    print(file_path)

    with file_path.open('w') as file:
        file.writelines(urls)
        
    print('File %s created successfully.' % file_path)