# from a particular commit, it scraps the + and - lines of code from the html file

from bs4 import BeautifulSoup

def get_all(filename):
    try:
        with open(f'../all_commits/{filename}', 'r') as file:
            html_content = file.read()
    except:
        print(f"Error in {filename}")
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
        # print('-' * 50)
    try:
        filename= filename.split('.')[0]
        with open (f'../all_codes/{filename}.txt', 'w') as file:
            for i in range(len(data_list)):
                # print(f"{data_list[i]}")
                file.write(f"{data_list[i]}\n")
    except:
        print(f"Error in {filename}")
                # print('-' * 50)



with open('all_files_names.txt', 'r') as file:
    filenames = file.read().splitlines()
    # print(filenames)
    for filename in filenames:
        print(f"Processing {filename}")
        get_all(filename)
        # print('-' * 50)
        # print('\n')