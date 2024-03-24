# open a gzip file
import gzip

with gzip.open('codes_1155-to-20/16a4351ba3a137354e760e35ad69da2a350cece9.txt.gz', 'rb') as f:
    file_content = f.read()
    print(file_content)