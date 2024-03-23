from bs4 import BeautifulSoup

# Read the HTML file
with open('w.html', 'r') as file:
    html_content = file.read()

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
for i in range(len(data_list)):
    print(f"{data_list[i]}")
    print('-' * 50)



