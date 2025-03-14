import os
from bs4 import BeautifulSoup
import re

def parse_country_info(html_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'c.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    # 获取所有国家块
    country_blocks = soup.find_all('div', {'class': 'country body-title'})
    if not country_blocks:
        return {}

    result={}
    for country_block in country_blocks:
        try:
            a_tag = country_block.find('a', class_='go')
            list_link = a_tag.get('href', '')
            country_id = re.search(r'1-4-0-(\d+)', list_link).group(1)
            
            name_span = country_block.find('span', class_='country-name-txt')
            name = name_span.text.strip() if name_span else ""
            
            flag_img = country_block.find('img', class_='dd-app-logo')
            flag_url = flag_img.get('data-src') or flag_img.get('src', '')
            country_code = flag_url.upper().split('/')[-1].split('.')[0]
            
            result[country_code]={
                "dd_country_id": country_id,
                "name": name,
                "country_code": country_code,
                "flag_url": flag_url
            }
        except (AttributeError, IndexError, TypeError) as e:
            print(f"解析错误: {e}")
            continue

    return result

# 使用示例
result = parse_country_info("c.html")
print(result)
# 将结果写入 country.py 文件
with open('country.py', 'w', encoding='utf-8') as f:
    f.write("countries = ")
    # The line `f.write(str(result))` is converting the Python dictionary `result` into a string
    # representation using the `str()` function, and then writing this string representation to the
    # file `country.py`. This allows the contents of the `result` dictionary to be written to the file
    # in a format that can be easily read back into a Python dictionary when the file is later read.
    f.write(str(result))