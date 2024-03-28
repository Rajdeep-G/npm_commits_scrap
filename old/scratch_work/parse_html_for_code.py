# from a particular commit, it scraps the + and - lines of code from the html file
import os
from bs4 import BeautifulSoup
from datetime import datetime
import gzip
def get_all(filename, path_name):
    try:
        with gzip.open(f'../{path_name}/{filename}.gz', 'r') as file:
            html_content = file.read()
    except:
        print(f"Error iiin {filename}")
        return
    
    soup = BeautifulSoup(html_content, 'html.parser')


    trs = soup.find_all('tr', attrs={'data-hunk': True})


    # for tr in trs:
        # print(tr)
    # print(len(trs))


    data_list = []

    for tr in trs:
        span = tr.find('span', class_='blob-code-inner')
        content = span.get_text(strip=True)
        data_code_marker = span['data-code-marker'] if 'data-code-marker' in span.attrs else ''

        # print(f"{data_code_marker} {content}")
        data_dict = {'content': content, 'data-code-marker': data_code_marker}
        data_list.append(data_dict)


        # print('-' * 50)
    # print(data_list[3])

    for i in range(len(data_list)):
        code= data_list[i]['content']
        code = code.strip()
        for j in range(10):
            code = code.replace('  ', ' ')
            code= code.replace('\n', ' ')
        data_list[i]['content'] = code
        # print(code)
    print('++' * 50)
    try:
        filename= filename.split('.')[0]
        # os.mkdir(f'../codes_{path_name}',exist_ok=True)
        with open (f'../codes_{path_name}/{filename}.txt', 'w') as file:
            for i in range(len(data_list)):
                # print(f"{data_list[i]}")
                file.write(f"{data_list[i]}\n")
    except:
        print(f"Error in {filename}")
                # print('-' * 50)


start_time_global = datetime.now()
with open('../gh_links.txt', 'r') as file:
    gh_links = file.read().splitlines()
    # print(gh_links)
    for link in gh_links[:2]:
        if not link:
            continue
        temp = link.split()
        
        path_name = temp[0]
        
        os.makedirs(f'../codes_{path_name}', exist_ok=True)
        with open(f'{path_name}_file_names.txt', 'r') as file:
            filenames = file.read().splitlines()
            # print(filenames)
            for filename in filenames:
                print(f"Processing {filename}")
                get_all(filename, path_name)
                
                # print('\n')
        print('-' * 50)
end_time_global = datetime.now()
print(f"Total time taken: {end_time_global - start_time_global}")